
import json

import pytest

from ...utils import is_prod_version
from .constants import TEST_COMPUTE_POOL, TEST_WAREHOUSE, SpcsSetupTuple, objects_to_setup


# Setup Warehouse
@pytest.fixture(scope="session")
def warehouse_setup(cursor):
    cursor.execute(f"CREATE WAREHOUSE IF NOT EXISTS {TEST_WAREHOUSE};").fetchone()
    cursor.execute(f"USE WAREHOUSE {TEST_WAREHOUSE};").fetchone()


# Setup basic objects: database, schema
@pytest.fixture(scope="session", autouse=True)
def setup_basic(connection):
    with connection.cursor() as cursor:
        # Like backup_database_schema, but scope of this fixture is session
        _database_name = cursor.execute("SELECT /* setup_basic */ CURRENT_DATABASE()").fetchone()[0]
        _schema_name = cursor.execute("SELECT /* setup_basic */ CURRENT_SCHEMA()").fetchone()[0]

        _temp_database = _database_name
        _temp_schema = _schema_name

        for db_name, db in objects_to_setup.items():
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS /* setup_basic */ {db_name} {db['params']}",
            )
            _temp_database = db_name

            cursor.execute(f"USE DATABASE /* setup_basic */ {db_name}")  # just in case it already existed
            for schema_name in db["schemas"]:
                cursor.execute(
                    f"CREATE SCHEMA IF NOT EXISTS /* setup_basic */ {schema_name}",
                )
                _temp_schema = schema_name

        cursor.execute(
            f"USE DATABASE /* setup_basic */ {_temp_database}",
        )
        cursor.execute(
            f"USE SCHEMA /* setup_basic */ {_temp_schema}",
        )

        try:
            yield
        finally:
            if _schema_name is not None:
                cursor.execute(f"USE SCHEMA /* setup_basic::reset */ {_database_name}.{_schema_name}")
            elif _database_name is not None:
                cursor.execute(f"USE DATABASE /* setup_basic::reset */ {_database_name}")
            if _temp_schema is not None:
                cursor.execute(f"DROP SCHEMA /* setup_basic::reset */ {_temp_database}.{_temp_schema}")


# Setup Compute pool by either create FAKE instance family or use CPU_X64_XS
@pytest.fixture(scope="session")
def spcs_setup(cursor, setup_basic, snowflake_version, use_role):
    # TODO: More accurate prod system detection
    if is_prod_version(snowflake_version):
        SPCS_parameters = {}
        instance_family = "CPU_X64_XS"
        cursor.execute("set snowservices_external_image_registry_allowlist = '*';").fetchone()
        cursor.execute(
            f"create compute pool if not exists {TEST_COMPUTE_POOL} "
            + f"with instance_family={instance_family} "
            + "min_nodes=1 max_nodes=5 auto_resume=true auto_suspend_secs=60;"
        ).fetchone()[0]
    else:
        SPCS_parameters = {
            "enable_snowservices": True,
            "enable_snowservices_user_facing_features": True,
        }
        instance_family = "FAKE"

        with use_role("accountadmin"):
            machine_info = cursor.execute("""CALL
                SYSTEM$SNOWSERVICES_MACHINE_IMAGE_REGISTER(
                    '{"image":"k8s_snowservices", "tag": "sometag", "registry": "localhost:5000"}'
                )""").fetchone()[0]

            machine_id = json.loads(machine_info)["machineImageId"]
            cursor.execute(f"""
                select SYSTEM$SNOWSERVICES_MACHINE_IMAGE_SET_DEFAULT('CONTROLLER', {machine_id});""").fetchone()[0]
            cursor.execute(f"""
                select SYSTEM$SNOWSERVICES_MACHINE_IMAGE_SET_DEFAULT('WORKER', {machine_id});""").fetchone()[0]

            for k, v in SPCS_parameters.items():
                cursor.execute(f"alter account set {k}={v}").fetchone()[0]

        with use_role("sysadmin"):
            cursor.execute(f"call system$snowservices_create_instance_type('{instance_family}');").fetchone()[0]

        cursor.execute(
            f"create compute pool if not exists {TEST_COMPUTE_POOL} "
            + f"with instance_family={instance_family} "
            + "min_nodes=1 max_nodes=1 auto_resume=true auto_suspend_secs=60;"
        ).fetchone()[0]


    try:
        yield SpcsSetupTuple(instance_family, TEST_COMPUTE_POOL)
    finally:
        if SPCS_parameters:
            with use_role("accountadmin"):
                for k in SPCS_parameters.keys():
                    cursor.execute(f"alter account unset {k}").fetchone()[0]

