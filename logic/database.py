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
    def __init__(self, id: int, telegram_id: str, count_of_layers: int):
        self.id: int = id
        self.telegram_id: str = telegram_id
        self.state: State = State.start
        self.count_of_players: int = count_of_layers
        self.current_asking_player: int = 0


class Controller:
    def __init__(self):
        self.manager = get_manager()
        self.user: User = User(0, "0", 0)

    def get_user(self, telegram_id: str):
        if self.user is None or self.user.telegram_id != telegram_id:
            user = self.manager.execute("SELECT "
                                            "(id, state, count_of_players, current_asking_player) "
                                        "FROM Users WHERE telegram_id = %s;" % telegram_id)[0]
            self.user.id = user[0]
            self.user.telegram_id = telegram_id
            self.user.state = State(user[1])
            self.user.count_of_players = user[2]
            self.user.current_asking_player = user[3]
        return self.user
