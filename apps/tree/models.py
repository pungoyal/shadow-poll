#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.db import models
from reporters.models import Reporter, PersistantConnection
import re


class Question(models.Model):
    '''A question, which is just some text to be sent to the user,
       and an optional error message if the question is not answered
       properly'''
    text = models.TextField()
    # allow the question to specify a default error
    # message
)
    type = models.CharField(max_length=1, choices=ANSWER_TYPES)
    answer = models.CharField(max_length=160)
    description = models.CharField(max_length=100, null=True)
    
    def __unicode__(self):
        return self.answer
        #return "%s %s (%s)" % (self.helper_text(), self.type)
    
    def helper_text(self):
        if self.type == "A":
            if self.description:
                return "%s (%s)" % (self.answer, self.description)
            return self.answer
        if self.type == "R":
            if self.description:
                return self.description
            # this will be ugly
            return self.answer
        if self.type == "C":
            if self.description:
                return self.description
            # this might be ugly
            return self.answer
    

class TreeState(models.Model):
    """ A TreeState is a location in a tree.  It is 
        associated with a question and a set of answers
        (transitions) that allow traversal to other states.""" 
    name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, blank=True, null=True)
    # the number of tries they have to get out of this state
    # if empty there is no limit.  When the num_retries is hit
    # a user's session will be terminated.
    num_retries = models.PositiveIntegerField(blank=True,null=True)

    def has_loops_below(self):
        return TreeState.path_has_loops([self])
    
    @classmethod
    def path_has_loops(klass, path):
        # we're going to get all unique paths through the this
        # (or until we hit a loop)
        # a path is defined as an ordered set of states
        # if at any point in a path we reach a state we've 
        # already seen then we have a loop
        # this is basically a depth first search
        last_node = path[len(path) - 1]
        transitions = last_node.transition_set.all()
        for transition in transitions:
          if transition.next_state:
              # Base case.  We have already seen this state in the path
              if path.__contains__(transition.next_state):
                  return True
              next_path = path[:]
              next_path.append(transition.next_state)
              # recursive case - there is a loop somewhere below this path
              if TreeState.path_has_loops(next_path):
                  return True
        # we trickle down to here - went all the way through without finding any loops
        return False
        
    def add_all_unique_children(self, added):
        ''' Adds all unique children of the state to the passed in list.  
            This happens recursively.'''
        transitions = self.transition_set.all()
        for transition in transitions:
            if transition.next_state:
                if transition.next_state not in added:
                    added.append(transition.next_state)
                    transition.next_state.add_all_unique_children(added)
                

    def __unicode__(self):
        return ("State %s, Question: %s" % (
            self.name,
            self.question))
    
class Transition(models.Model):
    """ A Transition is a way to navigate from one
        TreeState to another, via an appropriate 
        Answer. """ 
    current_state = models.ForeignKey(TreeState)
    answer = models.ForeignKey(Answer)
    next_state = models.ForeignKey(TreeState, blank=True, null=True, related_name='next_state')     
    
    def __unicode__(self):
        return ("%s : %s --> %s" % 
            (self.current_state,
             self.answer,
             self.next_state))
 
class Session(models.Model):
    """ A Session represents a single person's current 
        status traversing through a Tree. It is a way
        to persist information about what state they
        are in, how many retries they have had, etc. so 
        that we aren't storing all of that in-memory. """ 
    connection = models.ForeignKey(PersistantConnection)
    tree = models.ForeignKey(Tree)
    start_date = models.DateTimeField(auto_now_add=True)
    state = models.ForeignKey(TreeState, blank=True, null=True) # none if the session is complete
    # the number of times the user has tried to answer 
    # this question
    num_tries = models.PositiveIntegerField()
    # this flag stores the difference between completed
    # on its own, or manually canceled.
    canceled = models.NullBooleanField(blank=True, null=True) 
     
    def __unicode__(self):
        if self.state:
            text = self.state
        else:
            text = "completed"
        return ("%s : %s" % (self.connection.identity, text))

class Entry(models.Model):
    """ An Entry is a single successful movement within
        a Session.  It represents an accepted Transition 
        from one state to another within the tree. """ 
    session = models.ForeignKey(Session)
    sequence_id = models.IntegerField()
    transition = models.ForeignKey(Transition)
    time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=160)
    
    def __unicode__(self):
        return "%s-%s: %s - %s" % (self.session.id, self.sequence_id, self.transition.current_state.question, self.text)
    
    def meta_data(self):
        return "%s - %s %s" % (
            self.session.person.phone,
            self.time.strftime("%a %b %e"),
            self.time.strftime("%I:%M %p"))
    
    def display_text(self):
        # assume that the display text is just the text,
        # since this is what it is for free text entries
        return self.text
    
    
    class Meta:
        verbose_name_plural="Entries"
