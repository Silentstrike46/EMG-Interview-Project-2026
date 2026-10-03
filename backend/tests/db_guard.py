from sqlalchemy.engine import make_url

TEST_DATABASE_SUFFIX = "_test"


class UnsafeTestDatabaseError(RuntimeError):
    pass


def assert_test_database(url: str) -> None:
    """Refuse any database whose name does not end in `_test`.

    The test suite migrates, downgrades and wipes the database it runs against,
    so pointing it at a real database by mistake must be impossible.
    """
    database = make_url(url).database
    if not database or not database.endswith(TEST_DATABASE_SUFFIX):
        raise UnsafeTestDatabaseError(
            f"Refusing to run tests against database {database!r}: "
            f"its name must end in {TEST_DATABASE_SUFFIX!r}."
        )
