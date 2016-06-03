# -*- mode: Python ; coding: utf-8 -*-
# ~ Alternative hotkeys to cloze selected text in Add or Editor window
# https://ankiweb.net/shared/info/
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# Ctrl+Space which cloze selected text with maximum+1 number
# and Ctrl+Alt+Space which cloze selected text with maximum number.
#
# New keys are synonyms for old keys Ctrl+Shift+C
# and Ctrl+Alt+Shift+C respectively.
#
# You can invent your own keys combinations, specify them
# at the beginning of the source code and restart Anki. 
#
# No support. Use it AS IS on your own risk.

from anki.hooks import wrap
import aqt.editor
from aqt.editor import *

CtrlSpace = 'Ctrl+Space'
CtrlAltSpace = 'Ctrl+Alt+Space'


def setupButtonz(self):
    s = QShortcut(
        QKeySequence(CtrlSpace), self.parentWindow)
    s.connect(s, SIGNAL('activated()'), self.onCloze)

    s = QShortcut(
        QKeySequence(CtrlAltSpace), self.parentWindow)
    s.connect(s, SIGNAL('activated()'), self.onCloze)

aqt.editor.Editor.setupButtons = wrap(
    aqt.editor.Editor.setupButtons, setupButtonz)
