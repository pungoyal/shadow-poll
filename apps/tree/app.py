#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import rapidsms
from models import *
from reporters.models import Reporter
from internationalization.utils import get_translation as _
#from internationalization.utils import get_language_from_connection as lang
from internationalization.utils import get_language_from_message as lang
from register.models import Registration

class App(rapidsms.app.App):
    
    registered_functions = {}
    session_listeners = {}
    
    def start(self):
        pass
    
    def configure(self, last_message="You are done with this survey.  Thanks for participating!", **kwargs):
        self.last_message = last_message
    
    def handle(self, msg):
        # if this caller doesn't have a session attribute,
        # they're not currently answering a question tree, so
        # just search for triggers and return
        sessions = Session.objects.all().filter(state__isnull=False)\
            .filter(connection=msg.persistant_connection)
        if not sessions:
            try:
                tree = Tree.objects.get(trigger=msg.text)
                # start a new session for this person and save it
                session = Session(connection=msg.persistant_connection, 
                                  tree=tree, state=tree.root_state, num_tries=0)
                session.save()
                self.debug("session %s saved" % session)
                
                # also notify any session listeners of this
                # so they can do their thing
                if self.session_listeners.has_key(tree.trigger):
                    for func in self.session_listeners[tree.trigger]:
                        func(session, False)
            
            # no trigger found? no big deal. the
            # message is probably for another app
            except Tree.DoesNotExist:
                return False
        
        # the caller is part-way though a question
        # tree, so check their answer and respond
        else:
            session = sessions[0]
            state = session.state
            
            self.debug(state)
            options =  state.question.get_choices(msg.text, ",")
            # loop through all transitions starting with  
            # this state and try each one depending on the type
            # this will be a greedy algorithm and NOT safe if 
            # multiple transitions can match the same answer
            found_transition = state.get_transition(options)
            # the number of tries they have to get out of this state
            # if empty there is no limit.  When the num_retries is hit
            # a user's session will be terminated.
    
            # not a valid answer, so remind
            # the user of the valid options.
            if not found_transition:
                transitions = Transition.objects.filter(current_state=state)
                # there are no defined answers.  therefore there are no more questions to ask 
                if len(transitions) == 0:
                    # send back some precanned response
                    msg.respond(self.last_message)
                    # end the connection so the caller can start a new session
                    self._end_session(session)
                    return
                else:
                    # send them some hints about how to respond
                    if state.question.error_response:
                        response = (_(state.question.error_response, lang(msg)))
                        if "%(answer)s" in response:
                            response = response % ({"answer" : msg.text})
                    else:
                        flat_answers = " or ".join([trans.answer.helper_text() for trans in transitions])
                        translated_answers = _(flat_answers, lang(msg))
                        response = _('"%(answer)s" is not a valid answer. You must enter %(hint)s', 
                                     lang(msg))% ({"answer" : msg.text, "hint": translated_answers})
                         
                    msg.respond(response)
                    
                    # update the number of times the user has tried
                    # to answer this.  If they have reached the 
                    # maximum allowed then end their session and
                    # send them an error message.
                    session.num_tries = session.num_tries + 1
                    if state.num_retries and session.num_tries >= state.num_retries:
                        session.state = None
                        msg.respond(_("Sorry, invalid answer %(retries)s times. Your session will now end. Please try again later.",
                                      lang(msg)) % {"retries": session.num_tries })
                        
                    session.save()
                    return True
            
            # create an entry for this response
            # first have to know what sequence number to insert
            last_registered_list = Registration.objects.filter(phone = msg.persistant_connection).order_by('date')
            last_registered = None
            if(len(last_registered_list) > 0):
                last_registered = last_registered_list[0].phone
            ids = Entry.objects.all().filter(session=session).order_by('sequence_id').values_list('sequence_id', flat=True)
            if ids:
                # not sure why pop() isn't allowed...
                sequence = ids[len(ids) -1] + 1
            else:
                sequence = 1
            entry = Entry(session=session,sequence_id=sequence,transition=found_transition,text=str(options), uid = last_registered)
            entry.save()
            self.debug("entry %s saved" % entry)
                
            # advance to the next question, or remove
            # this caller's state if there are no more
            
            # this might be "None" but that's ok, it will be the 
            # equivalent of ending the session
            session.state = found_transition.next_state
            session.num_tries = 0
            session.save()
            
            # if this was the last message, end the session, 
            # and also check if the tree has a defined 
            # completion text and if so send it
            if not session.state:
                self._end_session(session)
                if session.tree.completion_text:
                    msg.respond(_(session.tree.completion_text, lang(msg)))
                
        # if there is a next question ready to ask
        # (and this includes THE FIRST), send it along
        sessions = Session.objects.all().filter(state__isnull=False).filter(connection=msg.persistant_connection)
        if sessions:
            state = sessions[0].state
            if state.question:
                msg.respond(_(state.question.text, lang(msg)))
                self.info(_(state.question.text, lang(msg)))
        
        # if we haven't returned long before now, we're
        # long committed to dealing with this message
        return True

    def _end_session(self, session, canceled=False):
        '''Ends a session, by setting its state to none,
           and alerting any session listeners'''
        session.state = None
        session.canceled = canceled
        session.save()
        if self.session_listeners.has_key(session.tree.trigger):
            for func in self.session_listeners[session.tree.trigger]:
                func(session, True)
                    
    def end_sessions(self, connection):
        ''' Ends all open sessions with this connection.  
            does nothing if there are no open sessions ''' 
        sessions = Session.objects.filter(connection=connection).exclude(state=None)
        for session in sessions:
            self._end_session(session, True)
            
    def register_custom_transition(self, name, function):
        ''' Registers a handler for custom logic within a 
            state transition '''
        self.info("Registering keyword: %s for function %s" %(name, function.func_name))
        self.registered_functions[name] = function  
        
    def set_session_listener(self, tree_key, function):
        '''Adds a session listener to this.  These functions
           get called at the beginning and end of every session.
           The contract of the function is func(Session, is_ending)
           where is_ending = false at the start and true at the
           end of the session.
        ''' 
        
        self.info("Registering session listener %s for tree %s" %(function.func_name, tree_key))
        # I can't figure out how to deal with duplicates, so only allowing
        # a single registered function at a time.
#        
#        if self.session_listeners.has_key(tree_key):
#            # have to check existence.  This is mainly for the unit tests
#            if function not in self.session_listeners[tree_key]:
#                self.session_listeners[tree_key].append(function)
#        else: 
        self.session_listeners[tree_key] = [function]
