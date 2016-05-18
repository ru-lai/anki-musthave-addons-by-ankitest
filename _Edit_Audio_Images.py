# -*- mode: Python ; coding: utf-8 -*-
# • Edit Audio Images
# https://ankiweb.net/shared/info/1040866511
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
from __future__ import division
from __future__ import unicode_literals
import os, sys, re

if __name__ == '__main__':
    print 'This is _Edit_Audio_Images add-on for the Anki program'
    print " and it can't be run directly."
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2': # Python 3 is utf8 only already.
  if hasattr(sys,'setdefaultencoding'):
    sys.setdefaultencoding('utf8')

from aqt import mw
from aqt.utils import tooltip, showInfo, showWarning, showCritical
from anki.hooks import addHook, wrap, runHook
from aqt.editor import Editor # the editor when you click 'Add' in Anki

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Get language class
import anki.lang
lang = anki.lang.getLang()

try:
    MUSTHAVE_COLOR_ICONS = os.path.join(mw.pm.addonFolder(), 'edit_icons')
except:
    MUSTHAVE_COLOR_ICONS = ''

HOTKEY = {      # in mw Main Window (deckBrowser, Overview, Reviewer)
    'edit'  : ['F10', '', '', ''' ''', """ """], 
    }

##

def JustDoItBy(note,curFld):
    fldl = len(note.fields)
    if curFld<0:
        flds = note.fields
    else:
        flds = [note.fields[curFld]]
    for fld in flds:
        #next_sound = re.search(r'\[sound:(.*?)\]',fld)
        next_sounds = re.findall(r'\[sound:(.*?)\]',fld)
        for next_sound in next_sounds:
          if next_sound:
            found = os.path.join(mw.col.media.dir(), next_sound) #.group(1))
            if os.path.exists(found):
                try:
                    os.startfile(found,'edit')
#>> WindowsError: [Error 1155] No application is associated with the specified file for this operation:
                except WindowsError:
                  try:
                    os.startfile(found)
                  except:
                    pass 
                break
    for fld in flds:
        #next_picture = re.search(r'''\<img src=["|'](.*?)["|']''',fld) # '''
        next_pictures = re.findall(r'\<img src="(.*?)"',fld)
        for next_picture in next_pictures:
          if next_picture:
            found = os.path.join(mw.col.media.dir(), next_picture) #.group(1))
            if os.path.exists(found):
                try:
                    os.startfile(found,'edit')
                except WindowsError:
                  try:
                    os.startfile(found)
                  except:
                    pass 
                break

##

def JustDoItByYourself():
    rst = mw.reviewer.state 
    NB = mw.reviewer.card.note()
    JustDoItBy(NB,-1)
    mw.reset()  # refresh gui
    if rst == 'answer':
        mw.reviewer._showAnswerHack() # ._showAnswer() # 

def TryItByYourself(edit):
    ecf = edit.currentField
    JustDoItBy(edit.note,ecf)
    mw.reset()  # refresh gui
    # focus field so it's saved
    edit.web.setFocus()
    edit.web.eval('focusField(%d);' % ecf)

##

edit_action = QAction(('&Правка Аудио и Картинок из полей' if lang == 'ru' else _('&Edit Audio Images from fields')), mw)
edit_action.setShortcut(QKeySequence(HOTKEY['edit'][0]))
edit_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit-audio-images.png')))
mw.connect(edit_action, SIGNAL('triggered()'), JustDoItByYourself)

mw.form.menuEdit.addSeparator()
mw.form.menuEdit.addAction(edit_action)
mw.form.menuEdit.addSeparator()

def edit_ai_off():
    edit_action.setEnabled(False)

def edit_ai_on():
    edit_action.setEnabled(True)

mw.deckBrowser.show = wrap(mw.deckBrowser.show, edit_ai_off)
mw.overview.show = wrap(mw.overview.show, edit_ai_off)
mw.reviewer.show = wrap(mw.reviewer.show, edit_ai_on)

##

def edit_ai_buttons(editor):
    """Add the buttons to the editor."""
    editor._addButton('image', lambda edito=editor: TryItByYourself(edito) , HOTKEY['edit'][0],
                       #text='', icon=os.path.join(MUSTHAVE_COLOR_ICONS, 'edit-audio-images.png'),
                       tip='Edit Audio Images from fields in external editor (' + HOTKEY['edit'][0] +')')

# register callback function that gets executed after setupEditorButtons has run. 
# See Editor.setupEditorButtons for details
addHook('setupEditorButtons', edit_ai_buttons)

##
