# -*- coding: utf-8 -*-
# by Anki user ankitest
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# • day learning cards always before new
# https://ankiweb.net/shared/info/1331545236

# Now it is the part of Must Have add-on:
# https://ankiweb.net/shared/info/67643234

# This is a simple monkey patch add-on that inserts day learning cards
# (learning cards with intervals that crossed the day turnover)
# always before new cards without depending due reviews.

# By default Anki do so:
#  learning; new if before; due; day learning; new if after
# With this add-on card will be displayed in the following order:
#  learning; (day learning; new) if before; due; (day learning; new) if after

# Normally these cards go after due, but I want them to go before new.

# If Tools -> Preferences... -> Basic -> Show new cards before reviews
#    learning; day learning; new; due
# If Tools -> Preferences... -> Basic -> Show new cards after reviews
#    learning; due; day learning; new

# inspired by Anki user rjgoif
# https://ankiweb.net/shared/info/1810271825
# put ALL due "learning" cards first ×
# ####################################################################
# That is a simple add-on that inserts the daily-learning cards, i.e.
# cards in the learning queue with intervals that crossed the day turnover,
# before starting other reviews (new cards, review cards). \
# Normally these cards go last, but I want them to go first.
# ####################################################################

import anki.sched


def _getCardReordered(self):
    'Return the next due card id, or None.'

    # learning card due?
    c = self._getLrnCard()
    if c:
        return c

    # new first, or time for one?
    if self._timeForNewCard():

        # day learning card due?
        c = self._getLrnDayCard()
        if c:
            return c

        c = self._getNewCard()
        if c:
            return c

    # card due for review?
    c = self._getRevCard()
    if c:
        return c

    # day learning card due?
    c = self._getLrnDayCard()
    if c:
        return c

    # new cards left?
    c = self._getNewCard()
    if c:
        return c

    # collapse or finish
    return self._getLrnCard(collapse=True)

anki.sched.Scheduler._getCard = _getCardReordered
