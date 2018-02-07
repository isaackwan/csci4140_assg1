#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from Cookie import SimpleCookie
from subprocess import call
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

conn = sqlite3.connect('insta.db')
cursor = conn.cursor()
cookie = SimpleCookie()

admin_exist = cursor.execute('SELECT 1=1 FROM users WHERE username = "admin"').fetchone() != None

header()

print '<h1>System Initialization</h1><p>Important: all data would be deleted</p>' \
'<form method="POST" action="/cgi-bin/reset.py">'

if admin_exist :
	print '<div class="form-group"><input class="form-control" placeholder="Enter admin password" name="password_verify" required type=password></div>'
else:
	print '<div class="form-group"><input class="form-control" placeholder="Define admin password" name="password_new" required type=password></div>'

print '<button name="confirm" value="yes" class="btn btn-danger btn-lg btn-block">Please Go Ahead</button>' \
'<a href="/" class="btn btn-secondary btn-lg btn-block">Go Back</a>' \
'</form>'

footer()