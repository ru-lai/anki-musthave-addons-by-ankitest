# -*- mode: Python ; coding: utf-8 -*-
# • Again Hard Good Easy wide big buttons
# https://ankiweb.net/shared/info/1508882486
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# Show answer and Again Hard Good Easy buttons
#  so wide as Anki window.
# Good button always takes place of Hard and Easy buttons,
#  if they are absent on the card.
# 4 wide color buttons only with smiles
#  instead of words and a bigger font on them.
#
# Hotkey 1 means AGAIN in any case.
# Hotkey 2 means HARD when available otherwise it mean GOOD.
# Hotkey 3 means GOOD anyway.
# Hotkey 4 means maximum available easiness anyhow
#  (it is Good for 2 buttons and Easy for 3 or 4 buttons).
#
# 2016-05-07 added button 'Later Not now'
#
# No support. Use it AS IS on your own risk.
from __future__ import division
from __future__ import unicode_literals
import json
import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from anki.hooks import wrap  # , addHook, runHook
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import showText, showCritical

# Get language class
import anki.lang
lang = anki.lang.getLang()

# It is a part of '• Must Have' addon's functionality:
#  --musthave.py
#   https://ankiweb.net/shared/info/67643234

# based on
#  _Again_Hard.py
#   https://ankiweb.net/shared/info/1996229983
#  _Later_not_now_button.py
#   https://ankiweb.net/shared/info/777151722

# inspired by
#  Answer_Key_Remap.py
#   https://ankiweb.net/shared/info/1446503737
#  Bigger Show Answer Button
#   https://ankiweb.net/shared/info/1867966335
#  Button Colours (Good, Again)
#   https://ankiweb.net/shared/info/2494384865
#  Bigger Show All Answer Buttons
#   https://ankiweb.net/shared/info/2034935033
#  More_Answer_Buttons_for_New_Cards.py
#   https://ankiweb.net/shared/info/468253198 invalid id
#   https://ankiweb.net/shared/info/153603893

remap = {2:  [None, 1, 2, 2, 2],    # nil     Again   Good    Good    Good
         3:  [None, 1, 2, 2, 3],    # nil     Again   Good    Good    Easy
         4:  [None, 1, 2, 3, 4]}    # nil     Again   Hard    Good    Easy

# -- width of Show Answer button, triple, double and single answers buttons
BEAMS4 = '99%'
BEAMS3 = '74%'
BEAMS2 = '48%'
BEAMS1 = '24%'

black = '#999'
orange = '#c90'
red = '#c33'
green = '#3c3'
blue = '#69f'

BUTTON_LABEL = ['<span style="color:' + red + ';">o_0</span>',
                '<b style="color:' + orange + ';">:-(</b>',
                '<b style="color:' + green + ';">:-|</b>',
                '<b style="color:' + blue + ';">:-)</b>']

##

old_addons = (
    'Answer_Key_Remap.py',
    'Bigger_Show_Answer_Button.py',
    'Button_Colours_Good_Again.py',
    'Bigger_Show_All_Answer_Buttons.py',
    'More_Answer_Buttons_for_New_Cards.py',
    '_Again_Hard.py',
    '_Later_not_now_button.py',
)

old_addons2delete = ''
for old_addon in old_addons:
    if len(old_addon) > 0:
        old_filename = os.path.join(mw.pm.addonFolder(), old_addon)
        if os.path.exists(old_filename):
            old_addons2delete += old_addon[:-3] + ' \n'

if old_addons2delete != '':
    if lang == 'ru':
        showText(
            'В каталоге\n\n ' + mw.pm.addonFolder() +
            '\n\nнайдены дополнения, которые уже включены в дополнение\n' +
            ' • Again Hard Good Easy wide big buttons \n' +
            'и поэтому будут конфликтовать с ним.\n\n' +
            old_addons2delete +
            '\nУдалите эти дополнения и перезапустите Anki.')
    else:
        showText(
            '<big>There are some add-ons in the folder <br>\n<br>\n' +
            ' &nbsp; ' + mw.pm.addonFolder() +
            '<pre>' + old_addons2delete + '</pre>' +
            'They are already part of<br>\n' +
            ' <b> &nbsp; • Again Hard Good Easy wide big buttons</b>' +
            ' addon.<br>\n' +
            'Please, delete them and restart Anki.</big>', type="html")

"""
# Bigger Show Answer Button
For people who do their reps with a mouse.
Makes the show answer button wide enough to cover all 4 of the review buttons.
"""


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


