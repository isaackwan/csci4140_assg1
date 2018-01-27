#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from Cookie import SimpleCookie
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n\n'

form = cgi.FieldStorage()
conn = sqlite3.connect('insta.db')
c = conn.cursor()

header()
print '<link rel="stylesheet" href="/css/index.css">'

if c.execute('SELECT COUNT(*) FROM users WHERE username = ? AND password = ?', form['username'].value, form['password'].value).fetchone()[0] == 1:
	print 'login success'
else:
	print 'login failed'

footer()