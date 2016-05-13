# -*- coding: utf-8 -*-
# ~ More Answer Buttons for ALL Cards
# https://ankiweb.net/shared/info/755044381
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
# 
"""
Adds extra buttons to the Reviewer window for new cards
https://ankiweb.net/shared/info/468253198

Copyright: Steve AW <steveawa@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

Modified by Glutanimate, 2016

WARNING: this addon uses private methods to achieve its goals. Use at your
    own risk and keep backups.

What it does: Adds anywhere between 1 to 4 new buttons to the review window
    when reviewing a new card. The new buttons function like the existing "Easy"
    button, but in addition, they reschedule the card to different interval, which
    is randomly assigned between a lower and upper limit that is preset
    by the user (see below).

By default 3 buttons are added, with intervals: "3-4d" , "5-7d" , "8-15d"
    This can be changed below.

I wanted this addon because many of my new cards do not need to be
    "Learned" as I created and added them myself, typically an hour or so before
    my first review session. I often add around 100-200 new cards per day, all on
    a related topic, and this addon allows me to spread the next review of the new
    cards that don't need learning out in time.

How it works: This addon works by intercepting the creation of the reviewer buttons
  and adds up to 4 extra buttons to the review window. The answer function
  is wrapped and the ease parameter is checked to see if it one of the new
  buttons. If it is, the standard answer function is used to add the card
  as an easy card, and then the browser 'reschedCards' function is used
  to reschedule it to the desired interval.

In summary, this functions as if you click the "Easy" button on a new card,
  and then go to the browser and reschedule the card.

Warning: This completely replaces the Reviewer._answerButtons fn, so any changes
   to that function in future updates will be lost. Could ask for a hook?
Warning: buyer beware ... The author is not a python, nor a qt programmer

Support: None. Use at your own risk. If you do find a problem please email me
    at steveawa@gmail.com

Setup data
List of dicts, where each item of the list (a dict) is the data for a new button.
This can be edited to suit, but there can not be more than 4 buttons.
    Description ... appears above the button
    Label ... the label of the button
    ShortCut ... the shortcut key for the button
    ReschedMin ... same as the lower number in the Browser's "Edit/Rescedule" command
    ReschedMax ... same as the higher number in the Browser's "Edit/Rescedule" command
"""
from __future__ import division
from __future__ import unicode_literals
import os, sys, datetime
import json

#Anki uses a single digit to track which button has been clicked.
NOT_NOW_BASE = 5

# We will use shortcut number from the first extra button
#  and above to track the extra buttons.
INTERCEPT_EASE_BASE = 6

extra_buttons = [ # should start from 6 anyway
    {"Description": "5-7d", "Label": "!!!", "ShortCut": "6", "ReschedMin": 5, "ReschedMax": 7},
    {"Description": "8-15d", "Label": "Veni", "ShortCut": "7", "ReschedMin": 8, "ReschedMax": 15},
    {"Description": "3-4w", "Label": "Vidi", "ShortCut": "8", "ReschedMin": 15, "ReschedMax": 30},
    {"Description": "2-3mo", "Label": "Vici", "ShortCut": "9", "ReschedMin": 31, "ReschedMax": 90},
    ]

#Must be four or less
assert len(extra_buttons) <= 4

SWAP_TAG = False
#SWAP_TAG = datetime.datetime.now().strftime("rescheduled::re-%Y-%m-%d::re-card")
#SWAP_TAG = datetime.datetime.now().strftime("re-%y-%m-%d-c")

from aqt.reviewer import Reviewer
from anki.hooks import wrap
from aqt.utils import tooltip
from aqt import mw

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Get language class
import anki.lang
lang = anki.lang.getLang()

USE_INTERVALS_AS_LABELS = False # True # 

def _bottomTime(self, i):
        if not self.mw.col.conf['estTimes']:
            return "&nbsp;"
        txt = self.mw.col.sched.nextIvlStr(self.card, i, True) or "&nbsp;"
        return txt
        
#todo: brittle. Replaces existing function

