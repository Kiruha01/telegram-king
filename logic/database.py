from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logic.db_setup import Player, Base, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


def getall():
    an = ''
    for i in session.query(Player).all():
        an += i.name + '\n'
    return an


def add(name, creator):
    a = Player(name=name, creator=creator)
    session.add(a)
    session.commit()
