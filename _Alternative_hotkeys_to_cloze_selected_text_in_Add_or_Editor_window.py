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

from aqt.utils import tooltip, showInfo
from anki.hooks import wrap
import aqt.editor
from aqt.editor import *

# You can set up your own hotkeys here:
HOTKEY = {
    "next_cloze": 'Ctrl+Space',
    "same_cloze": 'Ctrl+Alt+Space',

    'same_without_Alt': 'F1',
    "next_closure": 'F2',  # 'Ctrl+Shift+C'
    "same_closure": 'Alt+F2',  # 'Ctrl+Alt+Shift+C'
    # old style

    # Ctrl+F11 don't work
    "LaTeX": 'Alt+F11',  # "Ctrl+T, T"
    "LaTeX$": 'F11',       # "Ctrl+T, E"
    "LaTeX$$": 'Shift+F11',  # "Ctrl+T, M"
}


def onAltCloze(self, delta):
    # check that the model is set up for cloze deletion
    if not re.search('{{(.*:)*cloze:', self.note.model()['tmpls'][0]['qfmt']):
        if self.addMode:
            tooltip(_("Warning, cloze deletions will not work until " +
                      "you switch the type at the top to Cloze."))
        else:
            showInfo(_("""\
To make a cloze deletion on an existing note, you need to change it \
to a cloze type first, via Edit>Change Note Type."""))
            return
    # find the highest existing cloze
    highest = 0
    for name, val in self.note.items():
        m = re.findall("\{\{c(\d+)::", val)
        if m:
            highest = max(highest, sorted([int(x) for x in m])[-1])
    # reuse last?
    # if not self.mw.app.keyboardModifiers() & Qt.AltModifier:
    highest += delta
    # must start at 1
    highest = max(1, highest)
    self.web.eval("wrap('{{c%d::', '}}');" % highest)


def setupButtonz(self):
    s = QShortcut(
        QKeySequence(HOTKEY["next_cloze"]), self.parentWindow)
    s.connect(s, SIGNAL('activated()'), self.onCloze)

    s = QShortcut(
        QKeySequence(HOTKEY["same_cloze"]), self.parentWindow)
    s.connect(s, SIGNAL('activated()'), self.onCloze)

    s = QShortcut(
        QKeySequence(HOTKEY['same_without_Alt']), self.parentWindow)
    s.connect(s, SIGNAL('activated()'), lambda: onAltCloze(self, 0))

    s = QShortcut(
        QKeySequence(HOTKEY["next_closure"]), self.parentWindow)
    s.connect(s, SIGNAL('activated()'), self.onCloze)

    s = QShortcut(
        QKeySequence(HOTKEY["same_closure"]), self.parentWindow)
    s.connect(s, SIGNAL('activated()'), self.onCloze)

    s = QShortcut(QKeySequence(HOTKEY["LaTeX"]), self.widget)
    s.connect(s, SIGNAL("activated()"), self.insertLatex)
    s = QShortcut(QKeySequence(HOTKEY["LaTeX$"]), self.widget)
    s.connect(s, SIGNAL("activated()"), self.insertLatexEqn)
    s = QShortcut(QKeySequence(HOTKEY["LaTeX$$"]), self.widget)
    s.connect(s, SIGNAL("activated()"), self.insertLatexMathEnv)

aqt.editor.Editor.setupButtons = wrap(
    aqt.editor.Editor.setupButtons, setupButtonz)
