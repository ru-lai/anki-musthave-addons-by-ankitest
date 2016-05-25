# -*- coding: utf-8 -*-
# ~ Clear Field Formatting HTML
# https://ankiweb.net/shared/info/1114708966
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#  Made by request: 
#   Clear Field Formatting (HTML) in Bulk needs improvement 
#    https://anki.tenderapp.com/discussions/add-ons/7526-clear-field-formatting-html-in-bulk-needs-improvement
# Based on
# https://ankiweb.net/shared/info/728131107
# Removes the field formatting of all selected notes.
# Author: xelif@icqmail.com

import re #,sys

from anki.hooks import addHook
from aqt import mw

from PyQt4.QtCore import *
from PyQt4.QtGui import *

def stripFormatting(txt, imgbr, divbr):
    """
    Removes all html tags, except if they begin like this: <img...> <br...> <div > </div>
    This allows inserted images and line breaks to remain.

    Parameters
    ----------
    txt : string
        the string containing the html tags to be filtered
    Returns
    -------
    string
        the modified string as described above
    """
    return re.sub(imgbr, "", re.sub(divbr, "\n", re.sub("<div .*?>", "<div>", txt)))

def onClearFormat(self):
    mw.checkpoint("Clear Field Formatting HTML")
    mw.progress.start()
    for nid in self.selectedNotes():
        note = mw.col.getNote(nid)
        def clearField(field):
            return stripFormatting(field, "<(?!img|br|div|/div).*?>", "(^$)")
        note.fields = map(clearField, note.fields)
        note.flush()
    mw.progress.finish()
    mw.reset()

def onClearFormatting(self):
    """
    Clears the formatting for every selected note.
    Also creates a restore point, allowing a single undo operation.

    Parameters
    ----------
    self : Browser
        the anki self from which the function is called
    """
    mw.checkpoint("Clear Field Formatting HTML")
    mw.progress.start()
    for nid in self.selectedNotes():
        note = mw.col.getNote(nid)
        def clearField(field):
            result = stripFormatting(field, "<(?!img).*?>", "</div><div>|</div>|<div>|<br />");
            # if result != field:
            #     sys.stderr.write("Changed: \"" + field
            #                      + "\" ==> \"" + result + "\"")
            return result
        note.fields = map(clearField, note.fields)
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(self):
    """
    Add the items to the browser menu "edit".
    """
    a = QAction(_("Clear Field Formatting HTML (remain new lines)"), self)
    self.connect(a, SIGNAL("triggered()"), lambda e=self: onClearFormat(e))
    self.form.menuEdit.addSeparator()
    self.form.menuEdit.addAction(a)

    b = QAction(_("Clear Field Formatting HTML (at all)"), self)
    self.connect(b, SIGNAL("triggered()"), lambda e=self: onClearFormatting(e))
    self.form.menuEdit.addAction(b)
    self.form.menuEdit.addSeparator()

addHook("browser.setupMenus", setupMenu)
