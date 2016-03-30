# -*- coding: utf-8 -*-

'url handlers'

import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import User, Comment, Blog, next_id
from aiohttp import web
from config import configs
from apis import APIValueError, APIResourceNotFoundError, APIPermissionError

COOKIE_NAME = 'Uly'

'''
@get('/')
@asyncio.coroutine
def index(request):
    users = yield from User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }
    '''
@get('/')
@asyncio.coroutine
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summay=summary, created_at=time.time() - 120),
        Blog(id='2', name='Something New', summay=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summay=summary, created_at=time.time() - 7200),
    ]

    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }
'''
@get('/api/users')
def api_get_users():
    users = yield from User.findAll(orderBy='created_at desc')
    for u in users:
        print(u)
        print(type(u))
        print(u.passwd)
        # u.passwd = "******"
    return dict(users=users)
'''
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = yield from User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIValueError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
                 image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    yield from user.save()

    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    # I will finish user2cookie function later
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r
