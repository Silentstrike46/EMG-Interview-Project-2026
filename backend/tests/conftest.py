from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from db_guard import UnsafeTestDatabaseError, assert_test_database
from fastapi.testclient import TestClient

from backend.config import settings
from backend.main import app

BACKEND_DIR = Path(__file__).resolve().parents[1]


def pytest_sessionstart(session: pytest.Session) -> None:
    # Runs before any fixture or test, so nothing can connect to an unsafe
    # database before this check.
    try:
        assert_test_database(settings.database_url)
    except UnsafeTestDatabaseError as exc:
        pytest.exit(str(exc), returncode=pytest.ExitCode.USAGE_ERROR)


@pytest.fixture(scope="session", autouse=True)
def migrated_database() -> None:
    # The test database may survive between runs, so start from a clean schema.
    # Downgrading to base first also proves every migration downgrades cleanly.
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    command.downgrade(config, "base")
    command.upgrade(config, "head")


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
