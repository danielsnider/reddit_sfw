import datetime
import cryptacular.bcrypt
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    )
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    )
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    synonym,
    )
from sqlalchemy.types import (
    Integer,
    Unicode,
    )


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
crypt = cryptacular.bcrypt.BCRYPTPasswordManager()


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


class Fav(Base):
    """
    Model to store user favorites
    """
    __tablename__ = 'favs'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    username = Column(Text)

    def __init__(self, url, username):
        self.url = url
        self.username = username


class User(Base):
    """
    User model
    """
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), unique=True)
    name = Column(Unicode(50))
    email = Column(Unicode(50))
    _password = Column('password', Unicode(60))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    def __init__(self, username, password, name, email):
        self.username = username
        self.name = name
        self.email = email
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def check_password(cls, username, password):
        user = cls.get_by_username(username)
        if not user:
            return False
        return crypt.check(user.password, password)


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, Authenticated, 'loggedin') ]
    def __init__(self, request):
        pass


def hash_password(password):
    return unicode(crypt.encode(password))
