import os

import pytest
from app import main
from app.config import Settings, get_settings
from fastapi.testclient import TestClient
from pydantic import AnyUrl


def get_settings_override():
    db_url = os.environ.get("DATABASE_TEST_URL")
    return Settings(
        testing=True,
        database_url=AnyUrl(db_url) if db_url else None,
    )


@pytest.fixture(scope="module")
def test_app():
    main.app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(main.app) as test_client:
        yield test_client
