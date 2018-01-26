#!/usr/bin/env python2

import cgi
import cgitb
import sqlite3
from html import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

conn = sqlite3.connect('insta.db')
c = conn.cursor()

header()

for row in c.execute('SELECT * FROM photos'):
	print row

footer()