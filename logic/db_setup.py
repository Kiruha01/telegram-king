import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from enum import Enum

Base = declarative_base()


class Player(Base):
    __tablename__ = 'Player'

    id = Column(Integer, primary_key=True)
    creator = Column(Integer, nullable=False)
    name = Column(String(127), nullable=False)

    negative_bribes = Column(Integer, nullable=False, default=0)
    negative_hearts = Column(Integer, nullable=False, default=0)
    negative_boys = Column(Integer, nullable=False, default=0)
    negative_girls = Column(Integer, nullable=False, default=0)
    negative_king = Column(Integer, nullable=False, default=0)
    negative_last = Column(Integer, nullable=False, default=0)
    negative_patchwork = Column(Integer, nullable=False, default=0)

    positive_bribes = Column(Integer, nullable=False, default=0)
    positive_hearts = Column(Integer, nullable=False, default=0)
    positive_boys = Column(Integer, nullable=False, default=0)
    positive_girls = Column(Integer, nullable=False, default=0)
    positive_king = Column(Integer, nullable=False, default=0)
    positive_last = Column(Integer, nullable=False, default=0)
    positive_patchwork = Column(Integer, nullable=False, default=0)

    def __str__(self):
        return self.name


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


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)
    count_of_players = Column(Integer, nullable=False)  # число игроков, играющих в игру
    current_asking_player = Column(Integer, nullable=False)  # Текущий игрок, у которого спрашивают количество взяток

    def set_state(self, state):
        self.state = state.value


if os.environ.get("DEPLOY"):
    engine = create_engine(
        f'mysql+mysqldb://kinggame:{os.environ.get("DBPASS")}@kinggame.mysql.pythonanywhere-services.com/kinggame$game?charset=utf8')
else:
    engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)
