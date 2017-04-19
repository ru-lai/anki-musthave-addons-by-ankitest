# -*- mode: Python ; coding: utf-8 -*-
# • Timebox tooltip
# https://ankiweb.net/shared/info/2014169675
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 It puts the stats when you finish a timebox in a tooltip message
  that goes away after a few seconds.
"""
from __future__ import division

from anki.hooks import wrap
from anki.sound import playFromText, clearAudioQueue, play
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import tooltip

# anki/collection.py: .timeboxReached() .startTimebox()
# aqt/reviewer.py: .nextCard

# Based on Decks Total https://ankiweb.net/shared/info/1421528223
# https://github.com/b50/anki-deck-stats
# Author of original addon: Calumks <calumks@gmail.com>
import os
import time

# Get DeckBrowser class
from aqt.deckbrowser import DeckBrowser

from anki.lang import ngettext
from anki.hooks import wrap

# Get fmtTimeSpan required for renderStats method
from anki.utils import fmtTimeSpan

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Get language class
# Выбранный пользователем язык программной оболочки
import anki.lang
lang = anki.lang.getLang()

MSG = {
    'en': {
        'View': _('&View'),
        },
    'ru': {
        'View': '&Вид',
        },
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

HOTKEY = {
    'timebox': "Ctrl+Shift+T"
    }

__addon__ = "'" + __name__.replace('_',' ')
__version__ = "2.0.44a"


def renderOstrich(self):

    # Get due and new cards
    new = 0
    lrn = 0
    due = 0

    for tree in self.mw.col.sched.deckDueTree():
        new += tree[4]
        lrn += tree[3]
        due += tree[2]
    total = new + lrn + due

    # Get studdied cards
    cards, thetime = self.mw.col.db.first(
            """select count(), sum(time)/1000 from revlog where id > ?""",
            (self.mw.col.sched.dayCutoff - 86400) * 1000)

    cards = cards or 0
    thetime = thetime or 0

    speed = cards * 60 / max(1, thetime)
    minutes = int(total / max(1, speed))

    msgp1 = ngettext("%d card", "%d cards", cards) % cards

    buf = "" + _("Average") \
        + ": " + _("%.01f cards/minute") % (speed) + " &nbsp; " \
        + _("More") + "&nbsp;" + ngettext(
             "%s minute.", "%s minutes.", minutes) % (
                "<b>"+str(minutes)+"</b>")

    return buf


def timeboxReached(self):
    "Return (elapsedTime, reps)"
    if not self.conf['timeLim']:
        # timeboxing disabled
        return False
    elapsed = time.time() - self._startTime
    return (self.conf['timeLim'], self.sched.reps - self._startReps)


def maProc(self, elapsed):
        part1 = ngettext('%d card studied in',
                         '%d cards studied in', elapsed[1]) % elapsed[1]
        mins = int(round(elapsed[0] / 60))
        part2 = ngettext('%s minute.', '%s minutes.', mins) % mins
        tooltip(
            '<big><b style=font-size:larger;color:blue;font-weight:bold;>' +
            '%s <span style=color:red>%s</span></b> <br><br> %s</big>' % (
                part1, part2, renderOstrich(self)), period=8000)


def myInfoCards(self):
    elapsed = timeboxReached(self.mw.col)
    if elapsed:
        maProc(self, elapsed)


def maNextCard(self):
    elapsed = self.mw.col.timeboxReached()
    if elapsed:
        maProc(self, elapsed)
        self.mw.col.startTimebox()

Reviewer.nextCard = wrap(Reviewer.nextCard, maNextCard, 'before')

if True:
    info_action = QAction(mw)
    info_action.setText("&" + _("Timebox time limit"))
    info_action.setShortcut(HOTKEY['timebox'])
    info_action.setEnabled(False)

    try:
        mw.addon_view_menu
    except AttributeError:
        mw.addon_view_menu = QMenu(MSG[lang]['View'], mw)
        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(), mw.addon_view_menu)

    mw.connect(info_action, SIGNAL("triggered()"),
               lambda: myInfoCards(mw.reviewer))

    mw.addon_view_menu.addAction(info_action)

    def info_off():
        info_action.setEnabled(False)

    def info_on():
        info_action.setEnabled(True)

    mw.deckBrowser.show = wrap(mw.deckBrowser.show, info_off)
    mw.overview.show = wrap(mw.overview.show, info_off)
    mw.reviewer.show = wrap(mw.reviewer.show, info_on)
