#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from os import environ
from subprocess import check_call
from math import ceil
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

form = cgi.FieldStorage()
conn = sqlite3.connect('insta.db')
c = conn.cursor()

def new_url(delta):
	old_url = environ['QUERY_STRING'] # type: str
	old_url = old_url.rsplit('=', 1)
	return old_url[0] + '=' + str(int(old_url[1]) + delta)

if 'action' in form:
	if form['action'].value == 'undo':
		url = '{}?{}'.format(environ['SCRIPT_NAME'], new_url(-1))
		print '<meta http-equiv="refresh" content="0; url={}">'.format(cgi.escape(url, True))
		print '<h1>Please wait while you\'re being redirected...</h1>'
	elif form['action'].value == 'discard':
		check_call("rm upload_temp/{id}_*.jpg".format(id=form['id'].value), shell=True)
	elif form['action'].value == 'finish':
		pass
	else:
		print '\n unknown action'

with open('editor.html', 'r') as f:
	print f.read()