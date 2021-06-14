from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import PendingRollbackError

from logic.db_setup import Player, User, Base, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


class get_user(object):
    def __new__(cls, telegram_id) -> User:
        if (hasattr(cls, 'user') and (cls.user is not None) and cls.user.telegram_id != telegram_id) or not hasattr(cls, 'user'):
            try:
                cls.user = session.query(User).filter_by(telegram_id=telegram_id).first()
            except PendingRollbackError:
                session.rollback()
        return cls.user


def add(obj):
    try:
        session.add(obj)
    except PendingRollbackError:
        session.rollback()


def commit():
    try:
        session.commit()
    except PendingRollbackError:
        session.rollback()


def get_players(creator_id):
    try:
        return session.query(Player).filter_by(creator=creator_id)
    except PendingRollbackError:
        session.rollback()



def del_players_by_creator(creator):
    try:
        players = session.query(Player).filter_by(creator=creator)
        for i in players:
            session.delete(i)
        session.commit()
    except PendingRollbackError:
        session.rollback()
