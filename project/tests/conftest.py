import os

import pytest
from app.config import Settings, get_settings
from app.main import create_application
from fastapi.testclient import TestClient
from pydantic import AnyUrl
from tortoise.contrib.fastapi import register_tortoise


def get_settings_override():
    db_url = os.environ.get("DATABASE_TEST_URL")
    return Settings(
        testing=True,
        database_url=AnyUrl(db_url) if db_url else None,
    )


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client
