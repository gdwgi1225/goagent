#!/usr/bin/env python
# coding:utf-8

__version__ = '3.1.2'
__password__ = '123456'
__hostsdeny__ = ()  # __hostsdeny__ = ('.youtube.com', '.youku.com')
__content_type__ = 'image/gif'
__timeout__ = 20


import sys
import re
import itertools
import functools
import logging
import string
import urlparse
import httplib
import struct
import zlib


def message_html(title, banner, detail=''):
    MESSAGE_TEMPLATE = '''
    <html><head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <title>$title</title>
    <style><!--
    body {font-family: arial,sans-serif}
    div.nav {margin-top: 1ex}
    div.nav A {font-size: 10pt; font-family: arial,sans-serif}
    span.nav {font-size: 10pt; font-family: arial,sans-serif; font-weight: bold}
    div.nav A,span.big {font-size: 12pt; color: #0000cc}
    div.nav A {font-size: 10pt; color: black}
    A.l:link {color: #6f6f6f}
    A.u:link {color: green}
    //--></style>
    </head>
    <body text=#000000 bgcolor=#ffffff>
    <table border=0 cellpadding=2 cellspacing=0 width=100%>
    <tr><td bgcolor=#3366cc><font face=arial,sans-serif color=#ffffff><b>Message</b></td></tr>
    <tr><td> </td></tr></table>
    <blockquote>
    <H1>$banner</H1>
    $detail
    <p>
    </blockquote>
    <table width=100% cellpadding=0 cellspacing=0><tr><td bgcolor=#3366cc><img alt="" width=1 height=4></td></tr></table>
    </body></html>
    '''
    return string.Template(MESSAGE_TEMPLATE).substitute(title=title, banner=banner, detail=detail)


class XORCipher(object):
    """XOR Cipher Class"""
    def __init__(self, key):
        assert isinstance(key, basestring) and key
        self.__key_gen = itertools.cycle([ord(x) for x in key]).next

    def encrypt(self, data):
        return ''.join(chr(ord(x) ^ self.__key_gen()) for x in data)


def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        start_response('302 Found', [('Location', 'https://www.google.com')])
        raise StopIteration

    wsgi_input = environ['wsgi.input']
    input_data = wsgi_input.read(int(environ.get('CONTENT_LENGTH') or -1))

    metadata_length, = struct.unpack('!h', input_data[:2])
    metadata = zlib.decompress(input_data[2:2+metadata_length], -zlib.MAX_WBITS)
    payload = input_data[2+metadata_length:]
    headers = dict(x.split(':', 1) for x in metadata.splitlines() if x)
    method = headers.pop('G-Method')
    url = headers.pop('G-Url')
    urlparts = urlparse.urlparse(url)

    kwargs = {}
    any(kwargs.__setitem__(x[2:].lower(), headers.pop(x)) for x in headers.keys() if x.startswith('G-'))

    if 'Content-Encoding' in headers:
        if headers['Content-Encoding'] == 'deflate':
            payload = zlib.decompress(payload, -zlib.MAX_WBITS)
            headers['Content-Length'] = str(len(payload))
            del headers['Content-Encoding']

    cipher = XORCipher(__password__[0])
    normcookie = functools.partial(re.compile(', ([^ =]+(?:=|$))').sub, '\\r\\nSet-Cookie: \\1')

    if __password__ and __password__ != kwargs.get('password'):
        start_response('403 Forbidden', [('Content-Type', 'text/html')])
        yield message_html('403 Wrong Password', 'Wrong Password(%s)' % kwargs.get('password'), detail='please edit proxy.ini')
        raise StopIteration

    if __hostsdeny__ and urlparts.netloc.endswith(__hostsdeny__):
        start_response('200 OK', [('Content-Type', __content_type__)])
        yield cipher.encrypt('HTTP/1.1 403 Forbidden\r\nContent-type: text/html\r\n\r\n')
        yield cipher.encrypt(message_html('403 Forbidden Host', 'Hosts Deny(%s)' % urlparts.netloc, detail='url=%r' % url))
        raise StopIteration

    header_sent = False
    try:
        timeout = int(kwargs.get('timeout') or __timeout__)
        ConnectionType = httplib.HTTPSConnection if urlparts.scheme == 'https' else httplib.HTTPConnection
        conn = ConnectionType(urlparts.netloc, timeout=timeout)
        path = urlparts.path
        if urlparts.query:
            path += '?' + urlparts.query
        conn.request(method, path, body=payload, headers=headers)
        response = conn.getresponse()
        start_response('200 OK', [('Content-Type', __content_type__)])
        header_sent = True
        if response.getheader('Set-Cookie'):
            response.msg['Set-Cookie'] = normcookie(response.getheader('Set-Cookie'))
        yield cipher.encrypt('HTTP/1.1 %s\r\n%s\r\n' % (response.status, ''.join('%s: %s\r\n' % (k.title(), v) for k, v in response.getheaders() if k.title() != 'Transfer-Encoding')))
        while True:
            data = response.read()
            if not data:
                return
            yield cipher.encrypt(data)
    except Exception as e:
        if not header_sent:
            start_response('200 OK', [('Content-Type', __content_type__)])
        yield cipher.encrypt('HTTP/1.1 500 Internal Server Error\r\nContent-type: text/html\r\n\r\n')
        yield cipher.encrypt(message_html('500 Internal Server Error', 'urlfetch %r failed' % url, detail=repr(e)))
        raise StopIteration


try:
    import sae
    application = sae.create_wsgi_app(app)
except ImportError:
    pass
try:
    import bae.core.wsgi
    application = bae.core.wsgi.WSGIApplication(application)
except ImportError:
    pass


if __name__ == '__main__':
    import gevent.monkey
    import gevent.wsgi
    gevent.monkey.patch_all()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')
    server = gevent.wsgi.WSGIServer(('', int(sys.argv[1])), application)
    logging.info('local paas_application serving at %s:%s', server.address[0], server.address[1])
    server.serve_forever()
