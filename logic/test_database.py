import pytest
import os
import logic.db_setup as db


@pytest.fixture(params=[db.SQLiteManager, ])
def empty_database(request):
    c = request.param('temp.sqlite')
    c.create_players_table("test")
    return c


@pytest.fixture()
def fulfill_database(empty_database):
    c = empty_database
    c.execute("""
    INSERT INTO _test (name, positive_bribes) VALUES ('Losha', 3);
    INSERT INTO _test (name, negative_bribes) VALUES ('Kirill', -5);
    INSERT INTO _test (name, positive_bribes, positive_patchwork) VALUES ('Vova', 3, 45);
    """)

    return c


def setup():
    try:
        open('temp.sqlite', 'x')
    except:
        pass


def teardown():
    os.remove('temp.sqlite')


def test_createTable(empty_database):
    pass


def test_insert(empty_database):
    empty_database.execute("""INSERT INTO _test (name, positive_bribes) VALUES ('Losha', 3);""")
    assert empty_database.execute("SELECT * FROM _test;") == [(1, 'Losha', 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0),]


def test_select(fulfill_database):
    assert fulfill_database.execute("SELECT name FROM _test;") == [('Losha',),('Kirill',),('Vova',), ]


def test_delete(fulfill_database):
    fulfill_database.execute("DELETE FROM _test WHERE name='Losha';")
    assert fulfill_database.execute("SELECT name FROM _test;") == [('Kirill',), ('Vova',), ]


def test_update(fulfill_database):
    assert fulfill_database.execute("SELECT name, positive_bribes FROM _test WHERE name='Losha';") == [('Losha', 3), ]
    fulfill_database.execute("UPDATE _test SET positive_bribes = 10;")
    assert fulfill_database.execute("SELECT name, positive_bribes FROM _test WHERE name='Losha';") == [('Losha', 10), ]