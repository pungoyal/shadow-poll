
python /var/lib/buildbot/slave/shadow-poll/build/manage.py syncdb --noinput
rm -rf /var/www/shadowpoll/*
cp -r /var/lib/buildbot/slave/shadow-poll/build/* /var/www/shadowpoll

