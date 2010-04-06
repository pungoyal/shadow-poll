#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import os
import subprocess as sp
import pexpect
import shutil

DB_NAME='iraqchildren'
DB_USER='unicef'
DB_PWD='unicef'
DEPLOY_DIR='/var/www/'
APP_DIR='/var/www/shadow-poll/'
INIT_SCRIPT='/etc/init.d/rapidsms-init'
GIT_URL='git://github.com/pungoyal/shadow-poll.git'
CWD=os.getcwd()

def issue_cmd(cmd, failure_msg='Failed'):
    p = sp.Popen(cmd, stdout=sp.PIPE)
    print p.communicate()[0]
    if p.returncode != 0:
        print failure_msg
        os.chdir(CWD)
        sys.exit(p.returncode)

if __name__ == '__main__':
    import sys
    if len(sys.argv)>1:
        print "Usage: %s" % sys.argv[0]
        sys.exit(1)

    print "Stopping Iraq Children server"
    issue_cmd([INIT_SCRIPT, 'stop'], 'Could not stop Maplayers server')

    print "Deleting the app directory"
    shutil.rmtree(APP_DIR)

    print "Updating Git repo"
    os.chdir(DEPLOY_DIR)
    issue_cmd(['git', 'clone', GIT_URL], 'Could not pull git updates')

    print "Fixing ownership"
    os.chdir(DEPLOY_DIR)
    issue_cmd(['chown', '-R', 'www-data:www-data', DEPLOY_DIR], 'Could not set permissions')

    #print "creating resources folders"
    #os.chdir(DEPLOY_DIR)
    #issue_cmd(['mkdir','-p',  '/static/resources'])

    #os.chdir(DEPLOY_DIR)
    #issue_cmd(['mkdir', '-p', '/static/project-photos'])

    #os.chdir(DEPLOY_DIR)
    #issue_cmd(['chmod', '+w', '/static/resources'])

    #os.chdir(DEPLOY_DIR)
    #issue_cmd(['chmod', '+w', '/static/project-photos'])

    print "Dumping existing db"
    try:
        child = pexpect.spawn ('dropdb -U %s %s' % (DB_USER, DB_NAME))
        # child.logfile = sys.stdout
        #child.expect_exact ('Password:')
        #child.sendline (DB_PWD)
        child.wait()
    except:
        print "Failed to drop db"
        sys.exit(1)

    print "Creating blank db"
    try:
        child = pexpect.spawn ('createdb -T template_postgis -O %(user)s -U %(user)s %(db)s' % \
				       { 'user': DB_USER, 'db': DB_NAME} )
        # child.logfile = sys.stdout
        #child.expect_exact ('Password:')
        #child.sendline (DB_PWD)
        child.wait()
    except:
        print "Failed to create db"
        sys.exit(1)

    print "Syncing db and loading initial data"
    os.chdir(APP_DIR)
    try:
        child = pexpect.spawn ('./manage.py syncdb')
        # child.logfile = sys.stdout
        child.expect ('Would .*: ')
        child.sendline ('yes')
        child.expect('Username .*: ')
        child.sendline('supa')
        child.expect_exact('E-mail address: ')
        child.sendline('webmaster@mepemepe.com')
        child.expect_exact('Password: ')
        child.sendline('supa')
        child.expect_exact('Password (again): ')
        child.sendline('supa')
        child.wait()
    except Exception, ex:
        print ex
        print "Failed to sync db"
        sys.exit(1)

    issue_cmd(['python','manage.py','syncdb'], 'Could not sync db')
    issue_cmd(['python','manage.py', 'loaddata',os.path.join(APP_DIR, 'apps/charts/fixtures/messages.json')],
              'Could not load voice messages')

    print "Starting iraq-children server"
    issue_cmd([INIT_SCRIPT, 'start'], 'Could not start IraqChildren server')

#print "Starting smoke test"
#issue_cmd(['python', 'deploy/smoke/maplayer_smoke.py'], 'Failed in running smoke')

