python /var/lib/buildbot/github_buildbot.py -p 8097 -l /var/log/github_buildbot.py.log &
buildbot start master/
buildbot start slave/
