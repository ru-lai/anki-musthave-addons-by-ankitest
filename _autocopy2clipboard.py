# -*- mode: Python ; coding: utf-8 -*-
# ~ autocopy2clipboard
# https://ankiweb.net/shared/info/344503497
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# It copies field contain to system clipboard (exchange buffer)
# with or without HTML tags
# by keeping or removing newline (line feed and carriage return).
#
# You obtain Q&A sides from different lists of fields
# in priority order from top to bottom.
# Tested with Anki 2.0.36
#
# No support. Use it AS IS on your own risk.
from __future__ import unicode_literals

###############################################################################
#  Copyright (C) 2012 Christopher Brochtrup
#
#  This file is part of Copy2Clipboard
#
#  Copy2Clipboard is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Copy2Clipboard is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Copy2Clipboard.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
# Description:
#
# Copy2Clipboard will automatically copy a single card field to the clipboard
# when either the card's question side is shown or when the card's answer side
# is shown (or both, if desired).
#
# To change the default behavior simply edit the questionFields or answerFields
# variables in the # User Options  # section of this file.
#
###############################################################################
# Version: 1.1
# Tested with Anki 2.0.3
# Contact: cb4960@gmail.com
###############################################################################

import codecs
from datetime import datetime
import os
import re

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from aqt import mw
from anki.hooks import wrap, addHook
from anki.utils import stripHTML
from aqt.reviewer import Reviewer
from aqt.utils import tooltip, showText

# Get language class
import anki.lang
lang = anki.lang.getLang()

# User Options  #

# If you don't want to copy...
copyQuestion = True  # False  #
copyAnswer = False  # True  #

copySide = False  # True  #
removeHTML = True  # False  #
keepNewLines = True  # False  #
deleteSound = False  # True  #

# Find field names in list
caseSensitive = False  # True  #
clearBuffer = True  # False  #
# if not found

# Clear log at startup

writeLog = False  # True  #
clearLog = True  # False  #

# The name of the field to copy to the clipboard
# when the question side of the card is shown.
questionFields = (
    'PGN',
    _('Q'),
    'Q',
    _('Question'),
    'Question',
    _('Front'),
    'Front',
    _('Text'),
    'Text',
    )

# The name of the field to copy to the clipboard
# when the answer side of the card is shown.
answerFields = (
    'PGN',
    _('A'),
    'A',
    _('Answer'),
    'Answer',
    _('Back'),
    'Back',
    _('Extra'),
    'Extra',
    )

HOTKEY = {
    'do_copy_Question':    ['Alt+Q', '', '', ''' ''', """ """],
    'do_copy_Answer':      ['Alt+A', '', '', ''' ''', """ """],
    'do_clear_Buffer':     ['Alt+Z', '', '', ''' ''', """ """],
}

try:
    LOG_FILE = os.path.join(  # log to base folder
        mw.pm.addonFolder(), '..', '_autocopy2clipboard.log')
except:
    LOG_FILE = 'C:/TEMP/Copy2Clipboard.log'
# os.path.join(mw.pm.profileFolder(), 'backups', 'filename.ext')
# at the moment of running addons user's profile is not initiated yet

# Functions


def do_clearLog():
    if writeLog:
        file = codecs.open(LOG_FILE, 'w', 'utf-8-sig')
        file.write('')
        file.close()


def do_writeLog(text):
    if writeLog:
        if text:
            file = codecs.open(LOG_FILE, 'a', 'utf-8-sig')
            file.write(
                ('\n' if text[0] == 'Q' else '') +
                datetime.now().strftime('%Y-%m-%d_%H:%M:%S') +
                ' ' + text + '\n')
            file.close()


def copyTextToClipboard(text):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)


