"""
This is an experiment for writing tests against an empty postgres database
that is instantiated with docker. This test has docker as an external
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

import psycopg2
import pytest
from psycopg2._psycopg import ProgrammingError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql.ddl import CreateTable

from db_unit.docker_postgres_setup import (
    ensure_posgres_container_is_up,
    TEST_DB_NAME
)


@pytest.fixture(scope='module')
def postgres_conn():
    """
    This connection is (re)used by teng to create and remove the test database.
    """

    # This fixture has module scope so we only do this costly docker operation
    # once per test run, not once per unit test.
    ensure_posgres_container_is_up()

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
    This fixture creates a fresh database for each unit test. After the test
    using this fixture completes it will remove the database. This ensures that
    each unit test starts with an empty database to test against.
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
    Verify that teng fixture cleans up the database after each test. We can't
    call a pytest fixture directly so we call an inner function that does the
    work.
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
    table.create()


def test_insert_into_table(teng):
    meta = MetaData(teng)
    table = Table(
        'json_table', meta,
        Column('json', JSON)
    )
    table.create()
    with teng.connect() as conn:
        j = {'a': 1, 'b': 2}
        stmt = table.insert().values(
            json=j
        )
        conn.execute(stmt)
        results = list(conn.execute(table.select()))
        assert j == results[0][0]


def test_json_query(teng):
    meta = MetaData(teng)
    table = Table(
        'json_table', meta,
        Column('doc', JSON)
    )
    table.create()
    with teng.connect() as conn:
        j = {'a': 1, 'b': 2}
        stmt = table.insert().values(
            doc=j
        )
        conn.execute(stmt)
        stmt = table.insert().values(
            doc={'a': 2, 'b': 3}
        )
        conn.execute(stmt)
        results = list(conn.execute(
            table.select().where(
                # The effect of astext seems to be to lift '->' to '->>'
                table.c.doc['a'].astext.cast(Integer) == 1
            )
        ))
        assert j == results[0][0]


def test_serial_column(teng):
    """
    Test that the following method creates an automatically incrementing
    primary key column.
    """
    meta = MetaData(teng)
    table = Table(
        'serial_table', meta,
        # autoincrement=True not necessary for postgres to create a SERIAL
        # column
        Column('id', Integer, primary_key=True)
    )
    assert 'SERIAL' in str(CreateTable(table).compile(teng))
    table.create()
    with teng.connect() as conn:
        conn.execute(table.insert())
        conn.execute(table.insert())
        results = conn.execute(table.select())
        assert [
                   (1,),
                   (2,)
               ] == list(results)


def test_sequence(teng):
    """
    Create and consume a postgres sequence.
    """
    with teng.connect() as conn:
        conn.execute(
            'create sequence id'
        )

        result = conn.execute(
            "select nextval('id'), nextval('id')"
        )
        assert [(1, 2)] == list(result)
