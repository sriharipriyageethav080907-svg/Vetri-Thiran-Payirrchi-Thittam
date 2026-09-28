import json

from typing import Any, Optional

from google import genai
from google.genai import types

from ..config import get_settings

from .prompts import (
    build_home_prompt,
    build_party_prompt,
    build_jewelry_prompt,
)


def _extract_json(
    text: str,
) -> dict[str, Any]:

    text = text.strip()

    if text.startswith("```"):

        text = text.strip("`")

        if text.startswith("json"):
            text = text[4:]

    start = text.find("{")
    end = text.rfind("}")

    if start < 0 or end <= start:
        raise ValueError(
            "Gemini did not return a JSON object"
        )

    return json.loads(
        text[start:end + 1]
    )


def _normalize(
    result: dict,
    planner: str,
    budget: float,
    currency: str,
) -> dict:

    result.setdefault(
        "title",
        f"{planner.title()} Plan",
    )

    result.setdefault(
        "summary",
        "AI-generated budget recommendations.",
    )

    result.setdefault(
        "estimated_total",
        0,
    )

    result.setdefault(
        "budget_status",
        "within budget",
    )

    result.setdefault(
        "allocations",
        {},
    )

    result.setdefault(
        "recommendations",
        [],
    )

    result.setdefault(
        "tips",
        [],
    )

    for item in result[
        "recommendations"
    ]:

        item.setdefault(
            "category",
            "General",
        )

        item.setdefault(
            "description",
            "",
        )

        item.setdefault(
            "estimated_price",
            0,
        )

        item.setdefault(
            "currency",
            currency,
        )

        item.setdefault(
            "platform",
            "Search",
        )

        item.setdefault(
            "search_url",
            "",
        )

        item.setdefault(
            "quantity",
            1,
        )

        item.setdefault(
            "reason",
            "",
        )

    result["budget"] = budget
    result["currency"] = currency
    result["ai_generated"] = True
    result["planner_type"] = planner

    return result


async def generate(
    planner: str,
    data: dict,
    image_bytes: Optional[
        bytes
    ] = None,
    image_mime: Optional[
        str
    ] = None,
) -> Optional[dict]:

    settings = get_settings()

    if not settings.gemini_api_key:
        return None

    try:

        client = genai.Client(
            api_key=settings.gemini_api_key
        )

        if planner == "home":

            prompt = build_home_prompt(
                data
            )

        elif planner == "party":

            prompt = build_party_prompt(
                data
            )

        else:

            note = (
                "No outfit image was supplied."
            )

            if image_bytes:

                note = (
                    "An outfit image is attached. "
                    "Analyze visible colors, "
                    "silhouette and styling only."
                )

            prompt = build_jewelry_prompt(
                data,
                note,
            )

        contents: list[Any] = [
            prompt
        ]

        if image_bytes:

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=(
                        image_mime
                        or "image/jpeg"
                    ),
                )
            )

        response = (
            await client.aio.models.generate_content(
                model=settings.gemini_model,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.35,
                    response_mime_type="application/json",
                ),
            )
        )

        return _normalize(
            _extract_json(
                response.text
            ),
            planner,
            data["budget"],
            data["currency"],
        )

    except Exception:
        return None
        