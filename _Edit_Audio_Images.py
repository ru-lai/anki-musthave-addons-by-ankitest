# -*- mode: Python ; coding: utf-8 -*-
# ' Edit Audio Images
# https://ankiweb.net/shared/info/1040866511
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# In card reviewer F10 opens all images and sounds in external editors.
# Ctrl+F10 only pictures
# Shift+F10 only audios
#
# In Add/Edit window F10 opens sounds and images only from current field.
#
# You can uncomment lines # Windows_IMG or # Windows_SND
# to setup you own Windows command line
# to start external program with images/audio
#
# Runs on Windows and macOS.
#
# For Mac's start commands search: isMac
#
# No support. Use it AS IS on your own risk.
from __future__ import division
from __future__ import unicode_literals
import os
import sys
import re

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from anki.hooks import addHook, wrap, runHook
from aqt import mw
from aqt.editor import Editor  # the editor when you click 'Add' in Anki
from aqt.utils import tooltip, showInfo, showWarning, showCritical, showText
from anki.utils import isWin, isMac

# Get language class
import anki.lang
lang = anki.lang.getLang()

MSG = {
    'en': {
        'later': _('later'),
        'not now': _('not now'),
        'Cards': _('&Cards'),
        'View': _('&View'),
        'Go': _('&Go'),
        'Edit Audio Images': _('&Edit Audio Images from fields'),
        'Edit Images': _('Edit &Images from fields'),
        'Edit Audio': _('Edit &Audio from fields'),
        },
    'ru': {
        'later': 'позже',
        'not now': 'не сейчас',
        'Cards': '&Карточки',
        'View': '&Вид',
        'Go': 'П&ереход',
        'Edit Audio Images': '&Правка Аудио и Картинок из полей',
        'Edit Images': 'Правка &Картинок из полей',
        'Edit Audio': 'Правка &Аудио из полей',
        },
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

# '&Правка Аудио и Картинок из полей' if lang == 'ru' else
#   _('&Edit Audio Images from fields')
# 'Правка &Картинок из полей' if lang == 'ru' else
#   _('Edit &Images from fields')
# 'Правка &Аудио из полей' if lang == 'ru' else
#   _('Edit &Audio from fields')

HOTKEY = {      # in mw Main Window (deckBrowser, Overview, Reviewer)
    'edit':  'F10',
    'image': 'Ctrl+F10',
    'audio': 'Shift+F10',
}

win_open_edit = 'open'  # 'edit'  #

Windows_IMG = None
# Windows_IMG = u'''start "" /B "%s" '''

Windows_SND = None
# Windows_SND = u'''start "" /B "%s" '''

macOS_IMG = "open"

macOS_SND = "open -a " + "\'Audacity\'"

# macOS_SND = ("open -a " + "/Applications/Adobe\ Audition\ CC\ " +
#             "2017/Adobe\ Audition\ CC\ 2017.app")

##########################
#
if __name__ == '__main__':
    print 'This is _Edit_Audio_Images add-on for the Anki program'
    print " and it can't be run directly."
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2':  # Python 3 is utf8 only already.
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf8')

##


def JustDoItBy(note, curFld, audioPic):
    fldl = len(note.fields)
    if curFld < 0:
        flds = note.fields
    else:
        flds = [note.fields[curFld]]
    pathToCollection = mw.col.media.dir() + "/"

    if audioPic == 0 or audioPic == 1:
        for fld in flds:
            # next_picture =
            #   re.search(r'''\<img src=["|'](.*?)["|']''',fld) # '''
            next_pictures = re.findall(r'\<img src="(.*?)"', fld)
            for next_picture in next_pictures:
                if next_picture and isWin:
                    found = os.path.join(mw.col.media.dir(),
                                         next_picture)  # .group(1))
                    if os.path.exists(found):
                        if Windows_IMG:
                            os.system(Windows_IMG % (found))
                        else:
                            try:
                                os.startfile(found, win_open_edit)
                            except WindowsError:
                                try:
                                    os.startfile(found)
                                except:
                                    pass
                if next_picture and isMac:
                    fullPath = os.path.join(pathToCollection, found)
                    # need to escape spaces
                    fullPath = re.sub(" ", "\ ", fullPath)
                    os.system(macOS_IMG + " " + fullPath)

    if audioPic == 0 or audioPic == 2:
        for fld in flds:
            # next_sound = re.search(r'\[sound:(.*?)\]',fld)
            next_sounds = re.findall(r'\[sound:(.*?)\]', fld)
            for next_sound in next_sounds:
                if next_sound and isWin:
                    found = os.path.join(mw.col.media.dir(),
                                         next_sound)  # .group(1))
                    if os.path.exists(found):
                        if Windows_SND:
                            os.system(Windows_SND % (found))
                        else:
                            try:
                                os.startfile(found, win_open_edit)
# >> WindowsError: [Error 1155]
# No application is associated with the specified file for this operation:
                            except WindowsError:
                                try:
                                    os.startfile(found)
                                except:
                                    pass
                if next_sound and isMac:
                    fullPath = os.path.join(pathToCollection, next_sound)
                    fullPath = re.sub(" ", "\ ", fullPath)
                    os.system(macOS_SND + " " + fullPath)


def JustDoItByYourself():
    rst = mw.reviewer.state
    NB = mw.reviewer.card.note()
    JustDoItBy(NB, -1, 0)
    # mw.reset()  # refresh gui
    # if rst == 'answer':
    #     mw.reviewer._showAnswerHack()  # ._showAnswer() #
    # mw.requireReset()


def JustDoItByPictures():
    rst = mw.reviewer.state
    NB = mw.reviewer.card.note()
    JustDoItBy(NB, -1, 1)
    # mw.reset()  # refresh gui
    # if rst == 'answer':
    #     mw.reviewer._showAnswerHack()  # ._showAnswer() #
    # mw.requireReset()


def JustDoItBySounds():
    rst = mw.reviewer.state
    NB = mw.reviewer.card.note()
    JustDoItBy(NB, -1, 2)
    # mw.reset()  # refresh gui
    # if rst == 'answer':
    #     mw.reviewer._showAnswerHack()  # ._showAnswer() #
    # mw.requireReset()


def TryItByYourself(edit):
    ecf = edit.currentField
    JustDoItBy(edit.note, ecf, 0)
    mw.reset()  # refresh gui
    # focus field so it's saved
    edit.web.setFocus()
    edit.web.eval('focusField(%d);' % ecf)

##

edit_action = QAction(MSG[lang]['Edit Audio Images'], mw)
edit_action.setShortcut(QKeySequence(HOTKEY['edit']))
edit_action.setEnabled(False)
mw.connect(edit_action, SIGNAL('triggered()'), JustDoItByYourself)


images_action = QAction(MSG[lang]['Edit Images'], mw)
images_action.setShortcut(QKeySequence(HOTKEY['image']))
images_action.setEnabled(False)
mw.connect(images_action, SIGNAL('triggered()'), JustDoItByPictures)


sounds_action = QAction(MSG[lang]['Edit Audio'], mw)
sounds_action.setShortcut(QKeySequence(HOTKEY['audio']))
sounds_action.setEnabled(False)
mw.connect(sounds_action, SIGNAL('triggered()'), JustDoItBySounds)

##

mw.form.menuEdit.addSeparator()
mw.form.menuEdit.addAction(edit_action)
mw.form.menuEdit.addAction(images_action)
mw.form.menuEdit.addAction(sounds_action)
mw.form.menuEdit.addSeparator()


def edit_ai_off():
    edit_action.setEnabled(False)
    images_action.setEnabled(False)
    sounds_action.setEnabled(False)


def edit_ai_on():
    edit_action.setEnabled(True)
    images_action.setEnabled(True)
    sounds_action.setEnabled(True)

mw.deckBrowser.show = wrap(mw.deckBrowser.show, edit_ai_off)
mw.overview.show = wrap(mw.overview.show, edit_ai_off)
mw.reviewer.show = wrap(mw.reviewer.show, edit_ai_on)


def edit_ai_buttons(editor):
    """Add the buttons to the editor."""
    editor._addButton(
        'image', lambda edito=editor: TryItByYourself(edito),
        HOTKEY['edit'],
        tip='Edit Audio Images from fields in external editor (' +
        HOTKEY['edit'] + ')')

# register callback function that gets executed
#  after setupEditorButtons has run.
# See Editor.setupEditorButtons for details
addHook('setupEditorButtons', edit_ai_buttons)
