#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
import os
from uuid import uuid4
from subprocess import check_output
from Cookie import SimpleCookie
from shutil import copyfileobj
from urllib import quote
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

form = cgi.FieldStorage()

if form['file'].file:
	identify_output = check_output(["identify", "-"], stdin=form['file'].file)
	if ('PNG' in identify_output and form['file'].filename[-4:] == '.png') or \
		('GIF' in identify_output and form['file'].filename[-4:] == '.gif') or \
		('JPEG' in identify_output and form['file'].filename[-4:] == '.jpg') or \
		('JPEG' in identify_output and form['file'].filename[-5:] == '.jpeg'):
		id = str(uuid4())
		file_ext = form['file'].filename.split('.')[-1]
		with open('upload_temp/{}_0.{}'.format(id, file_ext), 'wb') as fout:
			form['file'].file.seek(0)
			copyfileobj(form['file'].file, fout, 100000)
		print 'Nice! Copied Over. Bringing you to the editor page...'
		print '<meta http-equiv="refresh" content="0; url=/cgi-bin/editor.py?id={}&file_ext={}&private={}&sequence=0">'.format(quote(id), quote(file_ext), quote(form['private'].value))

	else:
		print 'Rejecting because file type does not match'

else:
	print 'Crap, no file uploaded'