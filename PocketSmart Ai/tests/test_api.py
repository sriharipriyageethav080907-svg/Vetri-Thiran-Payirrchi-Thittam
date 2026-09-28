import os


os.environ[
    "DATABASE_URL"
] = "sqlite:///./test_pocketsmart.db"


os.environ[
    "SECRET_KEY"
] = "test-secret"


from fastapi.testclient import (
    TestClient,
)

from app.main import app

from app.database import (
    init_db,
)


init_db()


client = TestClient(
    app
)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_register_and_home():

    email = (
        "test@example.com"
    )


    response = client.post(
        "/register",
        json={
            "email": email,
            "password": "password123",
        },
    )


    assert response.status_code in (
        200,
        409,
    )


    response = client.post(
        "/login",
        json={
            "email": email,
            "password": "password123",
        },
    )


    assert response.status_code == 200


    response = client.post(
        "/generate-home",
        json={
            "budget": 50000,

            "currency": "INR",

            "rooms": [
                "Living Room"
            ],

            "items": [
                {
                    "name":
                        "LED ceiling light",
                    "quantity": 2,
                }
            ],

            "style": "Modern",

            "priorities":
                "value",

            "preferred_platforms": [
                "Amazon"
            ],
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert (
        data["planner_type"]
        == "home"
    )


    assert (
        len(
            data["recommendations"]
        )
        >= 1
    )
    