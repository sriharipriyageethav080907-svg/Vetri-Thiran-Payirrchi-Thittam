from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )

    email = Column(
        String(320),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    recommendations = relationship(
        "RecommendationHistory",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class RecommendationHistory(Base):

    __tablename__ = "recommendation_history"

    id = Column(
        Integer,
        primary_key=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    planner_type = Column(
        String(50),
        nullable=False,
        index=True,
    )

    input_json = Column(
        Text,
        nullable=False,
    )

    result_json = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="recommendations",
    )
    