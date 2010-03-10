import os
import uuid
import urllib2

from apps.django_extensions.management.jobs import BaseJob

from apps.atom.models import IVRFeedParser

atom_url = "file:///Users/Puneet/work/atom10.xml"
path = "atom.xml"
data_dir = "/tmp"

class SyncAtomJob(BaseJob):
    help = "Sync with the IVR atom feed"

    def execute(self):
        # add config stuff here
        self.sync_atom(atom_url)

    def sync_atom(self, atom_url):
        print "Fetching ATOM feed"
        response = urllib2.urlopen(atom_url)
        print "Parsing ATOM feed"
        parser = IVRFeedParser()
        entries = parser.parse(response)

        for entry in entries:
            print "Downloading audio file %s" % entry.file_url
            response = urllib2.urlopen(entry.file_url)
            extension = entry.file_url.rsplit(".")[-1]
            file_name = str(uuid.uuid4())
            if len(extension) < 5:
                file_name = file_name + '.'+ extension
            file_name = os.path.join(data_dir, file_name)
            print "Saving file to %s" % file_name

            fout = open(file_name, 'w+b')
            fout.write(response.read())
            fout.close()
            #mark file as processed
            #create a new audiomessage and save
        print "Generated all remote submissions archive"
