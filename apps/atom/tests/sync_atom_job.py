import os, os.path
import shutil
from unittest import TestCase

from apps.atom.models import Entry

from apps.atom.jobs.daily.sync_atom import SyncAtomJob

class SyncAtomJobTest(TestCase):
    def fails_test_run(self):
        initial_count = len(Entry.objects.all())

        job = SyncAtomJob()
        voice_messages = job.sync_atom("http://iraqyouth.mepemepe.com/ivr/atom.xml")
        self.assertEquals(len(voice_messages), 1)

        voice_message = voice_messages[0]
        self.file_name = voice_message.sound_file_name
        self.assertTrue(os.path.isfile(voice_message.sound_file_name))

        entries = Entry.objects.all()
        self.assertEquals(len(entries), initial_count + 1)
        self.assertTrue(entries[initial_count].processed)

    def tearDown(self):
        os.remove(self.file_name)        