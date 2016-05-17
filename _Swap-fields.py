# -*- mode: Python ; coding: utf-8 -*-
# • Swap fields
# https://ankiweb.net/shared/info/1040866511
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
from __future__ import division
from __future__ import unicode_literals
import os, sys, datetime

if __name__ == '__main__':
    print("This is _Swap_fields add-on for the Anki program and it can't be run directly.")
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2': # Python 3 is utf8 only already.
  if hasattr(sys,'setdefaultencoding'):
    sys.setdefaultencoding('utf8')

CASE_SENSITIVE = True # False # 

SWAP_TAG = False
#SWAP_TAG = datetime.datetime.now().strftime('swapped::swap-%Y-%m-%d') #-%H:%M:%S')
#SWAP_TAG = datetime.datetime.now().strftime('sw-%y-%m-%d') 

fldlst = [
    ['En','Ru'],
    ['Eng','Rus'],
    ['English','Russian'],
    ['по-английски','по-русски'],
    ['Q','A'], ['В','О'], 
    ['Question','Answer'],
    [_('Question'),_('Answer')],
    ['Front','Back'],
    [_('Front'),_('Back')], # Вопрос, Ответ
    ]

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
    MUSTHAVE_COLOR_ICONS = os.path.join(mw.pm.addonFolder(), 'swap_icons')
except:
    MUSTHAVE_COLOR_ICONS = ''

HOTKEY = {      # in mw Main Window (deckBrowser, Overview, Reviewer)
    'swap'  : ['F12', '', '', ''' ''', """ """], 
    }

##

import anki.notes
from anki.consts import MODEL_STD, MODEL_CLOZE

fld1st = _('Front') # Вопрос
fld2nd = _('Back') # Ответ

def JustDoIt(note, ecf):
    global fld1st, fld2nd
    """
    if not (mw.reviewer.state == 'question' or mw.reviewer.state == 'answer'):
     showCritical('''Обмен в списке колод или в окне колоды невозможен,
      <br>только при просмотре (заучивании) карточек.''' \
        if lang=='ru' else 'Swap fields is available only for cards,<br>not for decks panel nor deck overview as well.')
     return
    if not hasattr(mw.reviewer.card,'model'):
     showCritical('Извините, конечно, но пока делать просто нечего!' \
        if lang=='ru' else 'Oops, <s>I did it again!</s> there is <b>nothing to do</b> yet!')
     return
    """
    #c = mw.reviewer.card
    if note.model()['type'] == MODEL_CLOZE:
        showCritical('''<center>Обмен полей для типа записей <b>с пропусками</b><br> \
            не поддерживается. Только вручную.</center>''' \
            if lang=='ru' else '''<div style="text-align:center;">
It's unable to swap fields of CLOZE note type automatically.
<br>Please, do it manually by yourself.</div>''') 

        # Unfortunately, style="text-align:center;" does not work here. But <center> works.

    elif note.model()['type'] == MODEL_STD:
        fldn = note.model()['flds']
        fldl = len(note.fields)

        audioSound = False
        for fld in fldn:
            if fld['name'].lower()=='audio' or fld['name'].lower()=='sound':
               audioSound = True
               break

        fnd1st = False
        fnd2nd = False

        if ecf != None:
           fnd = fldn[ecf]['name']
           for lst in fldlst:
            if CASE_SENSITIVE:
                found = fnd==lst[0]
            else:
                found = fnd.lower()==lst[0].lower()
            if found:
               fnd1st = True
               fld1st = fnd
               fnd2nd = True
               fld2nd = lst[1]
               break
            else:
               for lst in fldlst:
                if CASE_SENSITIVE:
                    found = fnd==lst[1]
                else:
                    found = fnd.lower()==lst[1].lower()
                if found:
                   fnd1st = True
                   fld1st = lst[0]
                   fnd2nd = True
                   fld2nd = fnd
                   break

        if not fnd1st:
         for lst in fldlst:
          for fld in fldn:
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

        if not fnd2nd:
         for lst in fldlst:
          for fld in fldn:
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
            showCritical('У данной записи одно-единственное поле,<br> его просто не с чем обменивать.' \
                if lang=='ru' else 'It is unable to swap a note with a single field in it.')
            return

        elif fldl==2: # There are two fields only? Swap it anyway.
            fld1st = fldn[0]['name']
            fld2nd = fldn[1]['name']
            swap_fld = note[fld1st]
            note[fld1st] = note[fld2nd]
            note[fld2nd] = swap_fld

        elif fldl==3 and audioSound: 
            # There are three fields only? With Audio or Sound? Swap other two anyway.
            fld1st = ''
            fld2nd = ''
            for fld in fldn:
                if fld['name'].lower()!='audio' \
                        and fld['name'].lower()!='sound' and fld1st=='':
                    fld1st = fld['name']
                if fld['name'].lower()!='audio' \
                        and fld['name'].lower()!='sound' and fld2nd=='' and fld['name']!=fld1st:
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
            # Swap fields by name if names are found in list. 
            swap_fld = note[fld1st]
            note[fld1st] = note[fld2nd]
            note[fld2nd] = swap_fld

        else:
            # Otherwise swap two first fields anyway.
            fld1st = fldn[0]['name']
            fld2nd = fldn[1]['name']
            swap_fld = note[fld1st]
            note[fld1st] = note[fld2nd]
            note[fld2nd] = swap_fld

        if SWAP_TAG:
            if not note.hasTag(SWAP_TAG):
                note.addTag(SWAP_TAG)

        note.flush()  # never forget to flush
        tooltip(('Выполнен обмен значений между полями <b>%s</b> и <b>%s</b>.' \
            if lang=='ru' else '<b>%s</b> and <b>%s</b> swapped.')%(fld1st,fld2nd), period=2000)

