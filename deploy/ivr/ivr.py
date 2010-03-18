import urllib
import datetime
from ftplib import FTP

answer()

wait(1500)
say("http://hosting.tropo.com/44537/www/audio/sound_1.wav")
wait(500)

result = ask("http://hosting.tropo.com/44537/www/audio/sound_2.wav", {'repeat' : 3, 'choices' : "[2 DIGITS]", 'bargein' : False})
if (result.name == 'choice'):
    log("***********District code: " + result.value)

result = ask("http://hosting.tropo.com/44537/www/audio/sound_3.wav", {'repeat':3, 'choices':"[1 DIGITS]", 'bargein' : False})
if (result.name == 'choice'):
    log("***********Gender: " + result.value)

result = ask("http://hosting.tropo.com/44537/www/audio/sound_4.wav", {'repeat':3, 'choices':"[2 DIGITS]", 'bargein' : False})
if (result.name == 'choice'):
    log("***********Age: " + result.value)

result = record( "http://hosting.tropo.com/44537/www/audio/sound_5.wav",
                 { 'beep':True, 'timeout':10, 'silenceTimeout':4, 'maxTime':30, 'choiceMode':'speech', 'format':'audio/mp3', 'bargein':False})
if (result.name == 'record'):
    log( "result.recordURI = " + result.recordURI )
    say( "http://hosting.tropo.com/44537/www/audio/sound_6.wav" + result.recordURI )

f = urllib.urlopen(result.recordURI)
ftp = FTP('ftp.servage.net', 'unicef', 'recordmyvoice')
ftp.storbinary('STOR %s-%s.wav' % (currentCall.callerID, str(datetime.datetime.now())), f)
ftp.close()

say("http://hosting.tropo.com/44537/www/audio/sound_7.wav")

hangup()