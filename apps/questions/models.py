#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import re
from django.db import models
from locations.models import Location
from reporters.models import PersistantConnection, Reporter


class Section(models.Model):
    title   = models.CharField(max_length=100)
    code    = models.CharField(max_length=30)
    pattern = models.CharField(max_length=100, blank=True,
        help_text="Any incoming message prefixed by a string matching this regexp " +
                  "is assumed to be reporting on this section. The CODE field is " +
                  "automatically prepended to this pattern.")
    
    def __unicode__(self):
        return self.title
    
    @property
    def prefix(self):
        if self.pattern:
            return("%s|(?:%s)" %
                (self.code, self.pattern))
        
        # no pattern was specified, so all
        # we need to look for is the code
        return self.code


class Question(models.Model):
    QUESTION_TYPES = (
        ("F", "Free text"),
        ("B", "Boolean"),
        ("N", "Numeric"),
        ("M", "Multiple choice"))
    
    type = models.CharField(max_length=1, choices=QUESTION_TYPES,
        help_text="<br>".join([
            "<b>Free Text</b> questions will accept any text, but can use Options to coerce expected answers into data.",
            "<b>Boolean</b> questions will accept TRUE or FALSE, in a variety of guises. Options are ignored.",
            "<b>Numeric</b> questions will accept any numeric (integer or decimal) value. Options are ignored.",
            "<b>Multiple Choice</b> questions will only accept a valid Option.",
        ]))
    
    section = models.ForeignKey(Section, related_name="questions")
    number  = models.IntegerField()
    text    = models.TextField()

    
    class Meta:
        ordering = ["section", "number"]
    
    def __unicode__(self):
        return "%s Q%d" % (
            self.section,
            self.number)
    
    
    @property
    def num_answers(self):
        return self.answers.count()
    
    @property
    def answer_percentage(self):
        sect_sub = self.section.submissions.count()
        if not sect_sub:
            return "0"
        
        return "%2d" % ((float(self.num_answers) / sect_sub) * 100)
    
    @property
    def last_answer(self):
        """Returns the latest Answer to this Question, via the linked Sumbmission
           object's _submission_ field,, or returns None is no Answers are linked."""
        
        try:
            return self.answers.all().order_by("-submission__submitted")[0]
        
        # if there were no Answer objects, accessing [0]
        # will raise an indexerror, so wrap and return
        # None, to indicate something like NO ANSWERS
        except IndexError:
            return None


class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options")
    text     = models.CharField(max_length=100)
    
    letters = models.CharField(max_length=10, blank=True,
        help_text="Any answer containing ONLY a letter from this field " +\
                  "is assumed to be referring to this option. Intended " +\
                  "for shortcuts like <b>1</b> or <b>a</b>.")
    
    words = models.TextField(blank=True,
        help_text="Enter one word per line. Any answer containing " +\
                  "a word is assumed to be referring to this option.")
    
    pattern = models.CharField(max_length=100, blank=True,
        help_text="Any answer matched by this pattern is " +\
                  "assumed to be referring to this option.")
    
    
    class Meta:
        ordering = ["id"]
    
    
    def __unicode__(self):
        return "Option to %s: %s" % (
            self.question,
            self.text)


    def match(self, text):
        if self.letters:
            if re.match(r"^(" + "|".join(self.letters) + r")\.?$", text, re.IGNORECASE):
                return True
        
        elif self.words:
            if re.match(r"^.*" + ("|".join(self.words.split("\n"))) + r".*$", text, re.IGNORECASE):
                return True
        
        elif self.pattern:
            if re.match(self.pattern, text, re.IGNORECASE):
                return True
        
        # if we haven't returned yet,
        # this option does not match
        return False

            


class Submission(models.Model):
    reporter   = models.ForeignKey(Reporter, null=True, related_name="submissions")
    connection = models.ForeignKey(PersistantConnection, null=True, related_name="submissions")
    location   = models.ForeignKey(Location, null=True, related_name="submissions")
    section    = models.ForeignKey(Section, related_name="submissions")
    submitted  = models.DateTimeField(auto_now_add=True)
    raw_text   = models.TextField()
    
    
    class Meta:
        ordering = ["-submitted"]
    
    def __unicode__(self):
        return "Submission by %s on %s" % (
            (self.reporter or self.connection),
            self.section)
    
    
    @property
    def reported_by(self):
        for x in [self.reporter, self.connection]:
            if x is not None:
                return x
        
        # this won't happen if the submission was
        # created by app.py, but it could have
        # been created in the admin... (?)
        return None
        
    
    @property
    def num_answers(self):
        return self.answers.count()


class Answer(models.Model):
    TRUE  = re.compile(r"^(?:[YT].*|1)$", re.IGNORECASE)
    FALSE = re.compile(r"^(?:[NF].*|0)$", re.IGNORECASE)
    
    submission = models.ForeignKey(Submission, related_name="answers")
    question   = models.ForeignKey(Question, related_name="answers")
    raw_text   = models.TextField()
    
    
    def __unicode__(self):
        return "Answer to %s: %s" % (
            self.question,
            self.raw_text)
    
    
    @property
    def normalized(self):
        text = self.raw_text.strip()
        type = self.question.type
        
        # free text
        if type == "F":
            
            # attempt to match an option
            # but it's no big deal if none do
            for opt in self.question.options.all():
                if opt.match(text):
                    return opt.text
            
            return text
        
        # boolean
        elif type == "B":
            if    self.TRUE.match(text):  return True
            elif  self.FALSE.match(text): return False
            else:                         return None
        
        # numeric
        elif type == "N":
            
            # attempt to cast the text to a 
            for func in [int, float]:
                try: return func(text)
                except: pass

            # the answer couldn't be cast to a
            # float or int, so return None (unknown)
            return None
        
        # multiple-choice
        elif type == "M":
            
            # match the text to an option or return
            # None (unknown) - it's a strict version of
            # "free text", when ambiguity is undesirable
            for opt in self.question.options.all():
                if opt.match(text):
                    return opt.text
            
            return None
            
        # nothing else is supported yet!
        else: return None
