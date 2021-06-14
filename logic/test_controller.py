from logic.database import Player, User, Controller, State
from logic.db_setup import SQLiteManager


def test_controller(controller):
    assert type(controller.manager) is SQLiteManager


def test_createUser(controller: Controller, empty_database: SQLiteManager, user: User):
    controller.create_user(user.telegram_id, user.count_of_players)
    assert empty_database.execute("SELECT * FROM Users;") == [(user.id, user.telegram_id, user.state.value,
                                                               user.count_of_players, user.current_asking_player),]
    assert empty_database.execute(f"SELECT * FROM _{user.telegram_id};") == []


def test_createPlayer(controller: Controller, empty_database: SQLiteManager, user: User):
    controller.create_user(user.telegram_id, user.count_of_players)
    controller.create_player(user, 'Ivan')
    assert empty_database.execute(f"SELECT * FROM _{user.telegram_id};") == [(1, 'Ivan', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]


def test_setPointsToUsers(controller_with_two_players: Controller, empty_database: SQLiteManager, user: User):
    assert empty_database.execute(f"SELECT * FROM _{user.telegram_id} WHERE id = 1;") == [
        (1, 'Ivan', -42, 0, 0, 0, 0, 0, -420, 0, 0, 0, 0, 0, 0, 0)]
    assert empty_database.execute(f"SELECT * FROM _{user.telegram_id} WHERE id = 2;") == [
        (2, 'Vasya', 0, 0, 0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0, 0)]


def test_getPlayerById(controller_with_two_players: Controller, user: User):
    user2 = User(2, '213', 3)
    controller_with_two_players.create_user(user2.telegram_id, user2.count_of_players)
    controller_with_two_players.create_player(user2, "Olga")
    assert controller_with_two_players.get_ids_players(user) == [1, 2]
    assert controller_with_two_players.get_ids_players(user2) == [1,]


def test_getUserById(controller_with_two_players: Controller, user: User):
    player = controller_with_two_players.get_player_by_id(user, 1)
    assert player.name == "Ivan" and \
        player.negative_bribes == -42 and \
        player.negative_patchwork == -420


def test_optimize_getUser(controller_with_two_players: Controller, user: User):
    u1 = controller_with_two_players.get_user(user.telegram_id)
    u2 = controller_with_two_players.get_user(user.telegram_id)

    assert id(u1) == id(u2)


def test_updateUser(controller_with_two_players: Controller, user: User):
    user.state = State.positive_bribes
    user.current_asking_player = 2
    controller_with_two_players.update_user(user)
    new_user = controller_with_two_players.get_user(user.telegram_id)
    assert user.id == new_user.id
    assert user.state == new_user.state
    assert user.current_asking_player == new_user.current_asking_player
