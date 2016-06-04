# -*- coding: utf-8 -*-
# • Timebox tooltip
# https://ankiweb.net/shared/info/2014169675
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# It puts the stats when you finish a timebox in a tooltip message
#  that goes away after a few seconds. 
#
# No support. Use it AS IS on your own risk.
"""
    def timeboxReached(self):
        "Return (elapsedTime, reps) if timebox reached, or False."
        if not self.conf['timeLim']:
            # timeboxing disabled
            return False
        elapsed = time.time() - self._startTime
        if elapsed > self.conf['timeLim']:
            return (self.conf['timeLim'], self.sched.reps - self._startReps)
"""

from anki.hooks import wrap
from anki.sound import playFromText, clearAudioQueue, play
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import tooltip

# anki/collection.py
# aqt/reviewer.py Monkey Patch


def maNextCard(self, _old):
    elapsed = self.mw.col.timeboxReached()
    if elapsed:
        part1 = ngettext('%d card studied in',
                         '%d cards studied in', elapsed[1]) % elapsed[1]
        mins = int(round(elapsed[0] / 60))
        part2 = ngettext('%s minute.', '%s minutes.', mins) % mins
        tooltip('%s %s' % (part1, part2))
        self.mw.col.startTimebox()
    if self.cardQueue:
        # undone/edited cards to show
        c = self.cardQueue.pop()
        c.startTimer()
        self.hadCardQueue = True
    else:
        if self.hadCardQueue:
            # the undone/edited cards may be sitting in the regular queue;
            # need to reset
            self.mw.col.reset()
            self.hadCardQueue = False
        c = self.mw.col.sched.getCard()
    self.card = c
    clearAudioQueue()
    if not c:
        self.mw.moveToState('overview')
        return
    if self._reps is None or self._reps % 100 == 0:
        # we recycle the webview periodically so webkit can free memory
        self._initWeb()
    else:
        self._showQuestion()

Reviewer.nextCard = wrap(Reviewer.nextCard, maNextCard, 'around')
