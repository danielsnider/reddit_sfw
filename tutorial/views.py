import urllib2
import datetime
import json
import re
import ast
import formencode
from sqlalchemy.exc import DBAPIError
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    HTTPMovedPermanently,
    )
from .models import (
    DBSession,
    Cache,
    User,
    Fav,
    )
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
    )


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def home_view(request):
    return query2_view(request) # reuse query_view route


@view_config(route_name='query1', renderer='templates/mytemplate.pt')
def query1_view(request):
    return query2_view(request) # reuse query_view route


@view_config(route_name='query2', renderer='templates/mytemplate.pt')
def query2_view(request):
    all_subreddits = "earthporn+waterporn+skyporn+spaceporn+fireporn+destructionporn+geologyporn+winterporn+autumnporn+cityporn+villageporn+abandonedporn+infrastructureporn+machineporn+militaryporn+cemeteryporn+architectureporn+carporn+gunporn+boatporn+aerialporn+F1porn+ruralporn+animalporn+botanicalporn+humanporn+adrenalineporn+climbingporn+culinaryporn+foodporn+dessertporn+agricultureporn+designporn+albumartporn+movieposterporn+adporn+geekporn+instrumentporn+macroporn+artporn+fractalporn+exposureporn+microporn+metalporn+streetartporn+historyporn+mapporn+bookporn+newsporn+quotesporn+futureporn"

    if 'minsize' not in request.matchdict:
        minsize = 0
    else:
        minsize = int(request.matchdict['minsize'])
    if 'subreddits' not in request.matchdict:
        subreddits = all_subreddits 
    else:
        subreddits = request.matchdict['subreddits']

    reddit_url = "http://www.reddit.com/r/" + subreddits + "/hot.json?limit=15"
    images = find_images(reddit_url, minsize)

    return {'images_str': dict_to_str(images), 'username': authenticated_userid(request), 'images': images, 'length': len(images)}


class RegistrationSchema(formencode.Schema):
    allow_extra_fields = True
    username = formencode.validators.PlainText(not_empty=True)
    password = formencode.validators.PlainText(not_empty=True)
    email = formencode.validators.Email(resolve_domain=False)
    name = formencode.validators.String(not_empty=True)
    password = formencode.validators.String(not_empty=True)
    confirm_password = formencode.validators.String(not_empty=True)
    chained_validators = [
        formencode.validators.FieldsMatch('password', 'confirm_password')
    ]


@view_config(permission='view', route_name='register',
             renderer='templates/user_add.pt')
def user_add(request):
    form = Form(request, schema=RegistrationSchema)

    if 'form.submitted' in request.POST and form.validate():
        session = DBSession()
        username = form.data['username']
        user = User(
            username=username,
            password=form.data['password'],
            name=form.data['name'],
            email=form.data['email']
        )
        session.add(user)
        headers = remember(request, username)
        redirect_url = request.route_url('home')
        return HTTPFound(location=redirect_url, headers=headers)

    return {
        'form': FormRenderer(form),
    }


@view_config(permission='view', route_name='user',
             renderer='templates/user.pt')
def user_view(request):
    username = request.matchdict['username']
    user = User.get_by_username(username)
    favorites = DBSession.query(Fav).filter(Fav.username==username).all()
    return {
        'username': user.username,
        'favorites': favorites,
    }


@view_config(permission='view', route_name='login', renderer='templates/login.pt')
def login_view(request):
    # came_from = request.referer.replace(request.host, "").replace("http://", "") 

    post_data = request.POST
    if 'submit' in post_data:
        login = post_data['login']
        password = post_data['password']

        if User.check_password(login, password):
            headers = remember(request, login)
            return HTTPFound(location="/", headers=headers)

    return {}


@view_config(permission='loggedin', route_name='logout')
def logout_view(request):
    request.session.invalidate()
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


@view_config(permission='loggedin', route_name='favorite')
def favorite_view(request):
    url = request.body
    username = request.session['auth.userid']
    exists = DBSession.query(Fav).filter(Fav.url==url, Fav.username==username).first()
    if not exists:
        favorite = Fav(url, username)
        DBSession.add(favorite)
    return Response('OK')


