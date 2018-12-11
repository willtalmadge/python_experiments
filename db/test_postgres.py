"""
This is an experiment for writing tests against an empty postgres database
that is instantiated with docker. This test has docker as an implicit external
dependency and will pull postgres in as a part of its setup. It will destroy
all data created as part of the testing process.

# Log

Encountered a problem with accepting passwords. Turns out an old installation
of postgres was still running and conflicting with docker. Removed it to
resolve the issue.

Used this command for test_connection to pass without exception:
docker run --name test-postgres -e POSTGRES_PASSWORD=test \
-p 5432:5432 -d postgres -c fsync-off

NOTE: fsync=off should NEVER be used in a production database, this just means
nothing is written to disk. This is a feature good for tests like in this
module. See:
https://stackoverflow.com/questions/9407442/optimise-postgresql-for-fast-testing
"""
import json

import psycopg2
import pytest
from psycopg2._psycopg import ProgrammingError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, MetaData, Table, Column, JSON

TEST_DB_NAME = 'test'


@pytest.fixture(scope='module')
def postgres_conn():
    """
    This connection is (re)used by tdb to create and remove the test database.
    """
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        host='localhost',
        password='test'
    )
    yield conn


@pytest.fixture
def teng(postgres_conn):
    """
    This fixture creates a fresh database for each unit test.
    """
    yield from teng_inner(postgres_conn)


def teng_inner(postgres_conn):
    postgres_conn.set_isolation_level(
        ISOLATION_LEVEL_AUTOCOMMIT
    )
    cur = postgres_conn.cursor()
    try:
        cur.execute(
            f'drop database {TEST_DB_NAME}'
        )
    except ProgrammingError:
        pass
    cur.execute(
        f'create database {TEST_DB_NAME}'
    )
    try:
        db_string = f"postgres://postgres:test@localhost:5432/{TEST_DB_NAME}"
        eng = create_engine(db_string)
        yield eng
        eng.dispose()
    finally:
        cur.execute(
            f'drop database {TEST_DB_NAME}'
        )


def test_engine(teng):
    """
    Test that we can connect to the test database.
    """
    teng.execute('SELECT 1')


def test_db_empty(postgres_conn):
    """
    Test that the database is empty before a test.
    """
    for eng in teng_inner(postgres_conn):
        eng.execute("CREATE TABLE test (col text)")

    for eng in teng_inner(postgres_conn):
        eng.execute("CREATE TABLE test (col text)")


def test_create_table(teng):
    meta = MetaData(teng)
    table = Table(
        'json_table', meta,
        Column('json', JSON)
    )
    with teng.connect() as conn:
        table.create()
        j = {'a': 1, 'b': 2}
        stmt = table.insert().values(
            json=json.dumps(j)
        )
        conn.execute(stmt)
        results = list(conn.execute(table.select()))
        assert j == json.loads(results[0][0])
