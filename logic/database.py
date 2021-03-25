from sqlalchemy.orm import sessionmaker

from logic.db_setup import Player, User, Base, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


class get_user(object):
    def __new__(cls, telegram_id) -> User:
        if (hasattr(cls, 'user') and (cls.user is not None) and cls.user.telegram_id != telegram_id) or not hasattr(cls,
                                                                                                                    'user'):
            cls.user = session.query(User).filter_by(telegram_id=telegram_id).first()
        return cls.user


def push(obj):
    try:
        session.add(obj)
    except:
        pass
    session.commit()


def get_players(creator_id):
    return session.query(Player).filter_by(creator=creator_id)


# TODO: Удалить после создания всех шагов бота
def del_all_players():
    players = session.query(Player).all()
    for i in players:
        session.delete(i)
    session.commit()
