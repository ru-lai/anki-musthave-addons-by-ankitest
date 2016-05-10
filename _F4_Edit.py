# -*- mode: Python ; coding: utf-8 -*-
# • F4 Edit
# https://ankiweb.net/shared/info/2085904433
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
from __future__ import unicode_literals
from __future__ import division
import os, sys, datetime

# You can set up your own hotkeys here:
HOTKEY = {      # in Reviewer
    'Edit_HTML'     : 'F4',         # Ctrl+Shift+X
    'Edit_Fields'   : 'F4',         # e
    'Edit_Cards'    : 'Shift+F4'    # 
    }

if __name__ == "__main__":
    print("This is _F4_Edit add-on for the Anki program and it can't be run directly.")
    print("Please download Anki 2.0 from http://ankisrs.net/")
    sys.exit()
else:
    pass

if sys.version[0] == '2': # Python 3 is utf8 only already.
  if hasattr(sys,'setdefaultencoding'):
    sys.setdefaultencoding('utf8')

from aqt import mw
from anki.hooks import addHook, wrap, runHook
from aqt.editor import Editor # the editor when you click "Add" in Anki
import aqt.clayout

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Get language class
import anki.lang
lang = anki.lang.getLang()

try:
    MUSTHAVE_COLOR_ICONS = os.path.join(mw.pm.addonFolder(), 'f4edit_icons')
except:
    MUSTHAVE_COLOR_ICONS = ''

# 
##########################################################

def go_edit_current():
    """Edit the current card when there is one."""
    try:
        mw.onEditCurrent()
    except AttributeError:
        pass

def go_edit_layout():
    """Edit the current card's note's layout if there is one."""
    try:
        ccard = mw.reviewer.card
        aqt.clayout.CardLayout(mw, ccard.note(), ord=ccard.ord)
    except AttributeError:
        return

try:
    mw.addon_cards_menu
except AttributeError:
    mw.addon_cards_menu = QMenu(_(u"&Карточки") if lang == 'ru' else _(u"&Cards"), mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_cards_menu)

F4_edit_current_action = QAction(mw)
F4_edit_current_action.setText(u'Р&едактирование...' if lang=='ru' else _(u"&Edit..."))
F4_edit_current_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_current.png')))
F4_edit_current_action.setShortcut(QKeySequence(HOTKEY['Edit_Fields']))
F4_edit_current_action.setEnabled(False)
mw.connect(F4_edit_current_action, SIGNAL("triggered()"), go_edit_current)

F4_edit_layout_action = QAction(mw)
F4_edit_layout_action.setText(u'&Карточки...' if lang=='ru' else _(u"&Cards..."))
F4_edit_layout_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_layout.png')))
F4_edit_layout_action.setShortcut(QKeySequence(HOTKEY['Edit_Cards']))
F4_edit_layout_action.setEnabled(False)
mw.connect(F4_edit_layout_action, SIGNAL("triggered()"), go_edit_layout)

mw.addon_cards_menu.addSeparator()
mw.addon_cards_menu.addAction(F4_edit_current_action)
mw.addon_cards_menu.addAction(F4_edit_layout_action)
mw.addon_cards_menu.addSeparator()

def swap_off():
    F4_edit_current_action.setEnabled(False)
    F4_edit_layout_action.setEnabled(False)

def swap_on():
    F4_edit_current_action.setEnabled(True)
    F4_edit_layout_action.setEnabled(True)

mw.deckBrowser.show = wrap(mw.deckBrowser.show, swap_off)
mw.overview.show = wrap(mw.overview.show, swap_off)
mw.reviewer.show = wrap(mw.reviewer.show, swap_on)

# F4 as well as Ctrl+Shift+X in Fields Editor 
#   (Add Card, Edit Card, Browse)
######################################################################

def myHTMLeditF4(self):
    f4 = QShortcut(
         QKeySequence(HOTKEY['Edit_HTML']), self.parentWindow)
    f4.connect(f4, SIGNAL("activated()"), self.onHtmlEdit)

Editor.setupButtons = wrap(Editor.setupButtons, myHTMLeditF4)

##
