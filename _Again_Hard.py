# -*- mode: Python ; coding: utf-8 -*-
# • Again Hard (Yes No) 2 buttons only
# https://ankiweb.net/shared/info/1996229983
#
# 2 wide buttons only with smiles instead of words and a bigger font on them.
# It means NO YES in any case.
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
from __future__ import division
from __future__ import unicode_literals

# inspired by
#  Answer_Key_Remap.py 
#   https://ankiweb.net/shared/info/1446503737
#  Bigger Show Answer Button
#   https://ankiweb.net/shared/info/1867966335
#  Button Colours (Good, Again)
#   https://ankiweb.net/shared/info/2494384865
#  Bigger Show All Answer Buttons
#   https://ankiweb.net/shared/info/2034935033

from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap #, addHook, runHook
import json

remap = { 2:  [None, 1, 2, 2, 2],    # nil     Again   Again   Good    Good
          3:  [None, 1, 2, 2, 2],    # nil     Again   Again   Good    Easy
          4:  [None, 1, 2, 2, 2]}    # nil     Again   Hard    Good    Easy
      
# -- width of Show Answer button, triple, double and single answers buttons in pixels
BEAMS4 = '99%'
BEAMS3 = '74%'
BEAMS2 = '48%'
BEAMS1 = '24%'

black = '#000'
red = '#c33'
green = '#3c3'

BUTTON_LABEL = ['<b style="color:'+red+';">:-(</b>', '<b style="color:'+green+';">:-)</b>']

# Replace _answerButtonList method
def answerButtonList(self):
    l = ((1, '<style>button span{font-size:x-large;}' + \
    ' button small { color:#999;font-weight:400;padding-left:.35em;font-size: small; } ' + \
    '</style><span>' + BUTTON_LABEL[0] + '</span>', BEAMS2),)
    #cnt = self.mw.col.sched.answerButtons(self.card)
    return l + ((2, '<span>' + BUTTON_LABEL[1] + '</span>', BEAMS2),)
    # the comma at the end is mandatory, a subtle bug occurs without it

def AKR_answerCard(self, ease):
    count = mw.col.sched.answerButtons(mw.reviewer.card) # Get button count
    try:
        ease = remap[count][ease]
    except (KeyError, IndexError):
        pass
    __oldFunc(self, ease)

__oldFunc = Reviewer._answerCard
Reviewer._answerCard = AKR_answerCard

#Reviewer._answerCard = wrap(Reviewer._answerCard, AKR_answerCard, 'before')

def myAnswerButtons(self,_old):
    times = []
    default = self._defaultEase()
    def but(i, label, beam):
        if i == default:
            extra = 'id=defease'
        else:
            extra = ''
        due = self._buttonTime(i)
        return '''
<td align=center style="width:%s;">%s<button %s %s onclick='py.link("ease%d");'>\
%s</button></td>''' % (beam, due, extra, \
        ((' title=" '+_('Shortcut key: %s') % i)+' "'), i, label)
    buf = '<table cellpading=0 cellspacing=0 width=100%%><tr>'
    for ease, lbl, beams in answerButtonList(self):
        buf += but(ease, lbl, beams)
    buf += '</tr></table>'
    script = """
    <style>table tr td button { width: 100%; } </style>
<script>$(function () { $('#defease').focus(); });</script>"""
    return buf + script

"""
# Bigger Show Answer Button
For people who do their reps with a mouse. 
Makes the show answer button wide enough to cover all 4 of the review buttons. 
"""

def myShowAnswerButton(self,_old):
    self._bottomReady = True
    if not self.typeCorrect:
        self.bottom.web.setFocus()
    middle = '''
<span class=stattxt>%s</span><br>
<button %s id=ansbut style="display:inline-block;width:%s;%s" onclick="py.link('ans');">%s</button>
    </script>
''' % (
    self._remaining(), \
        ((' title=" '+_('Shortcut key: %s') % _('Space'))+' "'),
        BEAMS4, 'font-size:x-large;color:'+black, _('Show Answer'))
    # place it in a table so it has the same top margin as the ease buttons
    middle = '<div class=stat2 align=center style="width:%s!important;">%s</div>' % (BEAMS4, middle)
    if self.card.shouldShowTimer():
        maxTime = self.card.timeLimit() / 1000
    else:
        maxTime = 0
    self.bottom.web.eval('showQuestion(%s,%d);' % (
        json.dumps(middle), maxTime))
    return True

Reviewer._answerButtons = wrap(Reviewer._answerButtons, myAnswerButtons, 'around')
Reviewer._showAnswerButton = wrap(Reviewer._showAnswerButton, myShowAnswerButton, 'around')


