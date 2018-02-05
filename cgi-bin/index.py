#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from Cookie import SimpleCookie
from os import environ
from math import ceil
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

form = cgi.FieldStorage()
conn = sqlite3.connect('insta.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")
cookie = SimpleCookie(environ['HTTP_COOKIE'])
not_logged_in = 'username' not in cookie or '' == cookie['username'].value # type: bool

header()
print '<link rel="stylesheet" href="/css/index.css">'

print '<nav class="navbar navbar-dark bg-primary navbar-expand">'

if not_logged_in:
	print '<ul class="navbar-nav"><li class="nav-item"><a class="nav-link active" href="/login.html">Login</a></li><li class="nav-item"><a class="nav-link active" href="/register.html">Register</a></li></ul>'
else:
	print '<span class="navbar-text">Hello, {username}!</span><ul class="navbar-nav"><li class="nav-item"><a class="nav-link active " href="/cgi-bin/logout.py">Logout</a></li></ul>'.format(username=cookie['username'].value)
print '</nav>'

print '<div class="row">'

try:
	offset = int(form['offset'].value)
except KeyError:
	offset = 0

if not_logged_in:
	query = 'SELECT link FROM photos WHERE private = 0 ORDER BY time DESC LIMIT 8 OFFSET ?'
	query = c.execute(query, (str(offset*8)))
else:
	query = 'SELECT link FROM photos WHERE (private = 0 OR username = ?) ORDER BY time DESC LIMIT 8 OFFSET ?'
	query = c.execute(query, (cookie['username'].value, str(offset*8)))

for row in query:
	print '<div class="col-1 col-md-3"><a href="{}" target="_blank"><img src="{}" class="img-thumbnail"></a></div>'.format(cgi.escape(row[0]), cgi.escape(row[0]))

print '</div>'

if not_logged_in:
	total_pages = 'SELECT COUNT(*) FROM (SELECT link FROM photos WHERE private = 0 ORDER BY time DESC)'
	total_pages = c.execute(total_pages)
else:
	total_pages = 'SELECT COUNT(*) FROM (SELECT link FROM photos WHERE (private = ? OR username = ?) ORDER BY time DESC)'
	total_pages = c.execute(total_pages, (0, cookie['username'].value))

total_pages = total_pages.fetchone()[0]
#print (total_pages)
total_pages = int(ceil(float(total_pages)/8))
#print total_pages

print '<nav aria-label="Page navigation example"><ul class="pagination">'

for i in range(1, total_pages+1):
	is_current_page = (i-1) == offset
	print '<li class="page-item {}"><a class="page-link" href="?offset={}">{}</a></li>'.format('active' if is_current_page else '', i-1, i)

print '</ul></nav>'.format(offset+1)

if not not_logged_in:
	print '<div class="card"><div class="card-header">Upload photo</div><div class="card-body"><form action="/cgi-bin/upload.py" method="POST" enctype="multipart/form-data"><div class="form-group">' \
		  '<input name="file" type="file" class="form-control-file" required>' \
		  '<div class="form-check form-check-inline"><input class="form-check-input" type="radio" name="private" id="private_public" value="0" checked><label class="form-check-label" for="private_public">Public</label></div><div class="form-check form-check-inline"><input class="form-check-input" type="radio" name="private" id="private_private" value="1"><label class="form-check-label" for="private_private">Private</label></div>' \
		  '<button type="submit" class="btn btn-primary">Upload</button></div></form></div></div>'

footer()
