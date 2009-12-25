import rapidsms
import re
from rapidsms.connection import Connection 
from rapidsms.message import Message
from reporters.models import Reporter, Location
from models import *
from i18n.utils import get_translation as _
from i18n.utils import get_language_code
from strings import strings
import threading
import time
from datetime import datetime, timedelta
from datetime import time as dtt

class App (rapidsms.app.App):
    
    tree_app = None
    pending_pins = {}
    def start (self):
        """Configure your app in the start phase."""
        # we have to register our functions with the tree app
        self.tree_app = self.router.get_app("tree")
        self.tree_app.register_custom_transition("validate_pin", self.validate_pin)
        self.tree_app.register_custom_transition("validate_1_to_19", self.validate_1_to_19)
        self.tree_app.register_custom_transition("validate_num_times_condoms_used", 
                                                 self.validate_num_times_condoms_used)
        
        self.tree_app.set_session_listener("iavi uganda", self.uganda_session)
        self.tree_app.set_session_listener("iavi kenya", self.kenya_session)
        
        # interval to check for new surveys (in seconds)
        survey_interval = 60
        # start a thread for initiating surveys
        survey_thread = threading.Thread(
                target=self.survey_initiator_loop,
                args=(survey_interval,))
        survey_thread.daemon = True
        survey_thread.start()
        
    def parse (self, message):
        """Parse and annotate messages in the parse phase."""
        pass

    def handle (self, message):
        # there are three things this app deals with primarily:
        # registration, pin setup, and testing
        
        # but we'll also use it to circumvent some logic in the tree
        # app with a few custom codes.
        if message.text.lower() == "iavi uganda" or message.text.lower() == "iavi kenya":
            # if they are allowed to participate, return false so 
            # that the message propagates to the tree app.  If they
            # aren't this will come back as handled and the tree app
            # will never see it.  
            # ASSUMES ORDERING OF APPS AND THAT THIS IS BEFORE TREE
            return not self._allowed_to_participate(message)
        
        # we'll be using the language in all our responses so
        # keep it handy
        language = get_language_code(message.persistant_connection)
        
        # check pin conditions and process if they match
        if message.reporter and message.reporter.pk in self.pending_pins:
            return self._process_pin(message)
            
        # registration block
        # first make sure the string starts and ends with the *# - #* combination
        match = re.match(r"^\*\#(.*?)\#\*$", message.text)
        if match:
            self.info("Message matches! %s", message)
            body_groups = match.groups()[0].split("#")
            if len(body_groups)== 3 and body_groups[0] == "8377":
                # this is the testing format
                # this is the (extremely ugly) format of testing
                # *#8377#<Site Number>#<Last 4 Digits of Participant ID>#*
                # TODO: implement testing
                
                code, site, id = body_groups
                alias = IaviReporter.get_alias(site, id)
                try: 
                    # lookup the user in question and initiate the tree
                    # sequence for them.  If there are errors, respond
                    # with them
                    user = IaviReporter.objects.get(alias=alias)
                    
                    errors = self._initiate_tree_sequence(user, message.persistant_connection)
                    if errors:
                        message.respond(errors)
                except IaviReporter.DoesNotExist:
                    message.respond(_(strings["unknown_user"], language) % {"alias":id})
                return True
            
            else:
                # assume this is the registration format
                # this is the (extremely ugly) format of registration
                # time is optional
                # *#<Country/Language Group>#<Site Number>#<Last 3 Digits of Participant ID>#<time?>#*
                if len(body_groups) == 3:
                    language, site, id = body_groups
                    study_time = "1600"
                elif len(body_groups) == 4:
                    language, site, id, study_time = body_groups
                else:
                    message.respond(_(strings["unknown_format"], get_language_code(message.persistant_connection)))
                
                # validate the format of the id, existence of location
                if not re.match(r"^\d{3}$", id):
                    message.respond(_(strings["id_format"], get_language_code(message.persistant_connection)) % {"alias" : id})
                    return True
                try:
                    location = Location.objects.get(code=site)
                except Location.DoesNotExist:
                    message.respond(_(strings["unknown_location"], get_language_code(message.persistant_connection)) % {"alias" : id, "location" : site})
                    return True
                
                # TODO: validate the language
                
                # validate and get the time object
                if re.match(r"^\d{4}$", study_time):
                    hour = int(study_time[0:2])
                    minute = int(study_time[2:4])
                    if hour < 0 or hour >= 24 or minute < 0 or minute >= 60:
                        message.respond(_(strings["time_format"], get_language_code(message.persistant_connection)) % {"alias" : id, "time" : study_time})
                        return
                    real_time = dtt(hour, minute)
                else:
                    message.respond(_(strings["time_format"], get_language_code(message.persistant_connection)) % {"alias" : id, "time" : study_time})
                    return 
                
                # user ids are unique per-location so use location-id
                # as the alias
                alias = IaviReporter.get_alias(location.code, id)
                
                # make sure this isn't a duplicate alias
                if len(IaviReporter.objects.filter(alias=alias)) > 0:
                    message.respond(_(strings["already_registered"], language) % {"alias": id, "location":location.code})
                    return True
                
                # create the reporter object for this person 
                reporter = IaviReporter(alias=alias, language=language, location=location, registered=message.date)
                reporter.save()
                
                # create the study participant for this too.  Assume they're starting
                # tomorrow and don't set a stop date.  
                start_date = (datetime.today() + timedelta(days=1)).date()
                participant = StudyParticipant.objects.create(reporter=reporter, 
                                                              start_date = start_date,
                                                              notification_time = real_time)
                
                # also attach the reporter to the connection 
                message.persistant_connection.reporter=reporter
                message.persistant_connection.save()
                
                message.respond(_(strings["registration_complete"], language) % {"alias": id })
                
                # also send the PIN request and add this user to the 
                # pending pins
                self.pending_pins[reporter.pk] = None
                message.respond(_(strings["pin_request"], language))
        else:
            self.info("Message doesn't match. %s", message)
            # this is okay.  one of the other apps may yet pick it up
            
    
    def cleanup (self, message):
        """Perform any clean up after all handlers have run in the
           cleanup phase."""
        pass

    def outgoing (self, message):
        """Handle outgoing message notifications."""
        pass

    def stop (self):
        """Perform global app cleanup when the application is stopped."""
        pass
    
    def _allowed_to_participate(self, message):
        if message.reporter:
            iavi_reporter = IaviReporter.objects.get(pk=message.reporter.pk)
            if iavi_reporter.pin:
                return True
            else:
                message.respond(_(strings["rejection_no_pin"], get_language_code(message.persistant_connection)))
        else:
            message.respond(_(strings["rejection_unknown_user"], get_language_code(message.persistant_connection)))
        return False
            
    def _process_pin(self, message):
        language = get_language_code(message.persistant_connection)
        incoming_pin = message.text.strip()
        reporter = IaviReporter.objects.get(pk=message.reporter.pk)
        if self.pending_pins[reporter.pk]:
            # this means it has already been set once 
            # check if they are equal and if so save
            pending_pin = self.pending_pins.pop(reporter.pk)
            if incoming_pin == pending_pin:
                # success!
                reporter.pin = pending_pin
                reporter.save()
                message.respond(_(strings["pin_set"], language))
            else:
                # oops they didn't match.  send a failure string
                message.respond(_(strings["pin_mismatch"], language) % {"alias": reporter.study_id})
                # put an empty value back in the list of pins
                self.pending_pins[reporter.pk] = None
        else:
            # this is their first try.  make sure 
            # it's 4 numeric digits and if so ask for confirmation
            if re.match(r"^(\d{4})$", incoming_pin):
                self.pending_pins[reporter.pk] = incoming_pin
                message.respond(_(strings["pin_request_again"], language))
            else:
                # bad format.  send a failure string and prompt again
                message.respond(_(strings["bad_pin_format"], language) % {"alias": reporter.study_id})
        return True
    
    def _initiate_tree_sequence(self, user, initiator=None):
        user_conn = user.connection()
        if user_conn:
            db_backend = user_conn.backend
            # we need to get the real backend from the router 
            # to properly send it 
            real_backend = self.router.get_backend(db_backend.slug)
            if real_backend:
                connection = Connection(real_backend, user_conn.identity)
                text = self._get_tree_sequence(user)
                if not text:
                    return _(strings["unknown_survey_location"], get_language_code(user.connection)) % ({"location":user.location, "alias":user.study_id})
                else:
                    # first ask the tree app to end any sessions it has open
                    if self.tree_app:
                        self.tree_app.end_sessions(user_conn)
                    if initiator:
                        # if this was initiated by someone else
                        # create an entry for this so they can be
                        # notified upon completion, and also so 
                        # we can ignore the data
                        TestSession.objects.create(initiator=initiator, tester=user,
                                                   status="A")
                    start_msg = Message(connection, text)
                    self.router.incoming(start_msg)
                    return
            else:
                error = "Can't find backend %s.  Messages will not be sent" % connection.backend.slug
                self.error(error)
                return error
        else:
            error = "Can't find connection %s.  Messages will not be sent" % user_conn
            self.error(error)
            return error

    def _get_tree_sequence(self, user):
        # this is very hacky
        if user.location.type.name == "Kenya Location":
            return "iavi kenya"
        elif  user.location.type.name == "Uganda Location":
            return "iavi uganda"
        else:
            return None
    
    def _get_column(self, state):
        # this is just hard coded. *sigh*
        if state.name == "uganda_main_1": 
            return "sex_with_partner" 
        elif state.name == "uganda_main_2": 
            return "condom_with_partner" 
        if state.name == "uganda_main_3": 
            return "sex_with_other" 
        if state.name == "uganda_main_4": 
            return "condom_with_other" 
        if state.name == "kenya_main_1": 
            return "sex_past_day" 
        if state.name == "kenya_main_2": 
            return "condoms_past_day" 
        
        return None

    def _get_clean_answer(self, answer, value):
        # this is just hard coded. *sigh*
        if answer.name == "pin validation":
            return value
        elif answer.name == "1 to 19" or\
            answer.name == "times condoms used":
            return int(value)
        elif answer.name == "zero":
            return 0
        elif answer.name == "uganda no":
            return False
        elif answer.name == "uganda yes":
            return True
        
    # this region for session listeners
    
    def uganda_session(self, session, is_ending):
        self._handle_session(session, is_ending, UgandaReport)

    def kenya_session(self, session, is_ending):
        self._handle_session(session, is_ending, KenyaReport)

        
    def _handle_session(self, session, is_ending, klass):
        self.debug("%s session: %s" % (klass, session))
        
        # get the reporter object
        reporter = session.connection.reporter
        iavi_reporter = IaviReporter.objects.get(pk=reporter.pk)
            
        if not is_ending:
            # check if the reporter has an active test session
            # and if so, link it. Otherwise treat it normally
            try: 
                test_session = TestSession.objects.get(tester=iavi_reporter, 
                                                  status="A")
                test_session.tree_session = session
                test_session.save()
            except TestSession.DoesNotExist:
                # not an error, just means this wasn't a test
                # create a new report for this
                klass.objects.create(reporter=iavi_reporter, 
                                 started=session.start_date, 
                                 session=session, status="A")
            
        else:
            # if we have a test session mark the status and save
            try:
                test_session = TestSession.objects.get(tree_session=session)
                if session.canceled:
                    test_session.status = "F"
                    response = _(strings["test_fail"], get_language_code(test_session.initiator)) % ({"alias": iavi_reporter.study_id})
                else:
                    test_session.status = "P"
                    response = _(strings["test_pass"], get_language_code(test_session.initiator)) % ({"alias": iavi_reporter.study_id})
                
                test_session.save()
                
                # also have to initiate a callback to the 
                # original person who initiated the test
                db_backend = test_session.initiator.backend
                real_backend = self.router.get_backend(db_backend.slug)
                if real_backend:
                    real_connection = Connection(real_backend, test_session.initiator.identity)
                    response_msg = Message(real_connection, response)
                    self.router.outgoing(response_msg)
                else:
                    error = "Can't find backend %s.  Messages will not be sent" % connection.backend.slug
                    self.error(error)
            except TestSession.DoesNotExist:
                # not a big deal.  it wasn't a test.  
                # if we have a report
                # update the data and save
                try:
                    report = klass.objects.get(session=session)
                    for entry in session.entry_set.all():
                        answer = entry.transition.answer
                        column = self._get_column(entry.transition.current_state)
                        if column:
                            clean_answer = self._get_clean_answer(answer, entry.text)
                            setattr(report, column, clean_answer)
                    report.completed = datetime.now()
                    if session.canceled:
                        report.status = "C"
                    else:
                        report.status = "F"
                    report.save()
                except klass.DoesNotExist:
                    # oops, not sure how this could happen, but we don't
                    # want to puke
                    self.error("No report found for session %s" % session)
    
    
    # this region is for the validation logic
    
    def validate_pin(self, msg):
        rep = IaviReporter.objects.get(pk=msg.reporter.pk)
        return msg.text == rep.pin
    
    # we need to save these in order to validate the other
    sex_answers = {}
    
    def validate_1_to_19(self, msg):
        value = msg.text.strip()
        if value.isdigit():
            if 0 < int(value) < 20:
                self.sex_answers[msg.reporter.pk] = int(value)
                return True
        return False
    
    def validate_num_times_condoms_used(self, msg):
        value = msg.text.strip()
        if value.isdigit():
            old_value = self.sex_answers.get(msg.reporter.pk)
            if not old_value:
                # this should never happen unless we were
                # interrupted between questions. we could
                # look this up in the DB but for now we'll
                # be dumb.  
                # TODO: do this for real from the DB
                old_value = 20
            if 0 <= int(value) <= old_value:
                self.sex_answers.pop(msg.reporter.pk)
                return True
        return False
        
    # Survey Initiator Thread --------------------
    def survey_initiator_loop(self, seconds=60):
        '''This loops and initiates surveys with registered participants
           based on some criteria (like daily)'''
        self.info("Starting survey initiator...")
        prev_time = (datetime.now() + timedelta(hours=2)).time()
        while True:
            # wait for the time to pass when they registered to start a survey
            # and when it is, start it
            
            try: 
                # super hack... add 3 hours because of the time zone difference
                # i'm sure there is a better way to do this with real time zones
                # but i'm also sure I don't want to figure it out right nowx 
                now_adjusted =  datetime.now() + timedelta(hours=2) 
                next_time = now_adjusted.time()
                self.debug("Adjusted time: %s, checking for participants to notify" % next_time)
                # conditions are that the 
                # notification time is between the previous seen time
                # and the next time, the start date was sometime before
                # or equal to today, and the end date is either null
                # or after or equal to today
                to_initiate = StudyParticipant.objects.filter\
                    (notification_time__gt=prev_time).filter\
                    (notification_time__lte=next_time).filter\
                    (start_date__lte=now_adjusted.date())
                for participant in to_initiate:
                    self.debug("Initiating sequence for %s" % participant.reporter);
                    try:
                        errors = self._initiate_tree_sequence(participant.reporter) 
                        # unfortunately I'm not sure what else we can do if something
                        # goes wrong here
                        if errors:
                            self.debug("unable to initiate sequence for %s" % participant)
                            self.error(errors)
                    except Exception, e:
                        self.debug("unable to initiate sequence for %s" % participant)
                        self.error(e)
                    
                #update the previous time
                prev_time = next_time
                
            except Exception, e:
                # if something goes wrong log it, but don't kill the entire loop
                self.debug("survey initiation loop failure")
                self.debug(e)
            # wait until it's time to check again
            time.sleep(seconds)

    