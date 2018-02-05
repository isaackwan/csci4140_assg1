#!/usr/bin/env python2

from pprint import pprint
import cgi
import cgitb
from os import environ
from html_helpers import header, footer

cgitb.enable()
print 'Content-type: text/html\n'

form = cgi.FieldStorage()

header()

print '<a role="button" class="btn btn-primary btn-lg btn-block" href="/">Back</a>'
print '<form><div class="form-group"><input class="form-control" value="{}"></div>'.format(environ['CSCI4140_URL'] + '/' + cgi.escape(form['url'].value))
print '<img src="{}" class="img-thumbnail">'.format(cgi.escape('/' + form['url'].value))

footer()