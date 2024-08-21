import pytest


@pytest.fixture
def backup_database_schema(connection):
    """Reset the current database and schema after a test is complete.

    These 2 resources go hand-in-hand, so they should be backed up together.
    This fixture should be used when a database, or schema is created,
    or used in a test.
    """
    with connection.cursor() as cursor:
        database_name = cursor.execute("SELECT /* backup_database_schema */ CURRENT_DATABASE()").fetchone()[0]
        schema_name = cursor.execute("SELECT /* backup_database_schema */ CURRENT_SCHEMA()").fetchone()[0]
        try:
            yield
        finally:
            if schema_name is not None:
                cursor.execute(f"USE SCHEMA /* backup_database_schema::reset */ {database_name}.{schema_name}")
            elif database_name is not None:
                cursor.execute(f"USE DATABASE /* backup_database_schema::reset */ {database_name}")


@pytest.fixture
def backup_warehouse(connection):
    """Reset the current warehouse after a test is complete.

    This fixture should be used when a warehouse is created, or used in a test.
    """
    with connection.cursor() as cursor:
        warehouse_name = cursor.execute("SELECT /* backup_warehouse */ CURRENT_WAREHOUSE()").fetchone()[0]
        try:
            yield
        finally:
            if warehouse_name is not None:
                cursor.execute(f"USE WAREHOUSE /* backup_warehouse::reset */ {warehouse_name};")

