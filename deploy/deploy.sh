#!/bin/sh

/etc/init.d/rapidsms-init stop
rm -rf /var/www/shadowpoll/*

cp /var/lib/buildbot/slave/shadow-poll/build/rapidsms.ini.ci /var/lib/buildbot/slave/shadow-poll/build/rapidsms.ini
python /var/lib/buildbot/slave/shadow-poll/build/manage.py syncdb --noinput
python /var/lib/buildbot/slave/shadow-poll/build/manage.py loaddata poll_responses.json

cp -r /var/lib/buildbot/slave/shadow-poll/build/* /var/www/shadowpoll
/etc/init.d/rapidsms-init start

