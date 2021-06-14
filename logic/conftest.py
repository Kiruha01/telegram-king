import pytest
import os
import logic.db_setup as db

from logic.database import Controller, User


@pytest.fixture(params=[db.SQLiteManager, ])
def empty_database(request):
    c = request.param('temp.sqlite')
    return c


@pytest.fixture()
def database_with_table(empty_database):
    empty_database.create_players_table("test")
    return empty_database


@pytest.fixture()
def fulfill_database(database_with_table):
    c = database_with_table
    c.execute("""
    INSERT INTO _test (name, positive_bribes) VALUES ('Losha', 3);
    INSERT INTO _test (name, negative_bribes) VALUES ('Kirill', -5);
    INSERT INTO _test (name, positive_bribes, positive_patchwork) VALUES ('Vova', 3, 45);
    """)

    return c


@pytest.fixture()
def controller():
    return Controller()


@pytest.fixture()
def controller_with_two_players(controller, user):
    controller.create_user(user.telegram_id, user.count_of_players)
    controller.create_player(user, 'Ivan')
    controller.create_player(user, 'Vasya')
    return controller


@pytest.fixture()
def controller_with_two_players2(user, controller_with_two_players):
    controller_with_two_players.set_points(user, 1, 'negative_bribes', -42)
    controller_with_two_players.set_points(user, 1, 'negative_patchwork', -420)
    controller_with_two_players.set_points(user, 2, 'positive_bribes', 50)
    return controller_with_two_players


@pytest.fixture()
def user():
    return User(1, '123', 4)

@pytest.fixture(scope="function", autouse=True)
def setup(request):
    try:
        open('temp.sqlite', 'x')
    except:
        pass
    request.addfinalizer(teardown)


def teardown():
    os.remove('temp.sqlite')