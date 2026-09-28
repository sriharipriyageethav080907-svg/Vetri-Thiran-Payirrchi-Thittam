import json

from typing import Optional

from sqlalchemy.orm import Session

from ..models.db_models import (
    RecommendationHistory,
)

from .gemini import generate

from .fallback import (
    home_fallback,
    party_fallback,
    jewelry_fallback,
)


async def make_recommendation(
    db: Session,
    user_id: int,
    planner: str,
    data: dict,
    image_bytes: Optional[
        bytes
    ] = None,
    image_mime: Optional[
        str
    ] = None,
):

    result = await generate(
        planner,
        data,
        image_bytes,
        image_mime,
    )

    if (
        result is None
        or not result.get(
            "recommendations"
        )
    ):

        if planner == "home":

            result = home_fallback(
                data
            )

        elif planner == "party":

            result = party_fallback(
                data
            )

        else:

            result = jewelry_fallback(
                data,
                image_supplied=bool(
                    image_bytes
                ),
            )

        result["ai_generated"] = False

        result["planner_type"] = planner

        result["budget"] = data["budget"]

        result["currency"] = data[
            "currency"
        ]

    history = RecommendationHistory(
        user_id=user_id,
        planner_type=planner,
        input_json=json.dumps(
            data,
            ensure_ascii=False,
        ),
        result_json=json.dumps(
            result,
            ensure_ascii=False,
        ),
    )

    db.add(history)

    db.commit()

    db.refresh(history)

    result["history_id"] = history.id

    return result
    