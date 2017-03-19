# -*- mode: Python ; coding: utf-8 -*-
# • Collapse Them All
# https://ankiweb.net/shared/info/1846969611
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# Expand/Collapse Browser Tree
#
# Creates two options in Go menu to expand and collapse all items
# (Favourites searches, Decks and Tags) in Browse window.
#
#    Just press the Ctrl+Shift+Minus to collapse
#    and Ctrl+Shift+Plus keys to expand and view sub-decks.
#
# No support. Use it AS IS on your own risk.
from __future__ import unicode_literals

from anki.hooks import addHook

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QKeySequence

#####################
# Get language class
# Выбранный пользователем язык программной оболочки
import anki.lang
lang = anki.lang.getLang()

HOTKEY = {
    'CtrlShiftPlus': 'Ctrl+Shift++',  # Expand   Them All
    'CtrlShiftMinus': 'Ctrl+Shift+-',  # Collapse Them All
    }


def setupMenu(self):
    menu = self.form.menuJump  # .menuEdit
    menu.addSeparator()

    a = menu.addAction('Развернуть всё дерево' if lang ==
                       'ru' else _('Expand Them All'))
    a.setShortcut(HOTKEY['CtrlShiftPlus'])
    self.connect(a, SIGNAL('triggered()'),
                 lambda b=self: ExpandThemAll(b, True))

    a = menu.addAction('Свернуть все ветки' if lang ==
                       'ru' else _('Collapse Them All'))
    a.setShortcut(HOTKEY['CtrlShiftMinus'])
    self.connect(a, SIGNAL('triggered()'),
                 lambda b=self: ExpandThemAll(b, False))

    menu.addSeparator()


def ExpandThemAll(self, action):
    if action:
        self.form.tree.expandAll()
    else:
        self.form.tree.collapseAll()

addHook('browser.setupMenus', setupMenu)