def copyField(QandA, field_names, card):
    fieldIndex = -1
    fieldName = ''

    if copySide:
        # Side Template only, without CSS (Styling section)
        if QandA == 'Q':
            fieldToCopy = card._getQA()['q']  # card.q()  # with css
        else:
            fieldToCopy = card._getQA()['a']  # card.a()
    else:

        for fl in field_names:
            if not caseSensitive:
                fld = fl.lower()
            else:
                fld = fl

            for fldi, flde in enumerate(card.model()['flds']):
                if not caseSensitive:
                    fldn = flde['name'].lower()
                else:
                    fldn = flde['name']

                if fld == fldn:
                    fieldIndex = fldi
                    fieldName = flde['name']
                    break
            if fieldIndex > -1:
                break
        else:
            do_writeLog(QandA + ' Field name not found.')
            if clearBuffer:
                copyTextToClipboard('')
                return
            else:
                fieldIndex = 0
                fieldName = card.model()['flds'][0]['name']

        # do_writeLog('%d %s' % (fieldIndex, fieldName))

        fieldToCopy = card.note()[fieldName]

    do_writeLog(QandA + ' ' + fieldName + ': ' + fieldToCopy)

    def remove_newLines(html2txt, LFCR):

        retv = html2txt.replace('<br />', LFCR)

        def removeThemAll(fld, htm, lfcr):
            retv = fld.replace('<%s></%s>' % (htm, htm), lfcr)
            retv = retv.replace('</%s><%s>' % (htm, htm), lfcr)
            retv = retv.replace('<%s>' % (htm), lfcr)
            retv = retv.replace('</%s>' % (htm), lfcr)
            return retv

        retv = removeThemAll(retv, 'div', LFCR)
        retv = removeThemAll(retv, 'pre', LFCR)
        retv = removeThemAll(retv, 'p', LFCR)

        return retv

    if removeHTML:
        if keepNewLines:
            fieldToCopy = remove_newLines(fieldToCopy, '\n')
        else:
            fieldToCopy = remove_newLines(fieldToCopy, ' ')
            # fieldToCopy = re.sub('\n', ' ', fieldToCopy)
        fieldToCopy = stripHTML(fieldToCopy).strip()

    if deleteSound:
        fieldToCopy = re.sub('\[sound:.+?\]', '', fieldToCopy)

    fieldToCopy = re.sub('\n\s*\n+', '\n\n', fieldToCopy)

    if not copySide and fieldToCopy != card.note()[fieldName]:
        do_writeLog(fieldName + ' = ' + fieldToCopy)

    copyTextToClipboard(fieldToCopy)


def wrapped_showQuestion(self):
    if copyQuestion:
        copyField('Q', questionFields, self.card)


def wrapped_showAnswer(self):
    if copyAnswer:
        copyField('A', answerFields, self.card)

Reviewer._showQuestion = wrap(Reviewer._showQuestion, wrapped_showQuestion)
Reviewer._showAnswer = wrap(Reviewer._showAnswer, wrapped_showAnswer)

# Main

try:
    mw.addon_cards_menu
except AttributeError:
    mw.addon_cards_menu = QMenu(
        _(u"&Карточки") if lang == 'ru'
        else _(u'&Cards'), mw.menuBar())
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_cards_menu)

mw.copy2clipboad_submenu = QMenu(_('autocopy&2clipboard'), mw.menuBar())
mw.addon_cards_menu.addMenu(mw.copy2clipboad_submenu)

a = QAction(mw)
a.setText('= Right Now =')
a.setEnabled(False)


def do_copyQuestion():
    copyField('Q', questionFields, mw.reviewer.card)

aaa = QAction(mw)
aaa.setText('do copy &Question')
aaa.setShortcut(QKeySequence(HOTKEY['do_copy_Question'][0]))
mw.connect(aaa, SIGNAL("triggered()"), do_copyQuestion)


def do_copyAnswer():
    copyField('A', answerFields, mw.reviewer.card)

bbb = QAction(mw)
bbb.setText('do copy &Answer')
bbb.setShortcut(QKeySequence(HOTKEY['do_copy_Answer'][0]))
mw.connect(bbb, SIGNAL("triggered()"), do_copyAnswer)


def do_clearBuffer():
    copyTextToClipboard('')
    tooltip('Clipboard is erased.', period=1000)

eeee = QAction(mw)
eeee.setText('do &Clear buffer')
eeee.setShortcut(QKeySequence(HOTKEY['do_clear_Buffer'][0]))
mw.connect(eeee, SIGNAL("triggered()"), do_clearBuffer)

aaaa = QAction(mw)
aaaa.setText('= Always =')
aaaa.setEnabled(False)


