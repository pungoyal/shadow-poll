rm -rf pungoyal-shadow-poll-*

wget http://github.com/pungoyal/shadow-poll/tarball/master
tar -xvf pungoyal-shadow-poll-*.tar.gz
sudo pungoyal-shadow-poll-*/deploy/scripts/./redeploy.py

rm -rf pungoyal-shadow-poll-*