#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from Cookie import SimpleCookie
from subprocess import call
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html'

form = cgi.FieldStorage()
conn = sqlite3.connect('insta.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")
cookie = SimpleCookie()

if 'confirm' not in form:
	print '\n<h1>Please go to /init.html</h1>'
	exit()

cookie['username'] = ''
print cookie
print '\n'

cursor.execute('DELETE FROM users')
conn.commit()

call('rm upload_temp/* uploads/*', shell=True)

print '<h1>Reset success</h1>'
print '<p><a href="/">Click me to go back to the front page.</a></p>'