def on_copyQuestion():
    global copyQuestion
    copyQuestion = aa.isChecked()

aa = QAction(mw)
aa.setText('autoCopy on &FrontSide')
aa.setCheckable(True)
mw.connect(aa, SIGNAL("triggered()"), on_copyQuestion)


def on_copyAnswer():
    global copyAnswer
    copyAnswer = bb.isChecked()

bb = QAction(mw)
bb.setText('autoCopy on &BackSide')
bb.setCheckable(True)
mw.connect(bb, SIGNAL("triggered()"), on_copyAnswer)


def on_copySide():
    global copySide
    copySide = ccc.isChecked()

ccc = QAction(mw)
ccc.setText('C&opy Side (not only field)')
ccc.setCheckable(True)
mw.connect(ccc, SIGNAL("triggered()"), on_copySide)


def on_removeHTML():
    global removeHTML
    removeHTML = cc.isChecked()

    dd.setEnabled(removeHTML)

cc = QAction(mw)
cc.setText('&Delete HTML')
cc.setCheckable(True)
mw.connect(cc, SIGNAL("triggered()"), on_removeHTML)


def on_keepNewLines():
    global keepNewLines
    keepNewLines = dd.isChecked()

dd = QAction(mw)
dd.setText('&Keep new lines')
dd.setCheckable(True)
mw.connect(dd, SIGNAL("triggered()"), on_keepNewLines)


def on_deleteSound():
    global deleteSound
    deleteSound = ddd.isChecked()

ddd = QAction(mw)
ddd.setText('Remo&ve [sound:...]')
ddd.setCheckable(True)
mw.connect(ddd, SIGNAL("triggered()"), on_deleteSound)

e = QAction(mw)
e.setText('= Find Field =')
e.setEnabled(False)


def on_caseSensitive():
    global caseSensitive
    caseSensitive = ee.isChecked()

ee = QAction(mw)
ee.setText('Case &Sensitive')
ee.setCheckable(True)
mw.connect(ee, SIGNAL("triggered()"), on_caseSensitive)


def on_clearBuffer():
    global clearBuffer
    clearBuffer = eee.isChecked()

eee = QAction(mw)
eee.setText('Clear buffer if &not found')
eee.setCheckable(True)
mw.connect(eee, SIGNAL("triggered()"), on_clearBuffer)


def on_writeLog():
    global writeLog
    writeLog = ff.isChecked()

    gg.setEnabled(writeLog)

ff = QAction(mw)
ff.setText('&Write Log')
ff.setCheckable(True)
mw.connect(ff, SIGNAL("triggered()"), on_writeLog)


def on_clearLog():
    global clearLog
    clearLog = gg.isChecked()

gg = QAction(mw)
gg.setText('Clear &Log at startup')
gg.setCheckable(True)
mw.connect(gg, SIGNAL("triggered()"), on_clearLog)


def tick_flags():
    aa.setChecked(copyQuestion)
    bb.setChecked(copyAnswer)
    ccc.setChecked(copySide)
    cc.setChecked(removeHTML)
    dd.setChecked(keepNewLines)
    ddd.setChecked(deleteSound)
    ee.setChecked(caseSensitive)
    eee.setChecked(clearBuffer)
    ff.setChecked(writeLog)
    gg.setChecked(clearLog)

    dd.setEnabled(removeHTML)
    gg.setEnabled(writeLog)

init_flags = (copyQuestion, copyAnswer, copySide,
              removeHTML, keepNewLines, deleteSound,
              caseSensitive, clearBuffer, writeLog, clearLog)


def on_init_flags():
    global copyQuestion, copyAnswer, copySide, \
        removeHTML, keepNewLines, deleteSound, \
        caseSensitive, clearBuffer, writeLog, clearLog

    copyQuestion, copyAnswer,  copySide, \
        removeHTML, keepNewLines, deleteSound, \
        caseSensitive, clearBuffer, writeLog, clearLog = init_flags

    tick_flags()

zz = QAction(mw)
zz.setText('&Reset to default')
mw.connect(zz, SIGNAL("triggered()"), on_init_flags)

c2c = mw.copy2clipboad_submenu

c2c.addAction(a)
c2c.addAction(aaa)
c2c.addAction(bbb)
c2c.addAction(eeee)
c2c.addSeparator()

