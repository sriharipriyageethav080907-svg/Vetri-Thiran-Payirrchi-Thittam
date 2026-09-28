from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..dependencies import get_current_user
from ..models.db_models import User
from ..models.schemas import (
    HomeRequest,
    JewelryRequest,
    PartyRequest,
)
from ..services.recommendations import (
    make_recommendation,
)


router = APIRouter(
    tags=["planners"]
)


@router.post("/generate-home")
async def generate_home(
    payload: HomeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(
        get_current_user
    ),
):

    return await make_recommendation(
        db=db,
        user_id=user.id,
        planner="home",
        data=payload.model_dump(),
    )


@router.post("/generate-party")
async def generate_party(
    payload: PartyRequest,
    db: Session = Depends(get_db),
    user: User = Depends(
        get_current_user
    ),
):

    return await make_recommendation(
        db=db,
        user_id=user.id,
        planner="party",
        data=payload.model_dump(),
    )


@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...),
    currency: str = Form("INR"),
    occasion: str = Form("Wedding"),
    style: str = Form("Elegant"),
    metal: str = Form("Any"),
    outfit_color: str = Form(""),
    notes: str = Form(""),
    outfit_image: UploadFile | None = File(
        default=None
    ),
    db: Session = Depends(get_db),
    user: User = Depends(
        get_current_user
    ),
):

    if budget <= 0:
        raise HTTPException(
            status_code=422,
            detail="Budget must be greater than zero",
        )

    settings = get_settings()

    image_bytes = None
    mime = None

    if outfit_image and outfit_image.filename:

        mime = (
            outfit_image.content_type
            or ""
        ).lower()

        if (
            mime
            not in settings.allowed_image_type_set
        ):
            raise HTTPException(
                status_code=415,
                detail=(
                    "Only JPEG, PNG and WebP "
                    "images are supported"
                ),
            )

        image_bytes = (
            await outfit_image.read()
        )

        if (
            len(image_bytes)
            > settings.max_image_bytes
        ):
            raise HTTPException(
                status_code=413,
                detail="Image is too large",
            )

    payload = JewelryRequest(
        budget=budget,
        currency=currency,
        occasion=occasion,
        style=style,
        metal=metal,
        outfit_color=outfit_color,
        notes=notes,
    )

    data = payload.model_dump()

    return await make_recommendation(
        db=db,
        user_id=user.id,
        planner="jewelry",
        data=data,
        image_bytes=image_bytes,
        image_mime=mime,
    )
    