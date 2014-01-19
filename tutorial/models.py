from pyramid.security import (
    Allow,
    Everyone,
    )

import datetime
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Cache(Base):
    """ The SQLAlchemy declarative model class for a Cache object. """
    __tablename__ = 'cache'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    data = Column(Text)
    datetime = Column(DateTime)

    def __init__(self, url, data):
        self.url = url
        self.data = data
        self.datetime = datetime.datetime.now()

