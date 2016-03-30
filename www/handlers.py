# -*- coding: utf-8 -*-

'url handlers'

import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import User, Comment, Blog, next_id
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

@get('/api/users')
def api_get_users():
    users = yield from User.findAll(orderBy='created_at desc')
    for u in users:
        print(u)
        print(type(u))
        print(u.passwd)
        # u.passwd = "******"
    return dict(users=users)

