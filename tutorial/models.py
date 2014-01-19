import cryptacular.bcrypt

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    )

import datetime
from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    )

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relation,
    backref,
    column_property,
    synonym,
    joinedload,
    )

from sqlalchemy.types import (
    Integer,
    Unicode,
    UnicodeText,
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

def hash_password(password):
    return unicode(crypt.encode(password))


class Fav(Base):
    """
    Fav model.
    """
    __tablename__ = 'favs'
    fav_id = Column(Integer, primary_key=True)
    url = Column(Text, unique=True, index=True)

    def __init__(self, url):
        self.url = url

    @staticmethod
    def extract_favs(favs_string):
        favs = favs_string.replace(';', ' ').replace(',', ' ')
        favs = [fav.lower() for fav in favs.split()]
        favs = set(favs)

        return favs

    @classmethod
    def get_by_url(cls, fav_url):
        fav = DBSession.query(cls).filter(cls.url == fav_url)
        return fav.first()

    @classmethod
    def create_favs(cls, favs_string):
        favs_list = cls.extract_favs(favs_string)
        favs = []

        for fav_url in favs_list:
            fav = cls.get_by_url(fav_url)
            if not fav:
                fav = Fav(url=fav_url)
                DBSession.add(fav)
            favs.append(fav)

        return favs

users_favs = Table('users_favs', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('fav_id', Integer, ForeignKey('favs.fav_id'))
)

class User(Base):
    """
    Application's user model.
    """
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), unique=True)
    name = Column(Unicode(50))
    email = Column(Unicode(50))
    favs = relation(Fav, secondary=users_favs, backref='users')
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

    # @classmethod
    # def fav_counts(cls):
    #     query = DBSession.query(Fav.url, func.count('*'))
    #     return query.join('users').group_by(Fav.url) # NOT SO SURE HERE what join 'users' does


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, Authenticated, 'loggedin') ]
    def __init__(self, request):
        pass