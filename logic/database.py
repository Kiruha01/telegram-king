from logic.db_setup import get_manager_builder
from logic.config import State
import os


def get_manager():
    manager_name = os.environ.get('db_manager')
    if manager_name is None:
        raise Exception('DB Manager does not set.')
    manager = get_manager_builder(manager_name)(
        host=os.environ.get('db_host'),
        database=os.environ.get('db_name'),
        user=os.environ.get('db_user'),
        password=os.environ.get('db_password'),
        port=os.environ.get('db_port'),
    )
    manager.create_users_table()
    return manager


class User:
    def __init__(self, id: int, telegram_id: str, count_of_players: int):
        self.id: int = id
        self.telegram_id: str = telegram_id
        self.state: State = State.start
        self.count_of_players: int = count_of_players
        self.current_asking_player: int = 0


class Player:
    def __init__(self, id, name, nb, nh, nbs, ngs, nk, nl, np, pb, ph, pbs, pgs, pk, pl, pp):
        self.id = id
        self.name = name
        self.negative_bribes = nb
        self.negative_hearts = nh
        self.negative_boys = nbs
        self.negative_girls = ngs
        self.negative_king = nk
        self.negative_last = nl
        self.negative_patchwork = np

        self.positive_bribes = pb
        self.positive_hearts = ph
        self.positive_boys = pbs
        self.positive_girls = pgs
        self.positive_king = pk
        self.positive_last = pl
        self.positive_patchwork = pp


class Controller:
    def __init__(self):
        self.manager = get_manager()
        self.user: User = User(0, "0", 0)

    def create_user(self, telegram_id, count_of_players):
        self.manager.execute("INSERT INTO Users (telegram_id, count_of_players) VALUES ('%s', %s);" % (telegram_id, count_of_players))
        id = self.manager.execute("SELECT id FROM Users WHERE telegram_id = %s;" % telegram_id)[0][0]
        user = User(id, telegram_id, count_of_players)
        self.manager.create_players_table(telegram_id)
        return user

    def get_user(self, telegram_id: str):
        if self.user is None or self.user.telegram_id != telegram_id:
            user = self.manager.execute("SELECT "
                                        "id, state, count_of_players, current_asking_player "
                                        "FROM Users WHERE telegram_id = %s;" % telegram_id)[0]
            self.user.id = user[0]
            self.user.telegram_id = telegram_id
            self.user.state = State(user[1])
            self.user.count_of_players = user[2]
            self.user.current_asking_player = user[3]
        return self.user

    def update_user(self, user: User):
        self.manager.execute(f"UPDATE Users SET 'state' = {user.state.value}, "
                             f"current_asking_player = {user.current_asking_player} WHERE id = {user.id}")

    def create_player(self, user: User, name):
        self.manager.execute("INSERT INTO _%s (name) VALUES ('%s');" % (user.telegram_id, name))

    def set_points(self, user: User, id: int, field: str, points: int):
        self.manager.execute(f"UPDATE _{user.telegram_id} SET {field} = {points} WHERE id = {id};")

    def get_ids_players(self, user: User):
        raw = self.manager.execute(f"SELECT id FROM _{user.telegram_id};")
        players = []
        for i in raw:
            players.append(i[0])
        return players

    def get_player_by_id(self, user: User, id: int) -> Player:
        raw = self.manager.execute(f"SELECT * FROM _{user.telegram_id} WHERE id = {id}")[0]
        return Player(*raw)
