#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import re
import rapidsms
from models import *


class App(rapidsms.app.App):
    def __join_Qs(self, sequence):
        strs = map(lambda x: "Q%d" % x, sequence)
        
        # join all items in the sequence with
        # commans, except for the last one...
        flat = ", ".join(strs[0:-1])
        
        # append an "and" to link the last item,
        # unless there's nothing to link with
        if flat: flat += " and "
        
        # returns A, B, C, and D
        return flat + unicode(strs[-1])
    
    
    def handle(self, msg):
        for sect_obj in Section.objects.all():
            
            # attempt to match the incoming text against
            # this section's pattern. at this point, any
            # msg prefixed with a section pattern will do
            s_pat = r"^\s*(?:%s)\b(.*)$" % (sect_obj.prefix)
            sm = re.match(s_pat, msg.text, re.IGNORECASE)
            if sm is not None:
                
                # since we don't know what groups might be lurking
                # in sect_obj.prefix, assume that the LAST matched
                # group is the submission text
                text = str(sm.groups()[-1]).strip()
                self.info("Grabbed message: Section=%s, Text=%r" %
                    (sect_obj, text))
                
                # maybe the message has a Location attached
                # ...or maybe it doesn't. either way, store
                # it (or None) alongside the submission
                loc = getattr(msg, "location", None)
                
                # regardless of whether the submission was
                # valid or not, we want to keep hold of it
                sub_obj = Submission.objects.create(
                    section=sect_obj,
                    location=loc,
                    raw_text=text,
                    **msg.persistance_dict)
                
                # build an array of answers, by extracing
                # a single "Qn. Whatever" token from the
                # end of the text, until none are left
                answers = []
                while True:
                    q_pat = r"(.*)Q(\d+)\.?(.+?)$"
                    qm = re.match(q_pat, text, re.IGNORECASE)
                    if qm is None: break
                    
                    # we found an answer! store it, modify the
                    # text (replace it with the remainder)
                    text, number, answer = qm.groups()
                    answers.insert(0, (int(number), answer.strip()))
                
                self.info("Raw Answers: %r" % (answers))
                
                # if no answers were found, the caller probably
                # formatted the message wrong, so return an error
                # TODO: try to deduce their error heuristically
                if not answers:
                    return msg.respond(
                        ("Sorry, I couldn't understand your report.\n" +
                        "It should look like: %s Q1 answer Q2 answer") %
                            (sect_obj.code))
                
                answer_objects = []
                invalid_nums = []
                
                # iterate the answers that we just extracted,
                # which are still just chunks of raw text
                for num, text in answers:
                    try:
                    
                        # (attempt to) fetch the question object via
                        # its number. TODO: sub-questions? (1a, 1b, etc)
                        que_obj = Question.objects.get(
                            section=sect_obj,
                            number=num)
                            
                        # store the answer itself as raw text,
                        # since questions are untyped. casting
                        # happens when we want to VIEW the data
                        answer_objects.append(
                            Answer.objects.create(
                                submission=sub_obj,
                                question=que_obj,
                                raw_text=text))
                    
                    # the question number was invalid!
                    except Question.DoesNotExist:
                        invalid_nums.append(num)
                
                
                # normalize each of the answers, and store
                # the question numbers of those that returned
                # None (couldn't be parsed)
                invalid_answers = [
                    answ.question.number
                    for answ in answer_objects
                    if answ.normalized is None]
                
                # always acknowledge all answers, regardless of whether
                # they were successful or not. they're still stored, so
                # might turn out to be useful later. unfortunately, we
                # must use the section CODE here, because the title can
                # be really, really long...
                response = "Thank you for %d answers to the %s section" %\
                    (len(answers), sect_obj.code)
                
                # if anything went wrong, then we're going
                # to need to build a n error message
                if invalid_nums or invalid_answers:
                    response += ", but "
                    errors = []
                    
                    # answers which were stored, but failed normalization
                    # it's possible that this a bug, but warn anyway
                    if invalid_answers:
                        plural = len(invalid_answers) > 1
                        errors.append("%s %s invalid" %
                            (self.__join_Qs(invalid_answers), # 1, 2, 3 and 4
                             "were" if plural else "was"))    # 1 was, 2 were
                    
                    # answers to questions that don't exist
                    # (a typo like an extra or missing number?)
                    if invalid_nums:
                        plural = len(invalid_nums) > 1
                        errors.append("%s %s not exist" %
                            (self.__join_Qs(invalid_nums), # 97, 98 and 99
                             "do" if plural else "does"))  # 1 does, 2 do
                    
                    # append the errors (one or both)
                    response += ", and ".join(errors) + "."
                
                
                # send the compiled response back to the reporter
                return msg.respond(response)
        
        # no section was matched, so
        # assume this message was not
        # for us...
        return False
