# -*- mode: Python ; coding: utf-8 -*-
# _REPL_print_Debug_Console.py
# https://ankiweb.net/shared/info/887733884
# https://github.com/ankitest/anki-musthave-addonz-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.ru/
# No support. Use it AS IS on your own risk.
"""
' REPL print Debug Console
"""
from __future__ import unicode_literals

import anki
import aqt

from aqt import mw
from aqt.qt import *

import anki.lang
_lang = anki.lang.getLang()

HOTKEY = "Ctrl+Shift+D"

def _REPL():
    action = QAction(
        "&Отладка REPL print Debug Console" if _lang == "ru" else
        'REPL print &Debug Console', mw)
    action.setShortcut(QKeySequence(HOTKEY))
    action.triggered.connect(lambda: mw.onDebug())
    mw.form.menuTools.insertAction(mw.form.actionNoteTypes, action)
    font = action.font()
    font.setBold(True)
    action.setFont(font)
    action.setIcon(QIcon(':/icons/colors.png'))
    # mw.form.menuTools.insertSeparator(mw.form.actionNoteTypes)

_REPL()
