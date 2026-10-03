import pytest
from db_guard import UnsafeTestDatabaseError, assert_test_database


def test_accepts_database_ending_in_test() -> None:
    """Test that a database name ending in `_test` is allowed."""
    assert_test_database("postgresql+psycopg://emg:emg@db-test:5432/emg_test")


@pytest.mark.parametrize(
    "url",
    [
        "postgresql+psycopg://emg:emg@db:5432/emg",
        "postgresql+psycopg://emg:emg@db:5432/test_emg",
        "postgresql+psycopg://emg:emg@db:5432",
    ],
    ids=["dev-database", "test-prefix-not-suffix", "no-database-name"],
)
def test_rejects_database_not_ending_in_test(url: str) -> None:
    """Test that any database name not ending in `_test` is refused."""
    with pytest.raises(UnsafeTestDatabaseError):
        assert_test_database(url)
