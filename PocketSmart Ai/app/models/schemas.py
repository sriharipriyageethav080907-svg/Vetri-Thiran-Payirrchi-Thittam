from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class RegisterRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class HomeItem(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    quantity: int = Field(
        default=1,
        ge=1,
        le=50,
    )


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    currency: str = Field(
        default="INR",
        max_length=10,
    )

    rooms: list[str] = Field(
        default_factory=lambda: [
            "Living Room"
        ]
    )

    items: list[HomeItem] = Field(
        default_factory=list
    )

    style: str = Field(
        default="Modern",
        max_length=100,
    )

    priorities: str = Field(
        default="value for money",
        max_length=500,
    )

    preferred_platforms: list[str] = Field(
        default_factory=lambda: [
            "Amazon",
            "IKEA",
        ]
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    currency: str = Field(
        default="INR",
        max_length=10,
    )

    event_type: str = Field(
        default="Birthday",
        max_length=100,
    )

    guests: int = Field(
        gt=0,
        le=10000,
    )

    venue: str = Field(
        default="Home",
        max_length=200,
    )

    city: str = Field(
        default="",
        max_length=100,
    )

    food_preferences: str = Field(
        default="Mixed",
        max_length=500,
    )

    priorities: str = Field(
        default="balanced",
        max_length=500,
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    currency: str = Field(
        default="INR",
        max_length=10,
    )

    occasion: str = Field(
        default="Wedding",
        max_length=100,
    )

    style: str = Field(
        default="Elegant",
        max_length=100,
    )

    metal: str = Field(
        default="Any",
        max_length=100,
    )

    outfit_color: str = Field(
        default="",
        max_length=100,
    )

    notes: str = Field(
        default="",
        max_length=1000,
    )


class RecommendationItem(BaseModel):

    category: str

    name: str

    description: str

    estimated_price: float = Field(
        ge=0
    )

    currency: str = "INR"

    platform: str

    search_url: str

    quantity: int = Field(
        default=1,
        ge=1,
    )

    reason: str


class RecommendationResponse(BaseModel):

    planner_type: str

    title: str

    summary: str

    budget: float

    estimated_total: float

    currency: str

    budget_status: str

    allocations: dict[str, float]

    recommendations: list[
        RecommendationItem
    ]

    tips: list[str]

    ai_generated: bool = False

    history_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )
    