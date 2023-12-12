import json
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from telegram import Bot

from npb.app import app

client = TestClient(app)

TEST_SECRET_TOKEN = "test"


bad_token = {"x-telegram-bot-api-secret-token": "somebadtoken"}
good_token = {"x-telegram-bot-api-secret-token": TEST_SECRET_TOKEN}


def test_get_main_not_allowed():
    response = client.get("/")
    assert response.status_code == 405


def test_post_without_secret_token():
    response = client.post("/", json=json.load(open("tests/update1.json")))
    assert response.json() == {"detail": "Wrong or missing secret token"}
    assert response.status_code == 401


@patch("npb.tgapp.tg_app")
def test_post_with_bad_secret_token(mock_tg_app):
    response = client.post(
        "/", json=json.load(open("tests/update1.json")), headers=bad_token
    )
    assert response.json() == {"detail": "Wrong or missing secret token"}
    assert response.status_code == 401


@patch("npb.app.tg_app")
def test_post_with_good_secret_token(mock_tg_app):
    mock_tg_app.bot = Bot("token")
    mock_tg_app.initialize = AsyncMock()
    mock_tg_app.process_update = AsyncMock()
    mock_tg_app.shutdown = AsyncMock()
    response = client.post(
        "/", json=json.load(open("tests/update1.json")), headers=good_token
    )
    assert response.json() == {"status": "ok"}
    assert response.status_code == 200


@patch("npb.app.tg_app")
def test_post_with_bad_data(mock_tg_app):
    mock_tg_app.bot = Bot("token")
    mock_tg_app.initialize = AsyncMock()
    mock_tg_app.process_update = AsyncMock()
    mock_tg_app.shutdown = AsyncMock()
    response = client.post("/", json={"data": "nodata"}, headers=good_token)
    assert response.json() == {"detail": "Cannot serialize Telegram Update"}
    assert response.status_code == 400
