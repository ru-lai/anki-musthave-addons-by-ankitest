# -*- coding: utf-8 -*-
# ' Timebox tooltip
# https://ankiweb.net/shared/info/2014169675
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# It puts the stats when you finish a timebox in a tooltip message
#  that goes away after a few seconds. 
#
# No support. Use it AS IS on your own risk.
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

# Get DeckBrowser class
from aqt.deckbrowser import DeckBrowser

from anki.lang import ngettext
from anki.hooks import wrap

# Get fmtTimeSpan required for renderStats method
from anki.utils import fmtTimeSpan

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


def maNextCard(self):
    elapsed = self.mw.col.timeboxReached()
    if elapsed:
        part1 = ngettext('%d card studied in',
                         '%d cards studied in', elapsed[1]) % elapsed[1]
        mins = int(round(elapsed[0] / 60))
        part2 = ngettext('%s minute.', '%s minutes.', mins) % mins
        tooltip('<big>%s %s <br><br> %s</big>' % (
            part1, part2, 
            renderOstrich(self)), period=8000)
        self.mw.col.startTimebox()

Reviewer.nextCard = wrap(Reviewer.nextCard, maNextCard, 'before')
