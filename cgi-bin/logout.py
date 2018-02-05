#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
from Cookie import SimpleCookie

cgitb.enable()
print 'Content-type: text/html'
cookie = SimpleCookie()

cookie['username'] = ''
print cookie
print '\n<meta http-equiv="refresh" content="0; url=/">'
print '<h1>Done logging out</h1>'