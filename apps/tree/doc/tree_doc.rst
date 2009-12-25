==================
Using the Tree App
==================

The tree app allows you to define decision trees that can perform a question-and-answer type interaction with a user.  A tree consists of one or more states each of which is associated with a question and zero or more answers to that question that can transition to other states. As questions are answered the user traverses the tree based on the answers until he or she reaches a state that has no more transitions.  At this point the user has completed the session.  The tree saves every question/answer pairing in a single table, and provides functionality for applications to initiate a callback when trees are initiated and completed so that application developers can write their own processing of the tree data.  A visualization of a tree is below.

.. image:: http://github.com/rapidsms/rapidsms/raw/57faa4133f0839bee697e55cfd6361c70ec153dc/apps/tree/doc/demo_tree.png

**Making a Tree**

Currently trees can only be made through the admin interface.  

Trees have a trigger, which is is the incoming message that will initiate a tree.  They also have a root state which is the first state the tree will be in.  The question linked to the root state will be the one that is sent when the tree is initiated.  The remaining logic of the tree is encapsulated by the Transition objects, which define how answers to questions move from one state to the next (more on this below).
       
A tree also has optional completion text, which is the message that will be sent to the user when they reach a node in the tree with no possible transitions.

**Questions/Answers/TreeStates/Transitions**

The behavior of a tree is fully encapsulated a set of states and transitions that define how one moves through the tree.

A Question is just some text to be sent to the user, and an optional error message if the question is not answered properly.

A TreeState is a location in a tree.  A TreeState is associated with a Question (that will be asked when the user reaches that state in the Tree) and a set of Answers (Transitions) that allow traversal to other TreeStates.

A Transition is a way to move from one TreeState to another.  A Transition has a beginning state, an Answer, and an optional ending state. If a transition has no ending state, the answer will result in the completion of the tree.  

An Answer is a way to answer a question, and defines how one moves across a Transition
       
There are three possible types of answers:
       
1. The simplest is an exact answer. Messages will only match this answer if the text is exactly the same as the answer specified.  
2. The second is a regular expression.  In this case the system will run a regular expression over the message and match the answer if the regular expression matches.
3. The final type is custom logic.  In this case the answer should be a special keyword that  the application developer defines. The  application developer can then register a  function tied to this keyword with the tree  app and the tree app will call that function to see if the answer should match. The function should return any value that maps to True if  the answer is valid, otherwise any value that maps to False.
 
**Registering a custom answer handler**

The following code shows a function, and how to register that function with the Tree app as a custom answer handler for the word "demo".

:: 

   # inside myapp.App

   def validate_password(self, msg):
      '''This function validates a password.  This exact functionality could 
         have been provided with a normal answer type, but you can put
	 whatever logic you want here as long as you return True/False
	 for matching/non-matching answers'''
        return msg.text == "spomc"

   def start (self):
        '''Start is called by the router to bootstrap our app'''
        # get the app from the rapidsms router
	self.tree_app = self.router.get_app("tree")
	# register our validate password function with the "demo" keyword
        self.tree_app.register_custom_transition("demo", self.validate_password)

