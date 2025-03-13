import copy
import pytest
import sqlite3
from cpc.repositories.user import USER_REPOSITORIES
from cpc.repositories.asset import ASSET_REPOSITORIES
from cpc.repositories.favorite import FAVORITE_REPOSITORIES
from cpc.common.const import INIT_USER_DATA
from cpc.database.dml.init import init as INITIALIZE_SQL


# ============================================================
# use in tests/services/
# ============================================================
@pytest.fixture(scope="function", params=[INIT_USER_DATA])
def test_user(request):
    test_user = copy.deepcopy(request.param)
    test_user["id"] = 1
    return test_user


# ============================================================
# use in tests/repositoires/
# ============================================================
@pytest.fixture(scope="function", params=["user", "favorite", "asset"])
def db_connection(request):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    if request.param == "user":
        cursor.execute(INITIALIZE_SQL.USER_TABLE_SQL)
        cursor.execute(INITIALIZE_SQL.FAVORITE_TABLE_SQL)
        cursor.execute(INITIALIZE_SQL.ASSET_TABLE_SQL)
    elif request.param == "favorite":
        cursor.execute(INITIALIZE_SQL.FAVORITE_TABLE_SQL)
    elif request.param == "asset":
        cursor.execute(INITIALIZE_SQL.ASSET_TABLE_SQL)

    conn.commit()
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def init_repository(db_connection, request):
    if request.param == "user":
        return USER_REPOSITORIES(db_connection)
    elif request.param == "favorite":
        return FAVORITE_REPOSITORIES(db_connection)
    elif request.param == "asset":
        return ASSET_REPOSITORIES(db_connection)
