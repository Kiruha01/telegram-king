import os
from logic.config import rounds
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
                  telegram_id TEXT NOT NULL UNIQUE,
                  state INTEGER NOT NULL DEFAULT 0,
                  count_of_players INTEGER NOT NULL,
                  current_asking_player INTEGER NOT NULL DEFAULT 0
                );""")

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
