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

header()
print '<link rel="stylesheet" href="/css/index.css">'

print '<nav class="navbar navbar-dark bg-primary navbar-expand">'

if 'username' not in cookie or '' == cookie['username'].value:
	print '<ul class="navbar-nav"><li class="nav-item"><a class="nav-link active" href="#">Login</a></li><li class="nav-item"><a class="nav-link active" href="#">Register</a></li></ul>'
else:
	print '<span class="navbar-text">Hello, {username}!</span><ul class="navbar-nav"><li class="nav-item"><a class="nav-link active " href="#">Logout</a></li></ul>'.format(username=cookie['username'].value)
print '</nav>'

print '<div class="row">'

try:
	offset = int(form['offset'].value)
except KeyError:
	offset = 0

if False == False:
	query = 'SELECT * FROM photos ORDER BY time DESC'
else:
	query = ''

for row in c.execute(query + ' LIMIT 8 OFFSET ?', str(offset*8)):
	print '<div class="col-1 col-md-3"><a href="{}" target="_blank"><img src="{}" class="img-thumbnail"></a></div>'.format(cgi.escape(row[1]), cgi.escape(row[1]))

print '</div>'

total_pages = c.execute('SELECT COUNT(*) FROM ({})'.format(query)).fetchone()[0]
total_pages = int(ceil(float(total_pages)/8))

print '<nav aria-label="Page navigation example"><ul class="pagination"><li class="page-item"><a class="page-link" href="?offset={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(offset-1)

for i in range(1, total_pages+1):
	is_current_page = (i-1) == offset
	print '<li class="page-item {}"><a class="page-link" href="?offset={}">{}</a></li>'.format('active' if is_current_page else '', i-1, i)

print '<li class="page-item"><a class="page-link" href="?offset={}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li></ul></nav>'.format(offset+1)

print '<div class="card"><div class="card-header">Upload photo</div><div class="card-body"><form action="/cgi-bin/upload.py" method="POST" enctype="multipart/form-data"><div class="form-group">' \
	  '<input name="file" type="file" class="form-control-file">' \
	  '<div class="form-check form-check-inline"><input class="form-check-input" type="radio" name="private" id="private_public" value="0" checked><label class="form-check-label" for="private_public">Public</label></div><div class="form-check form-check-inline"><input class="form-check-input" type="radio" name="private" id="private_private" value="1"><label class="form-check-label" for="private_private">Private</label></div>' \
	  '<button type="submit" class="btn btn-primary">Upload</button></div></form></div></div>'

footer()