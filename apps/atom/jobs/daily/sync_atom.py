import os
import uuid
import urllib2

from rapidsms.webui import settings

from apps.django_extensions.management.jobs import BaseJob
from apps.atom.models import IVRFeedParser
from apps.charts.models import VoiceMessage

# share the same logging as IVRFeedParser()
# change all 'prints' to 'log'

class SyncAtomJob(BaseJob):
    help = "Sync with the IVR atom feed"
    media_dir = settings.RAPIDSMS_APPS["atom"]["media_dir"]

    def execute(self):
        atom_url = settings.RAPIDSMS_APPS["atom"]["atom_url"]
        self.sync_atom(atom_url)

    def sync_atom(self, atom_url):
        response = urllib2.urlopen(atom_url)
        parser = IVRFeedParser()
        entries = parser.parse(response)

        voice_messages = []

        for entry in entries:
            response = urllib2.urlopen(entry.file_url)
            extension = entry.file_url.rsplit(".")[-1]
            file_name = str(uuid.uuid4())
            if len(extension) < 5:
                file_name = file_name + '.'+ extension
            file_name = os.path.join(self.media_dir, file_name)

            fout = open(file_name, 'w+b')
            fout.write(response.read())
            fout.close()

            voice_message = VoiceMessage()
            voice_message.fill(entry, file_name)
            voice_message.save()

            voice_messages.append(voice_message)

            entry.processed = True
            entry.save()
        return voice_messages