def laterNotNow():
    return (
        '<style>td{vertical-align:bottom;}' +
        'td button{font-size:x-large;color:#999;}</style>' +
        '<table cellpadding=0 cellspacing=0 width=100%%><tr>' +
        '<td align=center><span class=stattxt>%s</span>' +
        '''<button title=" %s " onclick="py.link('ease%d');" ''' +
        'style="width:100%%;%s">%s</button></td><td>&nbsp;</td>') % (
            'позже' if lang == 'ru' else _('later'), 
            _("Shortcut key: %s")%(_('Escape')), NOT_NOW_BASE,
            'color:' + black + ';', ('&nbsp;не&nbsp;сейчас&nbsp;' 
            if lang == 'ru' else _('&nbsp;not&nbsp;now&nbsp;')))


def myShowAnswerButton(self, _old):
    if newRemaining(self):
        self.mw.moveToState('overview')
    self._bottomReady = True
    if not self.typeCorrect:
        self.bottom.web.setFocus()

    middle = laterNotNow() + (
        '<td align=center style="width:%s;">' +
        '<span class=stattxt>%s</span><button %s id=ansbut ' +
        '''style="width:100%%;%s" onclick="py.link('ans');" ''' +
        '>%s</button></td>' +
        '</tr></table>') % (
            BEAMS4, self._remaining(),
            ' title=" ' + (_('Shortcut key: %s') % _('Space')) + ' " ',
            ' color:' + black +';', _('Show Answer'))

    # place it in a table so it has the same top margin as the ease buttons
    # middle = '<!div align=center style='width:%s!important;'>%s</div>' %
    # (BEAMS4, middle)
    if self.card.shouldShowTimer():
        maxTime = self.card.timeLimit() / 1000
    else:
        maxTime = 0
    self.bottom.web.eval('showQuestion(%s,%d);' % (
        json.dumps(middle), maxTime))
    return True

if old_addons2delete == '':
    Reviewer._showAnswerButton = wrap(
        Reviewer._showAnswerButton, myShowAnswerButton, 'around')

# Anki uses a single digit to track which button has been clicked.
NOT_NOW_BASE = 5


def AKR_answerCard(self, ease, _old):
    count = mw.col.sched.answerButtons(mw.reviewer.card)  # Get button count
    try:
        ease = remap[count][ease]
    except (KeyError, IndexError):
        pass
    _old(self, ease)

if old_addons2delete == '':
    Reviewer._answerCard = wrap(Reviewer._answerCard, AKR_answerCard, 'around')
# 'before' does not working as intended cause ease is changing inside AKR

# Replace _answerButtonList method


def answerButtonList(self):
    l = ((1, '' + BUTTON_LABEL[0] + '', BEAMS1),)
    cnt = self.mw.col.sched.answerButtons(self.card)
    if cnt == 2:
        return l + ((2, '' + BUTTON_LABEL[2] + '', BEAMS3),)
        # the comma at the end is mandatory, a subtle bug occurs without it
    elif cnt == 3:
        return l + ((2, '' + BUTTON_LABEL[2] + '', BEAMS2),
                    (3, '' + BUTTON_LABEL[3] + '', BEAMS1))
    else:
        return l + ((2, '' + BUTTON_LABEL[1] + '', BEAMS1),
                    (3, '' + BUTTON_LABEL[2] + '', BEAMS1),
                    (4, '' + BUTTON_LABEL[3] + '', BEAMS1))
# all buttons are with coloured text
# and have an equal width with buttons in Night Mode


def myAnswerButtons(self, _old):
    times = []
    default = self._defaultEase()

    cnt = self.mw.col.sched.answerButtons(self.card)

    def but(i, label, beam):
        if i == default:
            extra = 'id=defease'
        else:
            extra = ''
        due = self._buttonTime(i)
        return (
            '<td align=center style="width:%s;">' +
            '<span class=stattxt>%s</span><button %s %s ' +
            '''style="width:100%%;%s" onclick="py.link('ease%d');"''' +
            '>%s</button></td>') % (
                beam, due, extra, (
                    (' title=" ' + _('Shortcut key: %s') % 
                    # (remap[cnt][i])) + ' "'),
                    (i)) + ' "'),
                'color:' + black, i, label)

    buf = laterNotNow()

    for ease, lbl, beams in answerButtonList(self):
        buf += but(ease, lbl, beams)

    return (
        buf + "</tr></table>" +
        "<script>$(function(){$('#defease').focus();});</script>")


def answer_card_intercepting(self, actual_ease, _old):
    ease = actual_ease
    if actual_ease >= NOT_NOW_BASE:
        self.nextCard()
        return True
    else:
        return _old(self, ease)

if old_addons2delete == '':
    Reviewer._answerButtons = wrap(
        Reviewer._answerButtons, myAnswerButtons, 'around')

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
