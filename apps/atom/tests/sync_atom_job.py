import os
import  shutil
from unittest import TestCase

from apps.atom.jobs.daily.sync_atom import SyncAtomJob

class SyncAtomJobTest(TestCase):
    def setUp(self):
        data_path = os.path.join( os.path.dirname(__file__), "data")
        template_atom_xml_file = os.path.join(data_path, "atom.xml.template")
        self.atom_xml_file = os.path.join(data_path, "atom.xml")

        xml_file_handle = open(template_atom_xml_file, 'r')
        xml_content = xml_file_handle.read()
        xml_file_handle.close()

        audio_file = os.path.join(data_path, "audio.3gp")
        xml_content = xml_content.replace("REPLACE_ME", "file://%s" % audio_file)

        xml_file_handle = open(self.atom_xml_file, 'w+')
        xml_file_handle.write(xml_content)
        xml_file_handle.close()

    def fails_test_run(self):
        job = SyncAtomJob()
        job.sync_atom("file://%s" % self.atom_xml_file)
