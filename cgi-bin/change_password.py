#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from Cookie import SimpleCookie
import os
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

form = cgi.FieldStorage()
conn = sqlite3.connect('insta.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")
cookie = SimpleCookie(os.environ['HTTP_COOKIE'])

if form['password'].value != form['password2'].value:
	print 'The passwords does not match'
else:
	if cursor.execute('UPDATE users SET `password` = ? WHERE `username` = ? AND `password` = ?', (form['password'].value, cookie['username'].value, form['password_old'].value)).rowcount >= 1:
		conn.commit()
		print 'Nice! Updated.'
	else:
		print 'Your current password is incorrect'