#!/usr/bin/env python

# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

SETTINGS = 'rapidsms.ini.dev'

if __name__ == '__main__':
	import sys
	if len(sys.argv)>1:
		print "Usage: %s" % sys.argv[0]
		sys.exit(1)

	import os
	print "Using %s for settings.py" % SETTINGS
	os.symlink(SETTINGS,'rapidsms.ini')
	print "Done"
	sys.exit(0)