def find_images(reddit_url, minsize):
    images = []

    objects = check_cache(reddit_url)
    if objects:
        objects = ast.literal_eval(objects.data) #convert objects to list of dicts
    else:
        json_str = get_url(reddit_url)
        if json_str == None: 
            print "Error: get_url failed \n Falling back to default image"
            images = [{'domain': 'ppcdn.500px.org', 'banned_by': None, 'media_embed': {}, 'subreddit': 'VillagePorn', 'selftext_html': None, 'selftext': '', 'likes': None, 'secure_media': None, 'link_flair_text': None, 'id': '1vg203', 'secure_media_embed': {}, 'clicked': False, 'stickied': False, 'author': 'soupyhands', 'media': None, 'width': 1920, 'score': 358, 'approved_by': None, 'over_18': False, 'hidden': False, 'thumbnail': 'http://a.thumbs.redditmedia.com/7rkYTCpFYUZKiMXr.jpg', 'subreddit_id': 't5_2sm1u', 'edited': False, 'link_flair_css_class': None, 'author_flair_css_class': 'Cottage', 'downs': 20, 'saved': False, 'is_self': False, 'height': 1280, 'permalink': '/r/VillagePorn/comments/1vg203/sunset_in_the_windows_of_the_old_bergen_museum/', 'name': 't3_1vg203', 'created': 1389995666.0, 'url': 'http://ppcdn.500px.org/57985348/fedb8cc44992e05f23dbf885a013dfbca4998e11/2048.jpg', 'author_flair_text': None, 'title': 'Sunset in the windows of the old Bergen Museum, Norway [1920x1280] photo by Tore H.', 'created_utc': 1389966866.0, 'ups': 378, 'num_comments': 8, 'visited': False, 'num_reports': None, 'distinguished': None}]
            return images
        json_str = json_str.replace("\u00d7", "x") # fix unicode problem: covert multiplication symbol to x
        objects = json.loads(json_str) 
        cache(reddit_url, objects)

    # find images in reddit's JSON
    for obj in objects['data']['children']: 
        if 'data' in obj: 
            obj = obj['data']
            if 'url' in obj:
                if contains_image_file_extension(obj['url']):
                    # size = extract_image_size(obj['title'])
                    # if size:
                    #     if size[0] > minsize and size[1] > minsize:
                    #         image = obj
                    #         image['width'] = size[0]
                    #         image['height'] = size[1]
                    #         images.append(image) 
                    images.append(obj) 
    return images


def get_url(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
    except Exception as e:
        print e 
        return None
    return html


def contains_image_file_extension(string):
    img_formats = [".jpg", ".jpeg", ".gif", ".png", ".svg", ".tiff", ".bmp", ".JPG", ".JPEG", ".GIF", ".PNG", ".SVG", ".TIFF", ".BMP" ]
    if any(img_format in string for img_format in img_formats):
        return True
    else:
        return False


def extract_image_size(string):
    size = re.search(r'\d+\s*[x]\s*\d+', string)
    if size: 
        size = size.group().replace(" ", "")
        size = size.replace(" ", "")
        size = size.split("x")
        size[0] = int(size[0])
        size[1] = int(size[1])
        return size
    else:
        return None


def check_cache(url):
    try:
        data = DBSession.query(Cache).filter(Cache.url==url).first()
    except DBAPIError:
        print "Database error: \n " + conn_err_msg 
        return None 
    if data:
        delta = datetime.datetime.now() - data.datetime
        if delta.seconds > 900: # 15 minutes
            return None
        else:
            print "Cache hit!  Entry age(seconds): " + str(delta.seconds)
            return data
    

def cache(url, data):
    records = DBSession.query(Cache).filter(Cache.url==url).all()
    for record in records:
        DBSession.delete(record) #remove any duplicates just in case
    record = Cache(url, str(data))
    DBSession.add(record)

def dict_to_str(mylist):
    new_objs = []
    for obj in mylist:
        new_obj = obj
        for key, value in obj.iteritems():
            if '"' in str(value): 
                new_obj[key] = value.replace('"',r'\"')
        new_objs.append(new_obj)
    return json.dumps(new_objs).replace("'",r"\'")