def JustDoItYourself():
    rst = mw.reviewer.state 
    NB = mw.reviewer.card.note()
    JustDoIt(NB, None)
    mw.reset()  # refresh gui
    if rst == 'answer':
        mw.reviewer._showAnswer() # ._showAnswerHack()

def TryItYourself(edit):
    edcufi = edit.currentField
    JustDoIt(edit.note, edcufi)
    mw.reset()  # refresh gui
    # focus field so it's saved
    edit.web.setFocus()
    edit.web.eval('focusField(%d);' % edcufi)

##

swap_action = QAction(('О&бмен полей %s и %s' if lang == 'ru' \
    else _('S&wap %s and %s fields'))%(fld1st,fld2nd), mw)
swap_action.setShortcut(QKeySequence(HOTKEY['swap'][0]))
swap_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'swap.png')))
mw.connect(swap_action, SIGNAL('triggered()'), JustDoItYourself)

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
    '''Add the buttons to the editor.'''
    editor._addButton('swap_fields', lambda edito=editor: TryItYourself(edito) , 
        HOTKEY['swap'][0], text='Sw', 
        tip=('Обмен полей' if lang=='ru' else _('Swap fields'))+' (' + HOTKEY['swap'][0] +')')

# register callback function that gets executed after setupEditorButtons has run. 
# See Editor.setupEditorButtons for details
addHook('setupEditorButtons', setup_buttons)

# reset_card_scheduling.py
# https://ankiweb.net/shared/info/1432861881
# Reset card(s) scheduling information / progress
#######################################################

# Col is a collection of cards, cids are the ids of the cards to reset.
def swapSelectedNotes(self):
    ''' Resets statistics for selected cards, and removes them from learning queues. '''
    nids = self.selectedNotes()
    if not nids:
        return
    # Allow undo
    self.mw.checkpoint('Обмен полей' if lang=='ru' else _('Swap fields'))
    self.mw.progress.start(immediate=True)
    # Not sure if beginReset is required
    self.model.beginReset()

    # Resets selected cards in current collection
    # self.col.sched.resetCards(cids)
    # Removes card from dynamic deck?
    # self.col.sched.remFromDyn(cids)
    # Removes card from learning queues
    # self.col.sched.removeLrn(cids)

    for nid in nids:
        JustDoIt(mw.col.getNote(nid), None)
    mw.reset()  # refresh gui

    self.model.endReset()
    self.mw.progress.finish()
    # Update the main UI window to reflect changes in card status
    self.mw.reset()

def addMenuItem(self):
    ''' Adds hook to the Edit menu in the note browser '''
    swp_action = QAction('Обмен полей' if lang=='ru' else _('Swap fields'), self)
    swp_action.setShortcut(QKeySequence(HOTKEY['swap'][0]))
    #self.resetSelectedCardScheduling = resetSelectedCardScheduling
    self.connect(swp_action, SIGNAL('triggered()'), lambda s=self: swapSelectedNotes(self))
    self.form.menuEdit.addAction(swp_action)

# Add-in hook; called by the AQT Browser object when it is ready for the add-on to modify the menus
addHook('browser.setupMenus', addMenuItem)