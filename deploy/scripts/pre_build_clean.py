#!/usr/bin/env python

# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

if __name__ == '__main__':
	import sys
	if len(sys.argv)<2:
		print "Usage: %s build_dir" % sys.argv[0]
		sys.exit(1)

	import os
	import shutil
	os.chdir('/tmp')
	print "Removing any previous build dir"
	shutil.rmtree(sys.argv[1], ignore_errors=True)
	print "Done"
	sys.exit(0)
