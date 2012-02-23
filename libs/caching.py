#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from functools import wraps
from flask import request
import pylibmc


mc = pylibmc.Client(
    servers=[os.environ.get('MEMCACHE_SERVERS', '127.0.0.1')],
    username=os.environ.get('MEMCACHE_USERNAME', None),
    password=os.environ.get('MEMCACHE_PASSWORD', None),
    binary=True
)


def cached(timeout, cache_key):
    """
    Oh hai I iz a wonderful decorator who checks the cache and return it
    otherwise execute dat parent function and put it into the cache. umad
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            rv = mc.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            mc.set(cache_key, rv, timeout)
            return rv
        return decorated_function
    return decorator