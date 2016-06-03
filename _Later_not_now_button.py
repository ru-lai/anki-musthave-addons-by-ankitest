# -*- mode: Python ; coding: utf-8 -*-
# • Later not now button
# https://ankiweb.net/shared/info/777151722
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# No answer will be given, next card will be shown.
#  Card stays on its place in queue,
#   you'll see it next time you study the deck.
#
#    Hotkey: Escape shortcut (Esc).
#
# inspired by More Answer Buttons for New Cards add-on
# https://ankiweb.net/shared/info/468253198
#
# No support. Use it AS IS on your own risk.
from __future__ import unicode_literals
import json
from aqt.reviewer import Reviewer
from anki.hooks import wrap
from aqt import mw

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Get language class
import anki.lang
lang = anki.lang.getLang()

# Anki uses a single digit to track which button has been clicked.
NOT_NOW_BASE = 5


def _answerButtons(self):
    times = []
    default = self._defaultEase()

    def but(i, label):
        if i == default:
            extra = 'id=defease'
        else:
            extra = ''
        due = self._buttonTime(i)
        return '''
<td align=center>%s<button %s title="%s" onclick="py.link('ease%d');">\
%s</button></td>''' % (due, extra, _('Shortcut key: %s') % i, i, label)

    buf = '<center><table cellpading=0 cellspacing=0><tr>'
    buf += '''
<td align=center><span class=nobold>%s</span><br><button
title="Short key: %s" onclick="py.link('ease%d');">\
%s</button></td><td>&nbsp;</td>''' % (
        'позже' if lang == 'ru' else _('later'), 'Escape', NOT_NOW_BASE,
        'не сейчас' if lang == 'ru' else _('not now'))

    for ease, label in self._answerButtonList():
        buf += but(ease, label)
    buf += '</tr></table>'
    script = "<script>$(function () { $('#defease').focus(); });</script>"
    return buf + script


def answer_card_intercepting(self, actual_ease, _old):
    ease = actual_ease
    if actual_ease >= NOT_NOW_BASE:
        self.nextCard()
        return True
    else:
        return _old(self, ease)

Reviewer._answerButtons = _answerButtons
Reviewer._answerCard = wrap(
    Reviewer._answerCard, answer_card_intercepting, 'around')


def onEscape():
    mw.reviewer.nextCard()

try:
    mw.addon_cards_menu
except AttributeError:
    mw.addon_cards_menu = QMenu(
        _(u'&Карточки') if lang == 'ru' else _(u'&Cards'), mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_cards_menu)

escape_action = QAction(mw)
escape_action.setText(u'Позж&е, не сейчас' if lang ==
                      'ru' else _(u'&Later, not now'))
escape_action.setShortcut(QKeySequence('Escape'))
escape_action.setEnabled(False)
mw.connect(escape_action, SIGNAL('triggered()'), onEscape)

# mw.addon_cards_menu.addSeparator()
mw.addon_cards_menu.addAction(escape_action)
# mw.addon_cards_menu.addSeparator()

mw.deckBrowser.show = wrap(
    mw.deckBrowser.show, lambda: escape_action.setEnabled(False))
mw.overview.show = wrap(
    mw.overview.show, lambda: escape_action.setEnabled(False))
mw.reviewer.show = wrap(
    mw.reviewer.show, lambda: escape_action.setEnabled(True))


def newRemaining(self):
    if not self.mw.col.conf['dueCounts']:
        return 0
    idx = self.mw.col.sched.countIdx(self.card)
    if self.hadCardQueue:
        # if it's come from the undo queue, don't count it separately
        counts = list(self.mw.col.sched.counts())
    else:
        counts = list(self.mw.col.sched.counts(self.card))
    return (idx == 0 and counts[0] < 1)


def myShowAnswerButton(self, _old):
    if newRemaining(self):
        # self.mw.moveToState('deckBrowser')
        self.mw.moveToState('overview')
    self._bottomReady = True
    if not self.typeCorrect:
        self.bottom.web.setFocus()

    buf = '''
<td align=center class=stat2><span class=stattxt>%s</span><br><button
title="Short key: %s" onclick="py.link('ease%d');">\
%s</button></td><td>&nbsp;</td>''' % (
        'позже' if lang == 'ru' else _('later'), 'Escape', NOT_NOW_BASE,
        'не сейчас' if lang == 'ru' else _('not now'))

    middle = '''<table cellpadding=0><tr>%s<td class=stat2 align=center>
<span class=stattxt>%s</span><br>
<button %s id=ansbut style="display:inline-block;width:%s;%s"
onclick="py.link('ans');">%s</button>
    </td></tr></table>
''' % (buf, self._remaining(),
       ' title=" ' + (_('Shortcut key: %s') % _('Space')) + ' "',
       '99%', '', _('Show Answer'))

    if self.card.shouldShowTimer():
        maxTime = self.card.timeLimit() / 1000
    else:
        maxTime = 0
    self.bottom.web.eval('showQuestion(%s,%d);' % (
        json.dumps(middle), maxTime))
    return True

Reviewer._showAnswerButton = wrap(
    Reviewer._showAnswerButton, myShowAnswerButton, 'around')
