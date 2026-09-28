from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
)

from sqlalchemy.orm import Session

from ..auth import (
    create_access_token,
    hash_password,
    verify_password,
)

from ..config import get_settings
from ..database import get_db
from ..dependencies import get_current_user
from ..models.db_models import User
from ..models.schemas import (
    LoginRequest,
    RegisterRequest,
)


router = APIRouter(
    tags=["auth"]
)


@router.post("/register")
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
):

    email = payload.email.lower()

    existing = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists",
        )

    user = User(
        email=email,
        password_hash=hash_password(
            payload.password
        ),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        user.id
    )

    settings = get_settings()

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=(
            settings.access_token_expire_minutes
            * 60
        ),
    )

    return {
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(
            User.email
            == payload.email.lower()
        )
        .first()
    )

    if not user or not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token(
        user.id
    )

    settings = get_settings()

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=(
            settings.access_token_expire_minutes
            * 60
        ),
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }


@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        "access_token"
    )

    return {
        "message": "Logged out"
    }


@router.get("/session-info")
def session_info(
    user: User = Depends(
        get_current_user
    ),
):

    return {
        "authenticated": True,
        "user_id": user.id,
        "email": user.email,
    }


@router.get("/session-data")
def session_data(
    user: User = Depends(
        get_current_user
    ),
):

    return {
        "user_id": user.id,
        "email": user.email,
        "login_status": "active",
    }
    