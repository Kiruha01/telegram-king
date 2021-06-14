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
        # except Error as e:
        #     raise Error
        #     print(f"The error '{e}' occurred")

    def create_table(self, name):
        self.execute(f"""CREATE TABLE IF NOT EXISTS _{name} (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          {", ".join(map(lambda x: x + " INTEGER DEFAULT 0", rounds)) }
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


# class User(Base):
#     __tablename__ = 'User'
#
#     id = Column(Integer, primary_key=True)
#     telegram_id = Column(Integer, nullable=False)
#     state = Column(Integer, nullable=False)
#     count_of_players = Column(Integer, nullable=False)  # число игроков, играющих в игру
#     current_asking_player = Column(Integer, nullable=False)  # Текущий игрок, у которого спрашивают количество взяток
#
#     def set_state(self, state):
#         self.state = state.value
#
#
# if os.environ.get("DEPLOY"):
#     engine = create_engine(
#         f'mysql+mysqldb://kinggame:{os.environ.get("DBPASS")}@kinggame.mysql.pythonanywhere-services.com/kinggame$game?charset=utf8')
# else:
#     engine = create_engine('sqlite:///db.sqlite')
# Base.metadata.create_all(engine)
