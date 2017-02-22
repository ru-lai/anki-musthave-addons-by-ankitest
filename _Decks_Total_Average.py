# -*- mode: Python ; coding: utf-8 -*-
# ' Decks Total Average
# https://ankiweb.net/shared/info/1040866511
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
from __future__ import division

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

# Replace _renderStats method
def renderStats(self, _old):

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
    
    buf = "<div style='display:table;padding-top:1.5em;'>" \
        + "<div style='display:table-cell;'> " \
        + _old(self) + "<hr>" \
        + _("New Cards") \
        + ": &nbsp; <font color=#00a> %(d)s</font>" % dict(d=new) \
        + " &nbsp; " + _("Learn") \
        + ": &nbsp; <font color=#a00>%(c)s</font>" % dict(c=lrn) \
        + " &nbsp; <span style='white-space:nowrap;'>" + _("To Review") \
        + ": &nbsp; <font color=#0a0>%(c)s</font>" % dict(c=due) \
        + "</span>" \
        + " &nbsp; <br><span style='white-space:nowrap;'>" + _("Due") \
        + ": &nbsp; <b style=color:#aaa>%(c)s</b> " % dict(c=(lrn+due)) \
        + "</span> " \
        + " &nbsp; <span style='white-space:nowrap;'>" + _("Total") \
        + ": &nbsp; <b style=color:#888>%(c)s</b>" % dict(c=(total)) \
        + "</span></div>" \
        + "<div style='display:table-cell;vertical-align:middle;" \
        + "padding-left:2em;'>" \
        + "<span style='white-space:nowrap;'>" + _("Average") \
        + ":<br> " + _("%.01f cards/minute") % (speed) + "</span><br><br>" \
        + _("More") + "&nbsp;" + ngettext(
             "%s minute.", "%s minutes.", minutes) % (minutes) \
        + "</div></div>"
    
    return buf

DeckBrowser._renderStats = wrap(DeckBrowser._renderStats, 
                                renderStats, 'around')
