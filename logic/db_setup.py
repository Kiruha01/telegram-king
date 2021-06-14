import os
from logic.config import rounds
from enum import Enum
import sqlite3
from sqlite3 import Warning


class SQLiteManager:
    def __init__(self, host, *args, **kwargs):
        self.core = "sqlite"
        self.connection = sqlite3.connect(host)

    def execute(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            r = cursor.execute(query)
        except Warning:
            r = cursor.executescript(query)
        self.connection.commit()
        print("Query executed successfully")
        return r.fetchall()

    def create_players_table(self, name):
        self.execute(f"""CREATE TABLE IF NOT EXISTS {name} (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          {", ".join(map(lambda x: x + " INTEGER DEFAULT 0", rounds)) }
        );""")

    def create_users_table(self):
        self.execute(f"""CREATE TABLE IF NOT EXISTS Users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  telegram_id TEXT NOT NULL,
                  state INTEGER NOT NULL DEFAULT 0,
                  count_of_players INTEGER NOT NULL,
                  current_asking_player INTEGER NOT NULL DEFAULT 0
                );""")



NUM_OF_ROUNDS = 6


class State(Enum):
    start = 0
    names = 1

    negative_bribes = 2
    negative_hearts = 3
    negative_boys = 4
    negative_girls = 5
    negative_king = 6
    negative_last = 7
    negative_patchwork = 8

    positive_bribes = 9
    positive_hearts = 10
    positive_boys = 11
    positive_girls = 12
    positive_king = 13
    positive_last = 14
    positive_patchwork = 15

    final = 16

# env:
#     db_manager: sqlite
#     db_host: db.sqlite
#     db_port: 232
#     db_name: tutor
#     db_user: user
#     db_password: ssfdsgrf


def get_manager_builder(name):
    if name == 'sqlite':
        return SQLiteManager
    else:
        raise Exception("Manager does not exist.")


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
