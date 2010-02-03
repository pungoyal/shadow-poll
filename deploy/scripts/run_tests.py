#!/usr/bin/env python

# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

if __name__ == '__main__':
	import sys
	if len(sys.argv)>1:
		print "Usage: %s" % sys.argv[0]
		sys.exit(1)

	import os
	import subprocess as sp
	print "Running Django tests for all apps"
	p = sp.Popen(["python", "manage.py","test"], stdout=sp.PIPE)
	print p.communicate()[0]
	sys.exit(p.returncode)

