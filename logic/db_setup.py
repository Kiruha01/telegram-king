import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()
#

class Player(Base):
    __tablename__ = 'Player'

    id = Column(Integer, primary_key=True)
    creator = Column(Integer, nullable=False)
    name = Column(String(127), nullable=False)

    def __str__(self):
        return self.name

    # negative_bribes = Column(Integer, nullable=False)
    # negative_hearts = Column(Integer, nullable=False)
    # negative_boys = Column(Integer, nullable=False)
    # negative_girls = Column(Integer, nullable=False)
    # negative_king = Column(Integer, nullable=False)
    # negative_patchwork = Column(Integer, nullable=False)
    #
    # positive_bribes = Column(Integer, nullable=False)
    # positive_hearts = Column(Integer, nullable=False)
    # positive_boys = Column(Integer, nullable=False)
    # positive_girls = Column(Integer, nullable=False)
    # positive_king = Column(Integer, nullable=False)
    # positive_patchwork = Column(Integer, nullable=False)


#

if os.environ.get("DEPOY"):
    engine = create_engine(f'mysql+mysqldb://kinggame:{os.environ.get("DBPASS")}@kinggame.mysql.pythonanywhere-services.com/kinggame$default')
else:
    engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)