# -*- mode: Python ; coding: utf-8 -*-
# ' Empty Cards Check Media Database
# github / dae / anki / designer / main.ui
# -- tested with Anki 2.0.41 under Windows 7 SP1
# https://ankiweb.net/shared/info/445912450
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2017 Dmitry Mikheev, http://finpapa.ucoz.ru/index.html
import aqt
from PyQt4.QtGui import *

aqt.mw.form.actionFullDatabaseCheck.setShortcut(
    QKeySequence('Ctrl+Delete'))  # Check Database...

aqt.mw.form.actionCheckMediaDatabase.setShortcut(
    QKeySequence('Alt+Shift+Delete'))  # Check Media...

aqt.mw.form.actionEmptyCards.setShortcut(
    QKeySequence('Ctrl+Shift+Delete'))  # Empty Cards...

# https://github.com/dae/anki/blob/master/designer/main.ui
