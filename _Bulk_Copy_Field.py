# -*- mode: Python ; coding: utf-8 -*-
# ~ Bulk Copy Field
# https://ankiweb.net/shared/info/2021298056
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# It copies src fld 2 dst 4 certain note types.
# Destinations may be overwritten.
#
# No support. Use it AS IS on your own risk.
#
# Copyright: Chris Langewisch <ccl09c@my.fsu.edu>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Based on japanese.reading by Damien Elmes <anki@ichi2.net>
# Bulk copy data in one field to another.
from __future__ import unicode_literals
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from anki.hooks import addHook
from aqt import mw
from aqt.utils import askUser, showText, tooltip

# Get language class
import anki.lang
lang = anki.lang.getLang()

# --- user defined options ---

# USE LOWERCASE. Model name must contain this.
modelName = 'Basic'.lower()

# NB! 'Cobasic-04Bc' also is matched for 'Basic' and so on.

# each field name must be exact!
srcField = 'Front'
dstField = 'Back'

# if data exists in dstField, should we overwrite it?
overwrite_dstField = True

# ----------------------------

def bulkCopy(nids):
    mw.checkpoint("~ Bulk Copy Field")
    mw.progress.start()
    for nid in nids:
        # print "Found note: %s" % (nid)
        note = mw.col.getNote(nid)
        if modelName not in note.model()['name'].lower():
            # print "--> Model mismatch: %s vs %s" % (
            #    modelName, note.model()['name'].lower())
            continue
        src = None
        if srcField in note:
            src = srcField
        if not src:
            # no src field
            # print "--> Field %s not found." % (srcField)
            continue
        dst = None
        if dstField in note:
            dst = dstField
        if not dst:
            # print "--> Field %s not found!" % (dstField)
            # no dst field
            continue
        if note[dst] and not overwrite_dstField:
            # already contains data, skip
            # print "--> %s not empty. Skipping!" % (srcField)
            continue
        # srcTxt = mw.col.media.strip(note[src])
        # if not srcTxt.strip():
        #    continue
        try:
            # print "--> Everything should have worked."
            note[dst] = note[src]
            # note[dst] = srcTxt
        except Exception, e:
            raise
        note.flush()
    mw.progress.finish()
    mw.reset()

##

def onBulkCopy(self):
    suffix = ''
    sfx = ''
    if overwrite_dstField:
        suffix = '<br>NB! Existing values would be overwritten!'
        sfx = '<br>Existing values were overwritten!'
    if askUser(
        ('<i>~ Bulk Copy Field</i> from <b>%s</b> to <b>%s</b>' +
         ' for <b>%s</b> note types?' + suffix) % (
            srcField, dstField, modelName)):

        bulkCopy(self.selectedNotes())

        tooltip(
            ('<i>~ Bulk Copy Field</i> from <b>%s</b> to <b>%s</b>' +
             ' for <b>%s</b> note types <i>done.</i>' + sfx) % (
                srcField, dstField, modelName))


def setupMenu(self):
    BCF = QAction("~ &Bulk Copy Field...", self)
    self.connect(BCF, SIGNAL("triggered()"), 
                 lambda e=self: onBulkCopy(e))

    def on_overwrite_dstField():
        global overwrite_dstField
        overwrite_dstField = YMCA.isChecked()

    YMCA = QAction("&Overwrite destination field", self)
    YMCA.setCheckable(True)
    YMCA.setChecked(overwrite_dstField)

    self.connect(YMCA, SIGNAL("triggered()"), on_overwrite_dstField)

    self.form.menuEdit.addSeparator()
    self.form.menuEdit.addAction(BCF)
    self.form.menuEdit.addAction(YMCA)
    self.form.menuEdit.addSeparator()

addHook("browser.setupMenus", setupMenu)

##

def save_flags():
    mw.pm.profile['BCF_overwrite_dstField'] = overwrite_dstField


def load_flags():
    global overwrite_dstField

    try:
        key_value = mw.pm.profile['BCF_overwrite_dstField']
        overwrite_dstField = key_value
    except KeyError:
        pass

addHook('unloadProfile', save_flags)
addHook('profileLoaded', load_flags)

##

old_addons = (
    'Bulk_Copy_Field.py',
    'Bulk_Field_Copy.py',
)

old_addons2delete = ''
for old_addon in old_addons:
    if len(old_addon) > 0:
        old_filename = os.path.join(mw.pm.addonFolder(), old_addon)
        if os.path.exists(old_filename):
            old_addons2delete += old_addon[:-3] + ' \n'

if old_addons2delete != '':
    if lang == 'ru':
        showText(
            'В каталоге\n\n ' + mw.pm.addonFolder() +
            '\n\nнайдены дополнения, которые уже включены в дополнение\n ' +
            os.path.basename(__file__) + '\n' +
            'и поэтому будут конфликтовать с ним.\n\n' +
            old_addons2delete +
            '\nПереименуйте (добавьте расширение .off) ' +
            '\n или удалите эти дополнения ' +
            '\n   и перезапустите Anki.')
    else:
        showText(
            'There are some add-ons in the folder \n\n ' +
            mw.pm.addonFolder() + '\n\n' +
            old_addons2delete +
            '\n\nThey are already part of this addon,\n ' +
            os.path.basename(__file__) +
            '\n\nPlease, rename them (add .off extension to file)' +
            ' or delete\n and restart Anki.')
