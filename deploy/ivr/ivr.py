import urllib
import datetime
import StringIO
from ftplib import FTP

answer()

wait(1500)
say("http://hosting.tropo.com/44537/www/audio/sound_1.wav")
wait(500)

data = StringIO.StringIO()

data.write("Call from: %s\n" % currentCall.callerID)
data.write("Time: %s\n" % str(datetime.datetime.now()))

result = ask("http://hosting.tropo.com/44537/www/audio/sound_2.wav", {'repeat' : 3, 'choices' : "[2 DIGITS]", 'bargein' : False})
if (result.name == 'choice'):
    log("***********District code: " + result.value)
    data.write("District Code: %s\n" % result.value)

result = ask("http://hosting.tropo.com/44537/www/audio/sound_3.wav", {'repeat':3, 'choices':"[1 DIGITS]", 'bargein' : False})
if (result.name == 'choice'):
    log("***********Gender: " + result.value)
    data.write("Gender: %s\n" % result.value)

result = ask("http://hosting.tropo.com/44537/www/audio/sound_4.wav", {'repeat':3, 'choices':"[2 DIGITS]", 'bargein' : False})
if (result.name == 'choice'):
    log("***********Age: " + result.value)
    data.write("Age: %s\n" % result.value)

result = record( "http://hosting.tropo.com/44537/www/audio/sound_5.wav",
                 { 'beep':True, 'timeout':10, 'silenceTimeout':4, 'maxTime':30, 'choiceMode':'speech', 'format':'audio/mp3', 'bargein':False})
if (result.name == 'record'):
    log( "result.recordURI = " + result.recordURI )
    filename = "q1-%s-%s.wav" % (currentCall.callerID, str(datetime.datetime.now()))
    data.write("Response 1 filename: %s\n" % filename)

f = urllib.urlopen(result.recordURI)
ftp = FTP('ftp.servage.net', 'unicef', 'recordmyvoice')
ftp.storbinary('STOR %s' % filename, f)
ftp.close()

result = record( "http://hosting.tropo.com/44537/www/audio/sound_6.wav",
                 { 'beep':True, 'timeout':10, 'silenceTimeout':4, 'maxTime':30, 'choiceMode':'speech', 'format':'audio/mp3', 'bargein':False})
if (result.name == 'record'):
    log( "result.recordURI = " + result.recordURI )
    filename = "q2-%s-%s.wav" % (currentCall.callerID, str(datetime.datetime.now()))
    data.write("Response 2 filename: %s\n" % filename)

f = urllib.urlopen(result.recordURI)
ftp = FTP('ftp.servage.net', 'unicef', 'recordmyvoice')
ftp.storbinary('STOR %s' % filename, f)
data.seek(0)
ftp.storlines('STOR %s-%s.txt' % (currentCall.callerID, str(datetime.datetime.now())), data)
ftp.close()

say("http://hosting.tropo.com/44537/www/audio/sound_7.wav")

hangup()
