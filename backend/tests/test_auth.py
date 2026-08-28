import pytest


@pytest.mark.asyncio
async def test_signup_creates_user(client, user_payload):
    response = await client.post("/auth/signup", json=user_payload)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == user_payload["email"]
    assert "hashed_password" not in body


@pytest.mark.asyncio
async def test_signup_rejects_duplicate_email(client, user_payload):
    await client.post("/auth/signup", json=user_payload)
    response = await client.post("/auth/signup", json=user_payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_with_correct_credentials_returns_token(client, user_payload):
    await client.post("/auth/signup", json=user_payload)

    response = await client.post(
        "/auth/login",
        data={"username": user_payload["email"], "password": user_payload["password"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


@pytest.mark.asyncio
async def test_login_with_wrong_password_rejected(client, user_payload):
    await client.post("/auth/signup", json=user_payload)

    response = await client.post(
        "/auth/login",
        data={"username": user_payload["email"], "password": "wrong-password"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_valid_token(client, user_payload):
    await client.post("/auth/signup", json=user_payload)
    login_resp = await client.post(
        "/auth/login",
        data={"username": user_payload["email"], "password": user_payload["password"]},
    )
    token = login_resp.json()["access_token"]

    response = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == user_payload["email"]


@pytest.mark.asyncio
async def test_me_rejects_missing_token(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401
