import os, os.path
import shutil
from unittest import TestCase

from apps.atom.jobs.daily.sync_atom import SyncAtomJob

class SyncAtomJobTest(TestCase):
    def test_run(self):
        job = SyncAtomJob()
        voice_messages = job.sync_atom("http://iraqyouth.mepemepe.com/ivr/atom.xml")
        self.assertEquals(len(voice_messages), 1)

        voice_message = voice_messages[0]
        self.assertTrue(os.path.isfile(voice_message.sound_file_name))

        os.remove(voice_message.sound_file_name)        