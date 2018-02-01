#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from os import environ, rename
from subprocess import check_call
from sys import exit
from Cookie import SimpleCookie
from math import ceil
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

form = cgi.FieldStorage()
conn = sqlite3.connect('insta.db')
c = conn.cursor()
cookie = SimpleCookie(environ['HTTP_COOKIE'])

def new_url(delta):
	old_url = environ['QUERY_STRING'] # type: str
	old_url = old_url.rsplit('=', 1)
	sequence_new = int(old_url[1]) + delta
	return old_url[0] + '=' + str(sequence_new)

if 'action' in form:
	if form['action'].value == 'undo':
		if int(form['sequence'].value) <= 0:
			print "<h1>Nothing to undo</h1>"
			exit()

		path_old = 'upload_temp/{id}_{sequence}.{ext}'.format(id=form['id'].value, sequence=int(form['sequence'].value)-1, ext=form['file_ext'].value)
		path_new = 'upload_temp/{id}_{sequence}.{ext}'.format(id=form['id'].value, sequence=int(form['sequence'].value)+1, ext=form['file_ext'].value)
		rename(path_old, path_new)
		url = '{}?{}'.format(environ['SCRIPT_NAME'], new_url(1))
		print '<meta http-equiv="refresh" content="0; url={}">'.format(cgi.escape(url, True))
		print '<h2>Please wait while you\'re being redirected...</h2>'
	elif form['action'].value == 'discard':
		check_call("rm upload_temp/{id}_*.{ext}".format(id=form['id'].value, ext=form['file_ext'].value), shell=True)
		print '<meta http-equiv="refresh" content="0; url=/">'
		print '<h1>Successfully discarded</h1>'
		print '<h2>Please wait while you\'re being redirected...</h2>'
	elif form['action'].value == 'finish':
		if 'username' not in cookie or len(cookie['username'].value) == 0:
			print "<h1>You are not logged in</h1>"
			exit()
		new_link = 'uploads/{id}.{ext}'.format(id=form['id'].value, ext=form['file_ext'].value)
		c.execute("INSERT INTO photos (link, username, private) VALUES (?, ?, ?)", ('/' + new_link, cookie['username'].value, form['private'].value))
		rename('upload_temp/{id}_{sequence}.{ext}'.format(id=form['id'].value, sequence=form['sequence'].value, ext=form['file_ext'].value), new_link)
		conn.commit()
		print '<meta http-equiv="refresh" content="0; url=/">'
		print '<h1>Successfully saved</h1>'
		print '<h2>Please wait while you\'re being redirected...</h2>'
	else:
		print '\n unknown action'

with open('editor.html', 'r') as f:
	print f.read()