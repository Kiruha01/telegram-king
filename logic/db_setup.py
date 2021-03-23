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

    negative_bribes = Column(Integer, nullable=False)
    negative_hearts = Column(Integer, nullable=False)
    negative_boys = Column(Integer, nullable=False)
    negative_girls = Column(Integer, nullable=False)
    negative_king = Column(Integer, nullable=False)
    negative_patchwork = Column(Integer, nullable=False)

    positive_bribes = Column(Integer, nullable=False)
    positive_hearts = Column(Integer, nullable=False)
    positive_boys = Column(Integer, nullable=False)
    positive_girls = Column(Integer, nullable=False)
    positive_king = Column(Integer, nullable=False)
    positive_patchwork = Column(Integer, nullable=False)


State = Enum("State", " ".join([
    'start',
    'names',

    'negative_bribes',
    'negative_hearts',
    'negative_boys',
    'negative_girls',
    'negative_king',
    'negative_patchwork',

    'positive_bribes',
    'positive_hearts',
    'positive_boys',
    'positive_girls',
    'positive_king',
    'positive_patchwork',

    'final'
]))


class User(Base):
    __tablename__ = 'Player'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)
    count_of_players = Column(Integer, nullable=False)  # число игроков, играющих в игру
    current_asking_player = Column(Integer, nullable=False)  # Текущий игрок, у которого спрашивают количество взяток


if os.environ.get("DEPOY"):
    engine = create_engine(
        f'mysql+mysqldb://kinggame:{os.environ.get("DBPASS")}@kinggame.mysql.pythonanywhere-services.com/kinggame$default')
else:
    engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)
