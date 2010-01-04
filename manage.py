Editing a setting changes only the text in this buffer.
To apply your changes, use the Save or Set buttons.
Saving a change normally works by editing your init file.
For details, see Saving Customizations in the Emacs manual.


 Operate on all settings in this buffer that are not marked HIDDEN:
 Set for current session Save for future sessions
 Undo edits Reset to saved Erase customizations   Exit

Parent groups: Tools

/- Ecb group: Emacs code browser.----------------------------------------\
      State: visible group members are all at standard values.
   
Ecb Download : Settings for downloading and installing a new ECB from within ECB.

Ecb Face Options : Settings for all faces used in ECB.

Ecb Tree Buffer : General settings related to the tree-buffers of ECB.

Ecb Layout : Settings for the screen-layout of the Emacs code browser.

Ecb Directories : Settings for the directories-buffer in the Emacs code browser.

Ecb Sources : Settings for the sources-buffers in the Emacs code browser.

Ecb History : Settings for the history-buffer in the Emacs code browser.

Ecb Version Control : Settings for the version-control support in the ECB.

Ecb Methods : Settings for the methods-buffer in the Emacs code browser.

Ecb Non Semantic : Settings for parsing and displaying non-semantic files.

Ecb Jde Integration : Settings for the JDEE-integration in the Emacs code browser.

Ecb Help : Settings for the ECB online help

Ecb Eshell : Settings for eshell integration within the ECB.

Ecb Cycle : Setting for cycling through misc ECB buffers.

Ecb Winman Support : Settings for supporting several window-managers. More

Ecb Analyse : Settings for the analyse-buffer in the Emacs code browser.

Ecb Symboldef : Settings for the symbol-definition-buffer in the Emacs code browser.

Ecb General : General settings for the Emacs code browser.

Ecb Most Important : The most important settings of ECB you should know.

\- Ecb group end -------------------------------------------------------/
#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import sys, os
from os import path

# figure out where all the extra libs (rapidsms and contribs) are
libs=[os.path.abspath('lib'),os.path.abspath('apps')] # main 'rapidsms/lib'
try:
    for f in os.listdir('contrib'):
        pkg = path.join('contrib',f)
        if path.isdir(pkg) and 'lib' in os.listdir(pkg):
            libs.append(path.abspath(path.join(pkg,'lib')))
except:
                # could be several reasons:
                        # no 'contrib' dir, 'contrib' not a dir
                        # 'contrib' not readable, in any case
                        # ignore and leave 'libs' as just
                        # 'rapidsms/lib'
    pass

# add extra libs to the python sys path
sys.path.extend(libs)

# import manager now that the path is correct
from rapidsms import manager

if __name__ == "__main__":
    manager.start(sys.argv)
