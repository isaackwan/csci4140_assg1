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
cookie = SimpleCookie()

if form['password'].value != form['password2'].value:
	print '\n'
	print 'The passwords does not match'
else:
	try:
		cursor.execute('INSERT INTO users (`username`, `password`) VALUES (?, ?)', (form['username'].value, form['password'].value))
		conn.commit()
		cookie['username'] = form['username'].value
		print cookie
		print '\n'
		print '<meta http-equiv="refresh" content="0; url=/">'
		print 'Registration success'
	except sqlite3.IntegrityError:
		print '\n'
		print 'Sorry, the username has been taken'