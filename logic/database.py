from sqlalchemy.orm import sessionmaker

from logic.db_setup import Player, User, Base, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


points_for_3 = {
    'negative_bribes': -2,
    'negative_hearts': -2,
    'negative_boys': -4,
    'negative_girls': -4,
    'negative_king': -16,

    'positive_bribes': 2,
    'positive_hearts': 2,
    'positive_boys': 4,
    'positive_girls': 4,
    'positive_king': 16
}

points_for_4 = {
    'negative_bribes': -4,
    'negative_hearts': -4,
    'negative_boys': -10,
    'negative_girls': -10,
    'negative_king': -40,

    'positive_bribes': 4,
    'positive_hearts': 4,
    'positive_boys': 10,
    'positive_girls': 10,
    'positive_king': 40
}

class get_user(object):
    def __new__(cls, telegram_id) -> User:
        if (hasattr(cls, 'user') and (cls.user is not None) and cls.user.telegram_id != telegram_id) or not hasattr(cls, 'user'):
            cls.user = session.query(User).filter_by(telegram_id=telegram_id).first()
        return cls.user


def add(obj):
    session.add(obj)

def commit():
    session.commit()


def get_players(creator_id):
    return session.query(Player).filter_by(creator=creator_id)


# TODO: Удалить после создания всех шагов бота
def del_all_players():
    players = session.query(Player).all()
    for i in players:
        session.delete(i)
    session.commit()
