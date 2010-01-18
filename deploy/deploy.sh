kill -9 $(cat /tmp/shadowpoll.pid)
python /var/lib/buildbot/slave/shadow-poll/build/manage.py syncdb --noinput
rm -rf /var/www/shadowpoll/*
cp -r /var/lib/buildbot/slave/shadow-poll/build/* /var/www/shadowpoll
python /var/lib/buildbot/slave/shadow-poll/build/manage.py runfcgi host=127.0.0.1 port=8801 pidfile=/tmp/shadowpoll.pid
