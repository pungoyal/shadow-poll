#!/bin/sh

kill -9 `ps -ef | grep route | grep python | awk '{print $2}'`
kill -9 $(cat /tmp/shadowpoll.pid)
rm -rf /var/www/shadowpoll/*

cp /var/lib/buildbot/slave/shadow-poll/build/rapidsms.ini.ci /var/lib/buildbot/slave/shadow-poll/build/rapidsms.ini
python /var/lib/buildbot/slave/shadow-poll/build/manage.py syncdb --noinput
python /var/lib/buildbot/slave/shadow-poll/build/manage.py loaddata poll_responses.json

cp -r /var/lib/buildbot/slave/shadow-poll/build/* /var/www/shadowpoll
python /var/www/shadowpoll/manage.py runfcgi -v 2 host=127.0.0.1 port=8801 pidfile=/tmp/shadowpoll.pid outlog=/var/log/shadowpoll/fcgi.log errlog=/var/log/shadowpoll/fcgi-errors.log
