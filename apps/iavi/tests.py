from rapidsms.tests.scripted import TestScript
from app import App
from models import *
import reporters.app as reporters_app
import tree.app as tree_app
#import i18n.app as i18n_app
from reporters.models import Reporter
import datetime

class TestApp (TestScript):
    apps = (reporters_app.App, App, tree_app.App )
    fixtures = ["iavi_locations", "iavi_trees", 'test_backend']
    
    
    
    def testRegistration(self):
        reg_script = """
            # base case
            reg_1 > *#En#22#001#*
            reg_1 < Confirm 001 Registration is Complete
            reg_1 < Please Enter Your PIN Code
            # we'll deal with pins later
            # bad location id
            reg_2 > *#En##002#*
            reg_2 < Error 002. Unknown location
            reg_2 > *#En#34#002#*
            reg_2 < Error 002. Unknown location 34
            # bad participant ids
            reg_3 > *#En#22##*
            reg_3 < Error. Id must be 3 numeric digits. You sent 
            reg_3 > *#En#22#03#*
            reg_3 < Error. Id must be 3 numeric digits. You sent 03 
            reg_3 > *#En#22#0003#*
            reg_3 < Error. Id must be 3 numeric digits. You sent 0003 
            reg_3 > *#En#22#o003#*
            reg_3 < Error. Id must be 3 numeric digits. You sent o003 
            # test a duplicate id
            reg_4 > *#En#22#001#*
            # but allow them to register with the same id in a different location
            reg_4 < Sorry, 001 has already been registered. Please choose a new user id.
            # but a duplicate at a new location should be ok
            reg_5 > *#En#19#001#*
            reg_5 < Confirm 001 Registration is Complete
            reg_5 < Please Enter Your PIN Code
        """
        self.runScript(reg_script)
        
        # this reporter should have been created
        rep1 = IaviReporter.objects.get(alias="22-001")
        
        # these ones should not have
        dict = {"alias":"22-002"}
        self.assertRaises(IaviReporter.DoesNotExist, IaviReporter.objects.get, **dict)     
        dict = {"alias":"22-003"}
        self.assertRaises(IaviReporter.DoesNotExist, IaviReporter.objects.get, **dict)     
    
    def testTimeFormats(self):
        reg_script = """
            # test time format failures
            # That's an "oh" 
            time_format_1 > *#En#22#004#140O#*
            time_format_1 < Error 004. Time must be 4 numeric digits between 0000 and 2359. You sent 140O
            time_format_1 > *#En#22#004#2400#*
            time_format_1 < Error 004. Time must be 4 numeric digits between 0000 and 2359. You sent 2400
            time_format_1 > *#En#22#004#1460#*
            time_format_1 < Error 004. Time must be 4 numeric digits between 0000 and 2359. You sent 1460
            time_format_1 > *#En#22#004#0000#*
            time_format_1 < Confirm 004 Registration is Complete
            time_format_1 < Please Enter Your PIN Code
            time_format_2 > *#En#22#005#*
            time_format_2 < Confirm 005 Registration is Complete
            time_format_2 < Please Enter Your PIN Code
            time_format_3 > *#En#22#006#1838#*
            time_format_3 < Confirm 006 Registration is Complete
            time_format_3 < Please Enter Your PIN Code
        """
        self.runScript(reg_script)
        
        # this reporter should have been created
        # and his time should be 0000
        rep = IaviReporter.objects.get(alias="22-004")
        time_status = StudyParticipant.objects.get(reporter=rep)
        self.assertEqual(time_status.notification_time, datetime.time(0,0))
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
        self.assertEqual(time_status.start_date, tomorrow)
        
        # this one should get the default (1600)
        rep = IaviReporter.objects.get(alias="22-005")
        time_status = StudyParticipant.objects.get(reporter=rep)
        self.assertEqual(time_status.notification_time, datetime.time(16,0))
        self.assertEqual(time_status.start_date, tomorrow)
        
        # this one should be 1838
        rep = IaviReporter.objects.get(alias="22-006")
        time_status = StudyParticipant.objects.get(reporter=rep)
        self.assertEqual(time_status.notification_time, datetime.time(18,38))
        self.assertEqual(time_status.start_date, tomorrow)
        
    
        
    def testTestSubmission(self):
        tester = self._register("tester", "001", "1234", "19", "en")
        nurse = self._register("nurse", "002", "1234", "19", "en")
        script = """
            # base case
            nurse > *#8377#19#001#*
            tester < Hello, Please Reply With Your PIN
            tester > 1234
            tester < Did you have sex with your main partner in the last 24 hours?
            tester > no
        """
        self.runScript(script)
        # make sure we got an active session for this.
        self.assertEqual(1, len(TestSession.objects.all()))
        session = TestSession.objects.get(tester=tester)
        self.assertEqual(nurse.connection(),session.initiator)
        self.assertEqual("A",session.status)
        script = """
            tester < Did you have sex with any other partner in the last 24 hours?
            tester > NO
            # due to some minor quirkiness, the nurse's message actually comes first
            nurse < 001 Passes Test            
            tester < Questionnaire is complete. Thank you.
            # unknown user
            nurse > *#8377#19#003#*
            nurse < Error 003. Unknown user.
        """
        self.runScript(script)
        # try in another language 
        self._register("tester2", "003", "1234", "19", "lg")
        script = """
            nurse > *#8377#19#003#*
            tester2 < Ssebo/Nnyabo Yingiza ennamba yo eye'kyaama mu ssimu yo. Era ennamba eyo giwereze ku kompyuta yaffe.
            tester2 > 1234
            tester2 < Wetabyeeko mu kikolwa eky'omukwano n'omwagalwawo gw'olinaye mukunoonyereza kuno mu lunaku lumu oluyise?
            tester2 > yes
            tester2 < Mwakozesezza kondomu?
            tester2 > yes
            tester2 < Wetabyeeko mu kikolwa ky'omukwano n'omwagalwawo omulala yenna mu lunaku lumu oluyise?
            tester2 > no
            nurse < 003 Passes Test            
            tester2 < Ebibuuzo bino bikomemye wano. Webale nnyo kuwaayo budde bwo.
        """
        self.runScript(script)
        # try another location
        self._register("tester3", "004", "1234", "22", "en")
        script = """
            nurse > *#8377#22#004#*
            tester3 < Hello, Please Reply With Your PIN
            tester3 > 1234
            tester3 < How many times did you have sex in the last 24 hours?
            tester3 > 2
            tester3 < Of the number of times that you had sex in the last 24 hours, how many times were condoms used?
            tester3 > 2
            nurse < 004 Passes Test            
            tester3 < Interview is complete. Remember to use a new condom each time you have sex and take your pills as agreed. Thank you
        """
        self.runScript(script)    
        # make sure these didn't count as real sessions
        self.assertEqual(0, len(Report.objects.all()))
        self.assertEqual(3, len(TestSession.objects.all()))
        for session in TestSession.objects.all():
            # the users were marked as passed
            self.assertEqual("P", session.status)
            self.assertEqual(nurse.connection(), session.initiator)
        for session in TestSession.objects.all():
            # the users were marked as passed
            self.assertEqual("P", session.status)
            self.assertEqual(nurse.connection(), session.initiator)
        
        
    def testPinEntry(self):
        # this does a base registration/pin combo with everyhing correct
        self._register("pin_1", "001", "4567")
        
        # get him back and make sure he's got the right pin
        rep = IaviReporter.objects.get(alias="22-001")
        self.assertEqual("4567", rep.pin)
        
        pin_script = """
            pin_2 > *#En#22#002#*
            pin_2 < Confirm 002 Registration is Complete
            pin_2 < Please Enter Your PIN Code
            # test some poor formats
            pin_2 > 
            pin_2 < Error 002. Poorly formatted PIN, must be 4 numbers. Please try again.
            pin_2 > 123
            pin_2 < Error 002. Poorly formatted PIN, must be 4 numbers. Please try again.
            pin_2 > 12345
            pin_2 < Error 002. Poorly formatted PIN, must be 4 numbers. Please try again.
            pin_2 > 123 4
            pin_2 < Error 002. Poorly formatted PIN, must be 4 numbers. Please try again.
            pin_2 > 123a
            pin_2 < Error 002. Poorly formatted PIN, must be 4 numbers. Please try again.
            pin_2 > I don't understand
            pin_2 < Error 002. Poorly formatted PIN, must be 4 numbers. Please try again.
        """
        self.runScript(pin_script)
        
        # get him back and make sure he doesn't have a pin yet
        rep = IaviReporter.objects.get(alias="22-002")
        self.assertEqual(None, rep.pin)
        
        pin_script = """
            pin_3 > *#En#22#003#*
            pin_3 < Confirm 003 Registration is Complete
            pin_3 < Please Enter Your PIN Code
            pin_3 > 1234
            # test mismatch
            pin_3 < Please Enter Your PIN Code Again
            pin_3 > 1235
            pin_3 < Error 003. PINs did not match. Please enter your PIN Code
            pin_3 > 1234
            pin_3 < Please Enter Your PIN Code Again
            pin_3 > 1235
            pin_3 < Error 003. PINs did not match. Please enter your PIN Code
        """
        self.runScript(pin_script)
        
        rep = IaviReporter.objects.get(alias="22-003")
        self.assertEqual(None, rep.pin)
        
        
    def testAllowEntry(self):
        # tests who is allowed to enter a survey.  for this application
        # only registered users with correctly set PINs are allowed to 
        # participate.  others will be rejected.  
        script = """
            # base case
            rejected_guy > iavi uganda
            rejected_guy < Sorry, only known respondants are allowed to participate in the survey. Please register before submitting.
            # register but don't set a PIN
            rejected_guy > *#En#22#001#*
            rejected_guy < Confirm 001 Registration is Complete
            rejected_guy < Please Enter Your PIN Code
            rejected_guy > iavi uganda
            rejected_guy < You must set a PIN before participating in the survey. Respond "iavi set pin" (without quotes) to do this now.
        """
        self.runScript(script)
        
        # register someone with a pin, and make sure they get in
        self._register("accepted_guy", "002", "1238")
        script = """
            accepted_guy > iavi uganda
            accepted_guy < Hello, Please Reply With Your PIN
        """
    def testPinLogic(self):
        self._register("pin_logic", "001", "5555")
        script = """
            pin_logic > iavi uganda
            pin_logic < Hello, Please Reply With Your PIN
            pin_logic > 1234
            # I would prefer this response was improved
            pin_logic < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again
            pin_logic > 1235
            pin_logic < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again
            # succeed
            pin_logic > 5555
            pin_logic < Did you have sex with your main partner in the last 24 hours? 
        """
        self.runScript(script)
        # test that 5 times and you get bounced
        self._register("pin_logic_2", "002", "6666")
        script = """    
            pin_logic_2 > iavi uganda
            pin_logic_2 < Hello, Please Reply With Your PIN
            pin_logic_2 > 1234
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again
            pin_logic_2 > 1235
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again
            pin_logic_2 > 5555
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again
            pin_logic_2 > abcd
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again 
            pin_logic_2 > 7777
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again
            pin_logic_2 < Sorry, invalid answer 5 times. Your session will now end. Please try again later.
            # make sure we got bounced and test the other tree
            pin_logic_2 > iavi kenya
            pin_logic_2 < Hello, Please Reply With Your PIN
            pin_logic_2 > 1234
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again 
            pin_logic_2 > 1235
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again 
            pin_logic_2 > 5555
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again 
            pin_logic_2 > abcd
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again 
            pin_logic_2 > 7777
            pin_logic_2 < Sorry, that wasn't the right PIN. Please try sending your 4-digit PIN again 
            pin_logic_2 < Sorry, invalid answer 5 times. Your session will now end. Please try again later.
        """
        self.runScript(script)
    
    def testUgandaBasic(self):
        self._register("ugb_1")
        script = """
            # base case
            ugb_1 > iavi uganda
            ugb_1 < Hello, Please Reply With Your PIN
            ugb_1 > 1234
            ugb_1 < Did you have sex with your main partner in the last 24 hours?
            ugb_1 > yes
            ugb_1 < Did you use a condom?
            ugb_1 > YES
            ugb_1 < Did you have sex with any other partner in the last 24 hours?
            ugb_1 > no
            ugb_1 < Questionnaire is complete. Thank you.
        """
        self.runScript(script)
        
    def testUgandaLocalization(self):
        # and again in another language
        self._register(**{"phone":"ugb_2", "id": "002", "language":"lg"})
        script = """
            ugb_2 > iavi uganda
            ugb_2 < Ssebo/Nnyabo Yingiza ennamba yo eye'kyaama mu ssimu yo. Era ennamba eyo giwereze ku kompyuta yaffe.
            ugb_2 > 1234
            ugb_2 < Wetabyeeko mu kikolwa eky'omukwano n'omwagalwawo gw'olinaye mukunoonyereza kuno mu lunaku lumu oluyise?
            ugb_2 > yes
            ugb_2 < Mwakozesezza kondomu?
            ugb_2 > yes
            ugb_2 < Wetabyeeko mu kikolwa ky'omukwano n'omwagalwawo omulala yenna mu lunaku lumu oluyise?
            ugb_2 > no
            ugb_2 < Ebibuuzo bino bikomemye wano. Webale nnyo kuwaayo budde bwo.
        """
        self.runScript(script)
        
    def testKenyaBasic(self):
        self._register("kenya_1")
        script = """
            # base case
            kenya_1 > iavi kenya
            kenya_1 < Hello, Please Reply With Your PIN
            kenya_1 > 1234
            kenya_1 < How many times did you have sex in the last 24 hours?
            kenya_1 > 2
            kenya_1 < Of the number of times that you had sex in the last 24 hours, how many times were condoms used?
            kenya_1 > 2
            kenya_1 < Interview is complete. Remember to use a new condom each time you have sex and take your pills as agreed. Thank you
            kenya_1 > iavi kenya
            kenya_1 < Hello, Please Reply With Your PIN
            kenya_1 > 1234
            kenya_1 < How many times did you have sex in the last 24 hours?
            # 0 should skip the next question
            kenya_1 > 0
            kenya_1 < Interview is complete. Remember to use a new condom each time you have sex and take your pills as agreed. Thank you
        """
        self.runScript(script)
        
        # test other cases
        script = """
            kenya_1 > iavi kenya
            kenya_1 < Hello, Please Reply With Your PIN
            kenya_1 > 1234
            kenya_1 < How many times did you have sex in the last 24 hours?
            kenya_1 > 50
            # this is ugly too.
            kenya_1 < "50" is not a valid answer. You must enter a number between 0 and 19
            kenya_1 > a
            kenya_1 < "a" is not a valid answer. You must enter a number between 0 and 19
            kenya_1 > -3
            kenya_1 < "-3" is not a valid answer. You must enter a number between 0 and 19
            kenya_1 < Sorry, invalid answer 3 times. Your session will now end. Please try again later.
            kenya_1 > iavi kenya
            kenya_1 < Hello, Please Reply With Your PIN
            kenya_1 > 1234
            kenya_1 < How many times did you have sex in the last 24 hours?
            kenya_1 > 5
            kenya_1 < Of the number of times that you had sex in the last 24 hours, how many times were condoms used?
            kenya_1 > a
            kenya_1 < "a" is not a valid answer. You must enter a number less than or equal to the previous answer
            kenya_1 > 6
            kenya_1 < "6" is not a valid answer. You must enter a number less than or equal to the previous answer
            kenya_1 > -1
            kenya_1 < "-1" is not a valid answer. You must enter a number less than or equal to the previous answer
            kenya_1 < Sorry, invalid answer 3 times. Your session will now end. Please try again later.
        """
        self.runScript(script)
        
    def testKenyaLocalization(self):
        # and again in another language
        self._register(**{"phone":"kenya_2", "id": "002", "language":"sw"})
        script = """
            kenya_2 > iavi kenya
            kenya_2 < Tafadhali peana jibu ukitumia nambari yako binafsi ya kujitambulisha
            kenya_2 > 1234
            kenya_2 < Umefanya mapenzi mara ngapi kwa masaa ishirini na nne iliopita?
            kenya_2 > 2
            kenya_2 < Kwa masaa hiyo kumi na nne iliopita, ulitumia mipira ya Kondom mara ngapi ulipofanya mapenzi?
            kenya_2 > 2
            kenya_2 < Maswali yamekwisha. Kumbuka kutumia mpira mpya wa kondom kila unavyo fanya mapenzi na kumeza dawa kama ulivyoshauriwa. Asante sana
        """
        self.runScript(script)
        # test error messages
        script = """
            kenya_2 > iavi kenya
            kenya_2 < Tafadhali peana jibu ukitumia nambari yako binafsi ya kujitambulisha
            kenya_2 > 1235
            kenya_2 < Samahani, nambari uliyopeana sio sahihi. Tafadhali jaribu kubonyeza nambari yako ya kujitambulisha tena
            kenya_2 > 1234
            kenya_2 < Umefanya mapenzi mara ngapi kwa masaa ishirini na nne iliopita?
            kenya_2 > abc
            kenya_2 < "abc" sio jibu sahihi. Lazima ubonyeze nambari kati ya sufuri hadi kumi na tisa
            kenya_2 > 2
            kenya_2 < Kwa masaa hiyo kumi na nne iliopita, ulitumia mipira ya Kondom mara ngapi ulipofanya mapenzi?
            kenya_2 > 6
            kenya_2 < "6" silo jibu sahihi. Lazima ubonyeze nambari inayolingana au iliyo chini ya jibu uliopeana hapo awali
            kenya_2 > 6
            kenya_2 < "6" silo jibu sahihi. Lazima ubonyeze nambari inayolingana au iliyo chini ya jibu uliopeana hapo awali
            kenya_2 > 6
            kenya_2 < "6" silo jibu sahihi. Lazima ubonyeze nambari inayolingana au iliyo chini ya jibu uliopeana hapo awali
            kenya_2 < Samahani, jibu lisilo sahihi mara 3. Muda wako umekwisha. Tafadhali jaribu tena baadaye
        """
        self.runScript(script)
    
    def testSessionListeners(self):
        self._register("session_listener")
        self._register("session_listener_2", "002")
        self.assertEqual(0, len(Report.objects.all()))
        script = """ 
            session_listener > iavi kenya
            session_listener < Hello, Please Reply With Your PIN
            session_listener_2 > iavi uganda
            session_listener_2 < Hello, Please Reply With Your PIN
        """
        self.runScript(script)
        # make sure the report got created
        self.assertEqual(2,len(Report.objects.all()))
        self.assertEqual(1,len(KenyaReport.objects.all()))
        self.assertEqual(1,len(UgandaReport.objects.all()))
        
        # make sure it's the right person/type
        k_report = KenyaReport.objects.all()[0]
        u_report = UgandaReport.objects.all()[0]
        self.assertEqual("session_listener", k_report.reporter.connection().identity)
        self.assertEqual(None, u_report.completed)
        self.assertEqual(None, k_report.completed)
        
        self.assertEqual("session_listener_2", u_report.reporter.connection().identity)
        
        # ok let's finish the sessions now
        # and make sure all the data is set
        script = """ 
            session_listener > 1234
            session_listener < How many times did you have sex in the last 24 hours?
            session_listener > 5
            session_listener < Of the number of times that you had sex in the last 24 hours, how many times were condoms used?
            session_listener > 2
            session_listener < Interview is complete. Remember to use a new condom each time you have sex and take your pills as agreed. Thank you
        """
        self.runScript(script)
        k_report = KenyaReport.objects.all()[0]
        self.assertNotEqual(None, k_report.completed)
        self.assertTrue(k_report.completed > k_report.started)
        self.assertEqual(5, k_report.sex_past_day)
        self.assertEqual(2, k_report.condoms_past_day)
        self.assertEqual("F", k_report.status)
        
        script = """ 
            session_listener_2 > 1234
            session_listener_2 < Did you have sex with your main partner in the last 24 hours?
            session_listener_2 > NO!
            session_listener_2 < Did you have sex with any other partner in the last 24 hours?
            session_listener_2 > yep
            session_listener_2 < Did you use a condom?
            session_listener_2 > yessir
            session_listener_2 < Questionnaire is complete. Thank you.
        """
        self.runScript(script)
        u_report = UgandaReport.objects.all()[0]
        self.assertNotEqual(None, u_report.completed)
        self.assertTrue(u_report.completed > u_report.started)
        self.assertEqual(False, u_report.sex_with_partner)
        self.assertEqual(None, u_report.condom_with_partner)
        self.assertEqual(True, u_report.sex_with_other)
        self.assertEqual(True, u_report.condom_with_other)
        self.assertEqual("F", u_report.status)
        
        
         
    def _register(self, phone="55555", id="001", pin="1234", location= "22", language="En"):
        """ Register a user, via the test script. """
        script = """
            # base case - everything's all good
            %(phone)s > *#%(language)s#%(location)s#%(id)s#*
            %(phone)s < Confirm %(id)s Registration is Complete
            %(phone)s < Please Enter Your PIN Code
            %(phone)s > %(pin)s
            %(phone)s < Please Enter Your PIN Code Again
            %(phone)s > %(pin)s
            %(phone)s < Thank You. Your PIN Has Been Set
        """ % ({"phone": phone, "id": id, "pin": pin, "language":language, "location": location } )
        self.runScript(script)
        return IaviReporter.objects.get(alias=IaviReporter.get_alias(location, id))
        