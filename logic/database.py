from sqlalchemy.orm import sessionmaker

from logic.db_setup import Player, User, Base, engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


class get_user(object):
    def __new__(cls, telegram_id) -> User:
        if (hasattr(cls, 'user') and cls.user.telegram_id != telegram_id) or not hasattr(cls, 'user'):
            cls.user = session.query(User).filter_by(telegram_id=telegram_id).first()
        return cls.user
