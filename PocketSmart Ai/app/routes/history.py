import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models.db_models import (
    RecommendationHistory,
    User,
)


router = APIRouter(
    tags=["history"]
)


@router.get("/history")
def history(
    db: Session = Depends(get_db),
    user: User = Depends(
        get_current_user
    ),
):

    rows = (
        db.query(
            RecommendationHistory
        )
        .filter(
            RecommendationHistory.user_id
            == user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
        .all()
    )

    return [
        {
            "id": row.id,
            "planner_type": row.planner_type,
            "created_at": row.created_at.isoformat(),
            "result": json.loads(
                row.result_json
            ),
        }
        for row in rows
    ]


@router.get(
    "/recommendations-details/{recommendation_id}"
)
def recommendation_details(
    recommendation_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(
        get_current_user
    ),
):

    row = (
        db.query(
            RecommendationHistory
        )
        .filter(
            RecommendationHistory.id
            == recommendation_id,
            RecommendationHistory.user_id
            == user.id,
        )
        .first()
    )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return {
        "id": row.id,
        "planner_type": row.planner_type,
        "input": json.loads(
            row.input_json
        ),
        "result": json.loads(
            row.result_json
        ),
    }
    