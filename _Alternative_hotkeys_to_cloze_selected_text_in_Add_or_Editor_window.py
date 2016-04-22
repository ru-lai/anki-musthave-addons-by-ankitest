# -*- mode: Python ; coding: utf-8 -*-

CtrlSpace = "Ctrl+Space"
CtrlAltSpace = "Ctrl+Alt+Space"

import aqt.editor
from aqt.editor import *
from anki.hooks import wrap

def setupButtonz(self):
    s = QShortcut(
        QKeySequence(CtrlSpace), self.parentWindow)
    s.connect(s, SIGNAL("activated()"), self.onCloze)

    s = QShortcut(
        QKeySequence(CtrlAltSpace), self.parentWindow)
    s.connect(s, SIGNAL("activated()"), self.onCloze)

aqt.editor.Editor.setupButtons = wrap(aqt.editor.Editor.setupButtons, setupButtonz)
