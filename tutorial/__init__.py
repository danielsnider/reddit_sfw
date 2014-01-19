from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig


from .models import (
    DBSession,
    # Base,
    RootFactory,
    )

def main(global_config, **settings): 
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    session_factory = UnencryptedCookieSessionFactoryConfig(
        settings['session.secret']
        )

    authn_policy = SessionAuthenticationPolicy()
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        root_factory=RootFactory,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        session_factory=session_factory
        )

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include(addroutes)
    config.scan()

    return config.make_wsgi_app()

def addroutes(config):
    # broken out of main() so it can be used by unit tests
    config.add_route('home', '/')
    config.add_route('query1', '/r/{subreddits}')
    config.add_route('query2', '/r/{subreddits}?minsize={minsize}')
    config.add_route('user', '/users/{username}')
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('about', '/about')
    
