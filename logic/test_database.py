def test_createTable(empty_database):
    pass


def test_insert(database_with_table):
    database_with_table.execute("""INSERT INTO _test (name, positive_bribes) VALUES ('Losha', 3);""")
    assert database_with_table.execute("SELECT * FROM _test;") == [(1, 'Losha', 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0),]


def test_select(fulfill_database):
    assert fulfill_database.execute("SELECT name FROM _test;") == [('Losha',),('Kirill',),('Vova',), ]


def test_delete(fulfill_database):
    fulfill_database.execute("DELETE FROM _test WHERE name='Losha';")
    assert fulfill_database.execute("SELECT name FROM _test;") == [('Kirill',), ('Vova',), ]


def test_update(fulfill_database):
    assert fulfill_database.execute("SELECT name, positive_bribes FROM _test WHERE name='Losha';") == [('Losha', 3), ]
    fulfill_database.execute("UPDATE _test SET positive_bribes = 10;")
    assert fulfill_database.execute("SELECT name, positive_bribes FROM _test WHERE name='Losha';") == [('Losha', 10), ]