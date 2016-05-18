# -*- mode: Python ; coding: utf-8 -*-
# • Collapse Them All
# https://ankiweb.net/shared/info/1846969611
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# 
# Expand/Collapse Browser Tree
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
from __future__ import unicode_literals

CtrlShiftPlus  = 'Ctrl+Shift++'  # Expand   Them All
CtrlShiftMinus = 'Ctrl+Shift+-' # Collapse Them All

from anki.hooks import addHook

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QKeySequence

#####################
# Get language class
# Выбранный пользователем язык программной оболочки
import anki.lang
lang = anki.lang.getLang()

def setupMenu(self):
    menu = self.form.menuJump #.menuEdit
    menu.addSeparator()

    a = menu.addAction('Развернуть всё дерево' if lang=='ru' else _('Expand Them All'))
    a.setShortcut(QKeySequence(CtrlShiftPlus))
    self.connect(a, SIGNAL('triggered()'), lambda b=self: ExpandThemAll(b, True))

    a = menu.addAction('Свернуть все ветки' if lang=='ru' else _('Collapse Them All'))
    a.setShortcut(QKeySequence(CtrlShiftMinus))
    self.connect(a, SIGNAL('triggered()'), lambda b=self: ExpandThemAll(b, False))

    menu.addSeparator()

def ExpandThemAll(self, action):
    if action:
        self.form.tree.expandAll()
    else:
        self.form.tree.collapseAll()

addHook('browser.setupMenus', setupMenu)
