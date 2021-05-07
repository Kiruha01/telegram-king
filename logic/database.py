from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import PendingRollbackError

from logic.db_setup import Player, User, Base, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


rounds = [
    'negative_bribes',
    'negative_hearts',
    'negative_boys',
    'negative_girls',
    'negative_king',
    'negative_last',
    'negative_patchwork',

    'positive_bribes',
    'positive_hearts',
    'positive_boys',
    'positive_girls',
    'positive_king',
    'positive_last',
    'positive_patchwork'
]


points_for_3 = {
    'negative_bribes': -4,
    'negative_hearts': -5,
    'negative_boys': -10,
    'negative_girls': -10,
    'negative_king': -40,
    'negative_last': -20,

    'positive_bribes': 4,
    'positive_hearts': 5,
    'positive_boys': 10,
    'positive_girls': 10,
    'positive_king': 40,
    'positive_last': 20
}

points_for_4 = {
    'negative_bribes': -2,
    'negative_hearts': -2,
    'negative_boys': -4,
    'negative_girls': -4,
    'negative_king': -16,
    'negative_last': -8,

    'positive_bribes': 2,
    'positive_hearts': 2,
    'positive_boys': 4,
    'positive_girls': 4,
    'positive_king': 16,
    'positive_last' : 8
}


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
