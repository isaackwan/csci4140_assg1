#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from Cookie import SimpleCookie
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html'

form = cgi.FieldStorage()
conn = sqlite3.connect('insta.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")
cookie = SimpleCookie()

if cursor.execute('SELECT 1=1 FROM users WHERE username = ? AND password = ?', (form['username'].value, form['password'].value)).fetchone() != None:
	cookie['username'] = form['username'].value
	print cookie
	print '\n'
	print '<meta http-equiv="refresh" content="0; url=/">'
	print 'login success'
else:
	print '\n'
	print 'login failed, please try again'