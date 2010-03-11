import os
import shutil
from unittest import TestCase

from apps.atom.jobs.daily.sync_atom import SyncAtomJob

class SyncAtomJobTest(TestCase):
    def test_run(self):
        job = SyncAtomJob()
        job.sync_atom("http://iraqyouth.mepemepe.com/ivr/atom.xml")
