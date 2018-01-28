#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from math import ceil
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

form = cgi.FieldStorage()
conn = sqlite3.connect('insta.db')
c = conn.cursor()

def new_url(delta):
	old_url = form.fp.getvalue() # type: str
	old_url = old_url.rsplit('=', 1)
	return old_url[0] + '=' + str(int(old_url[1]) + delta)

print new_url(-1)

if 'action' in form:
	if form['action'].value == 'undo':
		print 'undo'
	else:
		print 'unknown action'

with open('editor.html', 'r') as f:
	print f.read()