def _answerButtons(self):
    times = []
    default = self._defaultEase()

    def but(i, label):
        if i == default:
            extra = "id=defease"
        else:
            extra = ""
        if USE_INTERVALS_AS_LABELS:
            due = _bottomTime(self,i)
            return '''
<td align=center><span class=nobold>&nbsp;</span><br><button %s title="%s" onclick='py.link("ease%d");'>\
%s</button></td>''' % (extra, _("Shortcut key: %s") % i, i, due)
        else:
            due = self._buttonTime(i)
            return '''
<td align=center>%s<button %s title="%s" onclick='py.link("ease%d");'>\
%s</button></td>''' % (due, extra, _("Shortcut key: %s") % i, i, label)

    buf = "<center><table cellpading=0 cellspacing=0><tr>"
    if USE_INTERVALS_AS_LABELS:
        buf += '''
<td align=center><span class=nobold>&nbsp;</span><br><button title="Short key: %s" onclick='py.link("ease%d");'>\
%s</button></td><td>&nbsp;</td>''' % ("Escape", NOT_NOW_BASE, "позже" if lang=='ru' else _("later"))
    else:
        buf += '''
<td align=center><span class=nobold>%s</span><br><button title="Short key: %s" onclick='py.link("ease%d");'>\
%s</button></td><td>&nbsp;</td>''' % ("позже" if lang=='ru' else _("later"), "Escape", NOT_NOW_BASE, "не сейчас" if lang=='ru' else _("not now"))

    for ease, label in self._answerButtonList():
        buf += but(ease, label)
        #swAdded start ====>
    #Only for cards in the new queue
    if self.card.type in (0, 1, 2, 3): # New, Learn, Day learning
        #Check that the number of answer buttons is as expected.
        #assert self.mw.col.sched.answerButtons(self.card) == 3
        #python lists are 0 based
        for i, buttonItem in enumerate(extra_buttons):
            if USE_INTERVALS_AS_LABELS:
                buf += '''
<td align=center><span class=nobold>&nbsp;</span><br><button title="%s" onclick='py.link("ease%d");'>\
%s</button></td>''' % (_("Shortcut key: %s")%buttonItem["ShortCut"], \
                    i + INTERCEPT_EASE_BASE, buttonItem["Description"])
            else:
                buf += '''
<td align=center><span class=nobold>%s</span><br><button title="%s" onclick='py.link("ease%d");'>\
%s</button></td>''' % (buttonItem["Description"], _("Shortcut key: %s")%buttonItem["ShortCut"], \
                    i + INTERCEPT_EASE_BASE, buttonItem["Label"])
            #swAdded end
    buf += "</tr></table>"
    script = """<script>$(function () { $("#defease").focus(); });</script>"""
    return buf + script

#This wraps existing Reviewer._answerCard function.    
def answer_card_intercepting(self, actual_ease, _old):
  ease = actual_ease
  if actual_ease == NOT_NOW_BASE:
        self.nextCard()
        return True
  else:
    ease = actual_ease
    was_new_card = self.card.type in (0, 1, 2, 3)
    is_extra_button = was_new_card and actual_ease >= INTERCEPT_EASE_BASE
    if is_extra_button:
        #Make sure this is as expected.
        #assert self.mw.col.sched.answerButtons(self.card) == 3
        #So this is one of our buttons. First answer the card as if "Easy" clicked.
        ease = 3
        #We will need this to reschedule it.
        prev_card_id = self.card.id
        #
        buttonItem = extra_buttons[actual_ease - INTERCEPT_EASE_BASE]
        #Do the reschedule.
        self.mw.checkpoint(_("Reschedule card"))
        self.mw.col.sched.reschedCards([prev_card_id], buttonItem["ReschedMin"], buttonItem["ReschedMax"])
        tooltip("<center>Rescheduled:" + "<br>" + buttonItem["Description"] + "</center>")

        SwapTag = SWAP_TAG
        if SwapTag:
          SwapTag += unicode(self.mw.reviewer.card.ord+1)
          note = self.mw.reviewer.card.note()
          if not note.hasTag(SwapTag):
            note.addTag(SwapTag)
            note.flush()  # never forget to flush

        self.mw.reset()
        return True 
    else:
        ret = _old(self, ease)
        return ret

#Handle the shortcut. Used changekeys.py addon as a guide     
def keyHandler(self, evt, _old):
    key = unicode(evt.text())
    if self.state == "answer":
        for i, buttonItem in enumerate(extra_buttons):
            if key == buttonItem["ShortCut"]:
                #early exit ok in python?
                return self._answerCard(i + INTERCEPT_EASE_BASE)
    return _old(self, evt)

