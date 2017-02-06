# -*- mode: Python ; coding: utf-8 -*-
# rated:30:1 
# https://anki.tenderapp.com/discussions/add-ons/9032-rated301
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2017 Dmitry Mikheev, http://finpapa.ucoz.ru/index.html
# NO support. Use it AS IS on your own risk.

# RADIO_FORGOT: 30 -> 36500

# aqt/customstudy.py

# Copyright: Damien Elmes <anki@ichi2.net>
# -*- coding: utf-8 -*-
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from aqt.qt import *
import aqt.customstudy
import anki.find
from anki.consts import *

RATED301 = 36500

RADIO_NEW = 1
RADIO_REV = 2
RADIO_FORGOT = 3
RADIO_AHEAD = 4
RADIO_PREVIEW = 5
RADIO_CRAM = 6

TYPE_NEW = 0
TYPE_DUE = 1
TYPE_ALL = 2

def _onRadioChange(self, idx):
    f = self.form; sp = f.spin
    smin = 1; smax = DYN_MAX_SIZE; sval = 1
    post = _("cards")
    tit = ""
    spShow = True
    typeShow = False
    ok = _("OK")
    def plus(num):
        if num == 1000:
            num = "1000+"
        return "<b>"+str(num)+"</b>"
    if idx == RADIO_NEW:
        new = self.mw.col.sched.totalNewForCurrentDeck()
        self.deck['newToday']
        tit = _("New cards in deck: %s") % plus(new)
        pre = _("Increase today's new card limit by")
        sval = min(new, self.deck.get('extendNew', 10))
        smax = new
    elif idx == RADIO_REV:
        rev = self.mw.col.sched.totalRevForCurrentDeck()
        tit = _("Reviews due in deck: %s") % plus(rev)
        pre = _("Increase today's review limit by")
        sval = min(rev, self.deck.get('extendRev', 10))
    elif idx == RADIO_FORGOT:
        pre = _("Review cards forgotten in last")
        post = _("days")
        smax = RATED301
    elif idx == RADIO_AHEAD:
        pre = _("Review ahead by")
        post = _("days")
    elif idx == RADIO_PREVIEW:
        pre = _("Preview new cards added in the last")
        post = _("days")
        sval = 1
    elif idx == RADIO_CRAM:
        pre = _("Select")
        post = _("cards from the deck")
        #tit = _("After pressing OK, you can choose which tags to include.")
        ok = _("Choose Tags")
        sval = 100
        typeShow = True
    sp.setVisible(spShow)
    f.cardType.setVisible(typeShow)
    f.title.setText(tit)
    f.title.setVisible(not not tit)
    f.spin.setMinimum(smin)
    f.spin.setMaximum(smax)
    f.spin.setValue(sval)
    f.preSpin.setText(pre)
    f.postSpin.setText(post)
    f.buttonBox.button(QDialogButtonBox.Ok).setText(ok)
    self.radioIdx = idx

aqt.customstudy.CustomStudy.onRadioChange = _onRadioChange

def _findRated(self, (val, args)):
    # days(:optional_ease)
    r = val.split(":")
    try:
        days = int(r[0])
    except ValueError:
        return
    days = min(days, RATED301)
    # ease
    ease = ""
    if len(r) > 1:
        if r[1] not in ("1", "2", "3", "4"):
            return
        ease = "and ease=%s" % r[1]
    cutoff = (self.col.sched.dayCutoff - 86400*days)*1000
    return ("c.id in (select cid from revlog where id>%d %s)" %
            (cutoff, ease))

anki.find.Finder._findRated = _findRated