c2c.addAction(aaaa)
c2c.addAction(aa)
c2c.addAction(bb)
c2c.addSeparator()

c2c.addAction(ccc)
c2c.addAction(cc)
c2c.addAction(dd)
c2c.addAction(ddd)
c2c.addSeparator()
c2c.addAction(e)
c2c.addAction(ee)
c2c.addAction(eee)

c2c.addSeparator()
c2c.addAction(ff)
c2c.addAction(gg)

c2c.addSeparator()
c2c.addAction(zz)


def swap_off():
    mw.copy2clipboad_submenu.setEnabled(False)

    aaa.setEnabled(False)
    bbb.setEnabled(False)
    eeee.setEnabled(False)

    aa.setEnabled(False)
    bb.setEnabled(False)
    ccc.setEnabled(False)
    cc.setEnabled(False)
    dd.setEnabled(False)
    ddd.setEnabled(False)
    ee.setEnabled(False)
    eee.setEnabled(False)
    ff.setEnabled(False)
    gg.setEnabled(False)

    zz.setEnabled(False)


def swap_on():
    mw.copy2clipboad_submenu.setEnabled(True)

    aaa.setEnabled(True)
    bbb.setEnabled(True)
    eeee.setEnabled(True)

    aa.setEnabled(True)
    bb.setEnabled(True)
    ccc.setEnabled(True)
    cc.setEnabled(True)
    dd.setEnabled(removeHTML)
    ddd.setEnabled(True)
    ee.setEnabled(True)
    eee.setEnabled(True)
    ff.setEnabled(True)
    gg.setEnabled(writeLog)

    zz.setEnabled(True)

mw.deckBrowser.show = wrap(mw.deckBrowser.show, swap_off)
mw.overview.show = wrap(mw.overview.show, swap_off)
mw.reviewer.show = wrap(mw.reviewer.show, swap_on)


def save_flags():
    mw.pm.profile['c2c_copyQuestion'] = copyQuestion
    mw.pm.profile['c2c_copyAnswer'] = copyAnswer
    mw.pm.profile['c2c_copySide'] = copySide
    mw.pm.profile['c2c_removeHTML'] = removeHTML
    mw.pm.profile['c2c_keepNewLines'] = keepNewLines
    mw.pm.profile['c2c_deleteSound'] = deleteSound
    mw.pm.profile['c2c_caseSensitive'] = caseSensitive
    mw.pm.profile['c2c_clearBuffer'] = clearBuffer
    mw.pm.profile['c2c_writeLog'] = writeLog
    mw.pm.profile['c2c_clearLog'] = clearLog


def load_flags():
    global copyQuestion, copyAnswer, copySide, \
        removeHTML, keepNewLines, deleteSound, \
        caseSensitive, writeLog, clearLog

    try:
        key_value = mw.pm.profile['c2c_copyQuestion']
        copyQuestion = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['c2c_copyAnswer']
        copyAnswer = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['c2c_copySide']
        copySide = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['c2c_removeHTML']
        removeHTML = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['c2c_keepNewLines']
        keepNewLines = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['c2c_deleteSound']
        deleteSound = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['c2c_caseSensitive']
        caseSensitive = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['c2c_clearBuffer']
        clearBuffer = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['c2c_writeLog']
        writeLog = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['c2c_clearLog']
        clearLog = key_value
    except KeyError:
        pass

    tick_flags()

    if clearLog:
        do_clearLog()

    do_writeLog('-'*59)  # 79 - prefix YYYY-MM-DD_HH:MM:SS and space = 20
    # do_writeLog('%s' % (datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))

addHook('unloadProfile', save_flags)
addHook('profileLoaded', load_flags)

##

old_addons = (
    '_copy2clip.py',
    '_copy2clipboard.py',
    'Copy2Clipboard.py',
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
            '\n\nнайдены дополнения, которые уже включены в дополнение\n' +
            '~ autocopy2clipboard\n' +
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
            '\n\nThey are already part of\n' +
            ' `~ autocopy2clipboad` addon,\n' +
            '\nPlease, rename them (add .off extension) or delete\n' +
            ' and restart Anki.')