def more_proc():
    global USE_INTERVALS_AS_LABELS
    if more_action.isChecked():
        USE_INTERVALS_AS_LABELS = True
    else:
        USE_INTERVALS_AS_LABELS = False
    rst = mw.reviewer.state == 'answer'
    mw.reset()
    if rst:
        mw.reviewer._showAnswerHack()

try:
    mw.addon_view_menu
except AttributeError:
    mw.addon_view_menu = QMenu(_("&Вид") if lang == 'ru' else _("&View"), mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_view_menu)

more_action = QAction('&Кнопки оценок - без меток' if lang == 'ru' else _('&Answer buttons without labels'), mw)
more_action.setShortcut(QKeySequence("Ctrl+Alt+Shift+L"))
more_action.setCheckable(True)
more_action.setChecked(USE_INTERVALS_AS_LABELS)
mw.connect(more_action, SIGNAL("triggered()"), more_proc)
mw.addon_view_menu.addAction(more_action)

Reviewer._keyHandler = wrap(Reviewer._keyHandler, keyHandler, "around")
Reviewer._answerButtons = _answerButtons
Reviewer._answerCard = wrap(Reviewer._answerCard, answer_card_intercepting, "around")

#

def onEscape():
    mw.reviewer.nextCard()

try:
    mw.addon_cards_menu
except AttributeError:
    mw.addon_cards_menu = QMenu(_(u"&Карточки") if lang == 'ru' else _(u"&Cards"), mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_cards_menu)

escape_action = QAction(mw)
escape_action.setText(u'Позж&е, не сейчас' if lang=='ru' else _(u"&Later, not now"))
escape_action.setShortcut(QKeySequence('Escape'))
escape_action.setEnabled(False)
mw.connect(escape_action, SIGNAL("triggered()"), onEscape)

#mw.addon_cards_menu.addSeparator()
mw.addon_cards_menu.addAction(escape_action)
#mw.addon_cards_menu.addSeparator()

mw.deckBrowser.show = wrap(mw.deckBrowser.show, lambda: escape_action.setEnabled(False))
mw.overview.show = wrap(mw.overview.show, lambda: escape_action.setEnabled(False))
mw.reviewer.show = wrap(mw.reviewer.show, lambda: escape_action.setEnabled(True))

#

def newRemaining(self):
    if not self.mw.col.conf['dueCounts']:
        return 0
    idx = self.mw.col.sched.countIdx(self.card)
    if self.hadCardQueue:
        # if it's come from the undo queue, don't count it separately
        counts = list(self.mw.col.sched.counts())
    else:
        counts = list(self.mw.col.sched.counts(self.card))
    return (idx==0 and counts[0] < 1)

def myShowAnswerButton(self,_old):
    if newRemaining(self):
        self.mw.moveToState("overview")
    self._bottomReady = True
    if not self.typeCorrect:
        self.bottom.web.setFocus()

    buf = '''
<td align=center class=stat2><span class=stattxt>%s</span><br><button title="Short key: %s" onclick='py.link("ease%d");'>\
%s</button></td><td>&nbsp;</td>''' % ("позже" if lang=='ru' else _("later"), "Escape", NOT_NOW_BASE, "не сейчас" if lang=='ru' else _("not now"))

    middle = '''<table cellpadding=0><tr>%s<td class=stat2 align=center>
<span class=stattxt>%s</span><br>
<button %s id=ansbut style="display:inline-block;width:%s;%s" onclick='py.link(\"ans\");'>%s</button>
    </td></tr></table>
''' % ( buf, self._remaining(), \
        " title=' "+(_("Shortcut key: %s") % _("Space"))+" '",
        "99%", "", _("Show Answer"))
    
    if self.card.shouldShowTimer():
        maxTime = self.card.timeLimit() / 1000
    else:
        maxTime = 0
    self.bottom.web.eval("showQuestion(%s,%d);" % (
        json.dumps(middle), maxTime))
    return True

Reviewer._showAnswerButton = wrap(Reviewer._showAnswerButton, myShowAnswerButton, "around")
