# -*- mode: Python ; coding: utf-8 -*-
# • Swap 
# https://ankiweb.net/shared/info/1040866511
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
from __future__ import division
from __future__ import unicode_literals
import os, sys

if __name__ == "__main__":
    print("This is _Swap add-on for the Anki program and it can't be run directly.")
    print("Please download Anki 2.0 from http://ankisrs.net/")
    sys.exit()
else:
    pass

if sys.version[0] == '2': # Python 3 is utf8 only already.
  if hasattr(sys,'setdefaultencoding'):
    sys.setdefaultencoding('utf8')

CASE_SENSITIVE = False # True # 

fldlst = [
    ['En','Ru'],
    ['Eng','Rus'],
    ['English','Russian'],
    ['по-английски','по-русски'],
    ['Q','A'],
    ['Question','Answer'],
    [_('Question'),_('Answer')],
    ['Front','Back'],
    [_('Front'),_('Back')], # Вопрос, Ответ
    ]

from aqt import mw
from aqt.utils import tooltip, showInfo, showWarning, showCritical
from anki.hooks import addHook, wrap, runHook
from aqt.editor import Editor # the editor when you click "Add" in Anki

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Get language class
import anki.lang
lang = anki.lang.getLang()

try:
    MUSTHAVE_COLOR_ICONS = os.path.join(mw.pm.addonFolder(), 'swap_icons')
except:
    MUSTHAVE_COLOR_ICONS = ''

HOTKEY = {      # in mw Main Window (deckBrowser, Overview, Reviewer)
    'swap'  : ["F12", '', "", ''' ''', """ """], 
    }

##

from anki.consts import MODEL_STD, MODEL_CLOZE

fld1st = _('Front') # Вопрос
fld2nd = _('Back') # Ответ

def JustDoIt(note):
  global fld1st, fld2nd
  if not (mw.reviewer.state == 'question' or mw.reviewer.state == 'answer'):
    showCritical("Обмен в списке колод или в окне колоды невозможен,<br>только при просмотре (заучивании) карточек." if lang=='ru' else 'Swap is available only for cards,<br>not for decks panel nor deck overview as well.')
  else:
   if not hasattr(mw.reviewer.card,'model'):
    showCritical("Извините, конечно, но пока делать просто нечего!" if lang=='ru' else 'Oops, <s>I did it again!</s> there is <b>nothing to do</b> yet!')
   else:
    c = mw.reviewer.card
    if c.model()['type'] == MODEL_CLOZE:
        showCritical("<center>Обмен полей для типа записей <b>с пропусками</b><br> не поддерживается. Только вручную.</center>" if lang=='ru' else """<div style="text-align:center;">It's unable to swap fields of CLOZE note type automatically.<br>Please, do it manually by yourself.</div>""") 
        # Unfortunately, style="text-align:center;" does not work here. But <center> works.
    elif c.model()['type'] == MODEL_STD:
        fldn = note.model()['flds']
        fldl = len(note.fields)

        audioSound = False
        for fld in fldn:
            if fld['name'].lower()=='audio' or fld['name'].lower()=='sound':
               audioSound = True
               break

        fnd1st = False
        for fld in fldn:
          for lst in fldlst:
            if CASE_SENSITIVE:
                found = fld['name']==lst[0]
            else:
                found = fld['name'].lower()==lst[0].lower()
            if found:
               fnd1st = True
               fld1st = fld['name']
               break
          else:
            continue
          break

        fnd2nd = False
        for fld in fldn:
          for lst in fldlst:
            if CASE_SENSITIVE:
                found = fld['name']==lst[1] and lst[0]==fld1st
            else:
                found = fld['name'].lower()==lst[1].lower() and lst[0].lower()==fld1st.lower()
            if found:
               fnd2nd = True
               fld2nd = fld['name']
               break
          else:
            continue
          break

        if fldl<2:
            showCritical("У данной записи одно-единственное поле,<br> его просто не с чем обменивать." if lang=='ru' else 'It is unable to swap a note with a single field in it.')
            return

        elif fldl==2: # There are two fields only? Swap it anyway.
            fld1st = fldn[0]['name']
            fld2nd = fldn[1]['name']
            swap_fld = note[fld1st]
            note[fld1st] = note[fld2nd]
            note[fld2nd] = swap_fld

        elif fldl==3 and audioSound: # There are three fields only? With Audio or Sound? Swap other two anyway.
            fld1st = ''
            fld2nd = ''
            for fld in fldn:
                if fld['name'].lower()!='audio' and fld['name'].lower()!='sound' and fld1st=='':
                    fld1st = fld['name']
                if fld['name'].lower()!='audio' and fld['name'].lower()!='sound' and fld2nd=='' and fld['name']!=fld1st:
                    fld2nd = fld['name']
            if fld1st!='' and fld2nd!='':
                showInfo(unicode(fld1st)+' '+unicode(fld2nd))
                swap_fld = note[fld1st]
                note[fld1st] = note[fld2nd]
                note[fld2nd] = swap_fld
            else:
                showCritical('3 поля, но есть и Audio, и Sound. Что с чем обменивать-то тогда?')
                return 

        # There are 3 (w/o Audio/Sound) or 4 or more fields?
        elif fnd1st and fnd2nd:
            # Swap by name if names are found in list. 
            swap_fld = note[fld1st]
            note[fld1st] = note[fld2nd]
            note[fld2nd] = swap_fld

        else:
            # Otherwise swap two first anyway.
            fld1st = fldn[0]['name']
            fld2nd = fldn[1]['name']
            swap_fld = note[fld1st]
            note[fld1st] = note[fld2nd]
            note[fld2nd] = swap_fld

        note.flush()  # never forget to flush
        tooltip(("Выполнен обмен значений между полями <b>%s</b> и <b>%s</b>." if lang=='ru' else '<b>%s</b> and <b>%s</b> swapped.')%(fld1st,fld2nd))

def JustDoItYourself():
    rst = mw.reviewer.state 
    NB = mw.reviewer.card.note()
    JustDoIt(NB)
    mw.reset()  # refresh gui
    if rst == 'answer':
        mw.reviewer._showAnswer() # ._showAnswerHack()

def TryItYourself(edit):
    JustDoIt(edit.note)
    mw.reset()  # refresh gui
    # focus field so it's saved
    edit.web.setFocus()
    edit.web.eval("focusField(%d);" % edit.currentField)

##

swap_action = QAction(('О&бмен полей %s и %s' if lang == 'ru' else _('S&wap %s and %s fields'))%(fld1st,fld2nd), mw)
swap_action.setShortcut(QKeySequence(HOTKEY['swap'][0]))
swap_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'swap.png')))
mw.connect(swap_action, SIGNAL("triggered()"), JustDoItYourself)

mw.form.menuEdit.addSeparator()
mw.form.menuEdit.addAction(swap_action)
mw.form.menuEdit.addSeparator()

def swap_off():
    swap_action.setEnabled(False)

def swap_on():
    swap_action.setEnabled(True)

mw.deckBrowser.show = wrap(mw.deckBrowser.show, swap_off)
mw.overview.show = wrap(mw.overview.show, swap_off)
mw.reviewer.show = wrap(mw.reviewer.show, swap_on)

##

def setup_buttons(editor):
    """Add the buttons to the editor."""
    editor._addButton("swap_fields", lambda edito=editor: TryItYourself(edito) , HOTKEY['swap'][0],
                       text="Sw", tip="Swap fields (" + HOTKEY['swap'][0] +")")

# register callback function that gets executed after setupEditorButtons has run. 
# See Editor.setupEditorButtons for details
addHook("setupEditorButtons", setup_buttons)

##
