#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
import sqlite3
from os import environ, rename
from subprocess import check_call, check_output, call
from sys import exit
from Cookie import SimpleCookie
from math import ceil
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

form = cgi.FieldStorage()
conn = sqlite3.connect('insta.db')
c = conn.cursor()
# c.execute("PRAGMA foreign_keys = ON")
cookie = SimpleCookie(environ['HTTP_COOKIE'])

def gen_path(sequence=0, prefix=''):
	return prefix + 'upload_temp/{id}_{sequence}.{ext}'.format(id=form['id'].value, sequence=int(form['sequence'].value)+sequence, ext=form['file_ext'].value)

def new_url(delta):
	old_url = environ['QUERY_STRING'] # type: str
	old_url = old_url.rsplit('=', 1)
	sequence_new = int(old_url[1]) + delta
	return old_url[0] + '=' + str(sequence_new)

def next_sequence():
	url = '{}?{}'.format(environ['SCRIPT_NAME'], new_url(1))
	print '<meta http-equiv="refresh" content="0; url={}">'.format(cgi.escape(url, True))
	print '<h2>Please wait while you\'re being redirected...</h2><noscript>'

if 'action' in form:
	if form['action'].value == 'undo':
		if int(form['sequence'].value) <= 0:
			print "<h1>Nothing to undo</h1>"
			exit()

		path_old = gen_path(-1)
		path_new = gen_path(1)
		rename(path_old, path_new)
		next_sequence()
	elif form['action'].value == 'discard':
		check_call("rm upload_temp/{id}_*.{ext}".format(id=form['id'].value, ext=form['file_ext'].value), shell=True)
		print '<meta http-equiv="refresh" content="0; url=/">'
		print '<h1>Successfully discarded</h1>'
		print '<h2>Please wait while you\'re being redirected...</h2><noscript>'
	elif form['action'].value == 'finish':
		if 'username' not in cookie or len(cookie['username'].value) == 0:
			print "<h1>You are not logged in</h1>"
			exit()
		new_link = 'uploads/{id}.{ext}'.format(id=form['id'].value, ext=form['file_ext'].value)
		c.execute("INSERT INTO photos (link, username, private) VALUES (?, ?, ?)", ('/' + new_link, cookie['username'].value, form['private'].value))
		rename(gen_path(), new_link)
		conn.commit()
		call("rm upload_temp/{id}_*.{ext}".format(id=form['id'].value, ext=form['file_ext'].value), shell=True)
		print '<meta http-equiv="refresh" content="0; url=finish.py?url={}">'.format(new_link)
		print '<h1>Successfully saved</h1>'
		print '<h2>Please wait while you\'re being redirected...</h2>'
	elif form['action'].value == 'border':
		check_call(['convert', gen_path(), '-bordercolor', 'black', '-border', '15', gen_path(1)])
		next_sequence()
	elif form['action'].value == 'lomo':
		check_call(['convert', gen_path(), '-channel', 'R,G', '-level', '33%', gen_path(1)])
		next_sequence()
	elif form['action'].value == 'lens_flare':
		width = check_output(['identify', gen_path()])
		width = width.split(' ')[2].split('x')[0]
		check_call('convert static/lensflare.png -resize {width}x tmp.png && composite -compose screen -gravity northwest tmp.png {in_} {out}'.format(width=width, in_=gen_path(), out=gen_path(1)), shell=True)
		next_sequence()
	elif form['action'].value == 'black_and_white':
		dimensions = check_output(['identify', gen_path()]).split(' ')[2]
		check_call('convert {in_} -type grayscale itm.png && convert static/linear_gradient.png -resize {dimension}\! tmp.png && composite -compose softlight -gravity center tmp.png itm.png {out} && rm itm.png'.format(in_=gen_path(), out=gen_path(1), dimension=dimensions), shell=True)
		next_sequence()
	elif form['action'].value == 'blur':
		check_call(['convert', gen_path(), '-blur', '0.5x4', gen_path(1)])
		next_sequence()
	elif form['action'].value == 'annotate_top':
		if 'font_size' not in form:
			print '<h1>Font size not set</h1>'
			exit()
		if 'message' not in form:
			print '<h1>Message not set</h1>'
			exit()
		check_call(['convert', gen_path(), '-background', 'grey', '-pointsize', form['font_size'].value, '-font', form['font_type'].value, 'label:{}'.format(form['message'].value), '+swap', '-gravity', 'center', '-append', gen_path(1)])
		next_sequence()
	elif form['action'].value == 'annotate_bottom':
		if 'font_size' not in form:
			print '<h1>Font size not set</h1>'
			exit()
		if 'message' not in form:
			print '<h1>Message not set</h1>'
			exit()
		check_call(['convert', gen_path(), '-background', 'grey', '-pointsize', form['font_size'].value, '-font', form['font_type'].value, 'label:{}'.format(form['message'].value), '-gravity', 'center', '-append', gen_path(1)])
		next_sequence()
	else:
		print 'unknown action'

with open('static/editor.html', 'r') as f:
	print str(f.read()).replace('{img_addr}', gen_path(0, '/'))