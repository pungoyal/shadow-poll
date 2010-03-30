import random, os
from django.core.management.base import NoArgsCommand

from apps.poll.models import *
from apps.charts.models import *
from apps.reporters.models import *

class Command(NoArgsCommand):
    USERS_TO_BE_CREATED = 100000
    RESPONSES_PER_QUESTION = 1000000

    def handle_noargs(self, **options):
        self.setUp()
        governorates = Governorate.objects.all()
        for i in range(0, self.USERS_TO_BE_CREATED):
            self.save_random_user(random.choice(governorates))

        users = User.objects.all()
        for i in range(0, self.RESPONSES_PER_QUESTION):
            self.save_random_user_response(random.choice(users))

#        os.system('/Users/Puneet/work/shadow-poll/manage.py dumpdata reporters poll --indent=4 > /Users/Puneet/work/shadow-poll/a.json')
        print "I just created %s Users and %s dummy UserResponses!" % (self.USERS_TO_BE_CREATED, self.RESPONSES_PER_QUESTION)

    def setUp(self):
        backends = PersistantBackend.objects.all()
        if len(backends) == 0:
            backend = PersistantBackend(slug="test", title="data")
            backend.save()
        else:
            backend = backends[0]

        connections = PersistantConnection.objects.all()
        if len(connections) == 0:
            self.connection = PersistantConnection(is_bot=False, identity="test", backend=backend)
            self.connection.save()
        else:
            self.connection = connections[0]

    def save_random_user(self, governorate):
        districts = District.objects.filter(governorate=governorate.id)
        user = User(connection = self.connection,
                    age = random.randint(2,18),
                    gender = random.choice('mf'),
                    governorate = governorate.id,
                    district = random.choice(districts).code)
        user.save()

    def save_random_user_response(self, user):
        for question_id in range(1,4):
            question = Question.objects.get(id=question_id)
            choices = Choice.objects.filter(question=question)
            user_response = UserResponse(question=question, user=user, choice=random.choice(choices))
            user_response.save()
            