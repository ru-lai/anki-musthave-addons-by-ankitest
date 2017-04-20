# -*- mode: Python ; coding: utf-8 -*-
# • Again Good HUGE buttons
# https://ankiweb.net/shared/info/2074653746
# https://github.com/ankitest/anki-musthave-addonz-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 Show 2 buttons: Again and (Hard or Good or Easy) buttons
  so wide as Anki window.
 Or usual 4 buttons: it's on user's choice.

 Good button always takes place of Hard and Easy buttons,
  if they are absent on the card.
 4 wide color buttons only with smiles
  instead of words and with a bigger font on them.

 -- In 2-buttons mode hotkeys are:
 Hotkey 1 means AGAIN in any case.
 Hotkeys 2,3,4 means the same:
   it is Hard, Good or Easy (on user's choice)
 -- In 3-4-buttons mode hotkeys are:
 Hotkey 1 means AGAIN in any case.
 Hotkey 2 means HARD when available otherwise it mean GOOD.
 Hotkey 3 means GOOD anyway.
 Hotkey 4 means maximum available easiness anyhow
  (it is Good for 2 buttons and Easy for 3 or 4 buttons).

 Adds 1-4 (4 by default) extra answer buttons with regular intervals.
  No answer on that card will be given, just setup additional interval.
 You can assign you own intervals, labels (by editing source).
  Hotkeys are 6, 7, 8, 9.
 You can use intervals as button labels
  View - Answer buttons without labels or Ctrl+Alt+Shift+L

 On Cards - Later, Not Now menu click (Escape hotkey):
  No answer will be given, next card will be shown.
  Card stays on its place in queue,
  you'll see it next time you study the deck
  or immediatly after reset of cards' queue.

 • Flip-flop card (Show FrontSide/BackSide
   by F7/F8 or Ctrl+PgUp/Control+PageDown or ^9/^3 or Insert/0)
"""
from __future__ import division
from __future__ import unicode_literals
import datetime
import random
import json
import sys
import os
import re

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import anki
import aqt

from aqt.clayout import CardLayout

# Get language class
# import anki.lang
lang = anki.lang.getLang()

extra_buttons = [  # should start from 6 anyway
    {'Description': '5-7d',
        'Label': '!!!',
        'ShortCut': '6',
        'ReschedMin': 5,
        'ReschedMax': 7},
    {'Description': '8-15d',
        'Label': 'Veni',
        'ShortCut': '7',
        'ReschedMin': 8,
        'ReschedMax': 15},
    {'Description': '3-4w',
        'Label': 'Vidi',
        'ShortCut': '8',
        'ReschedMin': 15,
        'ReschedMax': 30},
    {'Description': '2-3mo',
        'Label': 'Vici',
        'ShortCut': '9',
        'ReschedMin': 31,
        'ReschedMax': 90},
]

MSG = {
    'en': {
        'later': _('later'),
        'not now': _('not now'),
        'Cards': _('&Cards'),
        'View': _('&View'),
        'Sound': _('&Sound'),
        'Go': _('&Go'),
        'HardGoodEasy':
            _('Again')+', '+_('Hard')+', '+_('Good')+', '+_('Easy'),
        'Again': '&'+_('Again'),
        'AgainHard': _('Again')+', &'+_('Hard'),
        'AgainGood': _('Again')+', &'+_('Good'),
        'AgainEasy': _('Again')+', &'+_('Easy'),
        'Later, not now': _('&Later, not now'),
        'no_smiles': _('No smiles'),
        'no_styles': _('No big buttons'),
        'no_labels': _('Next Interva&L — on answer buttons'),
        'later_not_now': _('&nbsp;not&nbsp;now&nbsp;'),
        'no_extra_buttons': _('Hide &Extra buttons'),
        'Hide button: ': _('&Hide button: '),
        'Edit': _('Edit'),
        'More': _('More'),
        'Hide buttons': _('Hide buttons: '),
        'Edit': _('&Edit...'),
        'Edit Layout': _('Edi&t Layout...'),
        'Edit Fields': _('Edit &Fields...'),
        'flat_buttons': _('&Flat buttons'),
        'HUGE_buttons': _('&HUGE buttons options'),
        'aa': _('About addon  '),
        'showFrontSide': _('Show &FrontSide'),
        'showBackSide': _('Show &BackSide'),
        'viewFrontSide': _('&FrontSide'),
        'viewBackSide': _('&BackSide'),
        'cardFrontSide': _("Card's &FrontSide"),
        'cardBackSide': _("Card's &BackSide"),
        'gotoFrontSide': _('Goto &FrontSide'),
        'gotoBackSide': _('Goto &BackSide'),
        'goFrontSide': _('to &FrontSide'),
        'goBackSide': _('to &BackSide'),
        },
    'ru': {
        'later': 'позже',
        'not now': 'не сейчас',
        'Cards': '&Карточки',
        'View': '&Вид',
        'Sound': '&Звук',
        'Go': 'П&ереход',
        'HardGoodEasy':
            _('Again')+', '+_('Hard')+', '+_('Good')+', '+_('Easy'),
        'Again': '&'+_('Again'),
        'AgainHard': _('Again')+', &'+_('Hard'),
        'AgainGood': _('Again')+', &'+_('Good'),
        'AgainEasy': _('Again')+', &'+_('Easy'),
        'Later, not now': 'Поз&же, не сейчас',
        'no_smiles': '&Без смайликов',
        'no_styles': '&Обычная высота кнопок',
        'no_labels': 'На кнопках о&ценок - следующий интервал',
        'later_not_now': '&nbsp;не&nbsp;сейчас&nbsp;',
        'Hide button: ': 'Скрыть кнопку: ',
        'no_extra_buttons': 'Скрыть кнопки &интервалов',
        'Edit': 'Правка',
        'More': 'Ещё',
        'Hide buttons': 'Скрыть кнопки: ',
        'Edit': 'Ре&дактирование...',
        'Edit Layout': '&Шаблоны карточек...',
        'Edit Fields': '&Список полей...',
        'flat_buttons': '&Плоские кнопки',
        'HUGE_buttons': '&Настройка кнопок ответа',
        'aa': 'О дополнении  ',
        'showFrontSide': 'Показать &Лицевую Сторону',
        'showBackSide': 'Показать &Оборотную Сторону',
        'viewFrontSide': '&Лицевая Сторона',
        'viewBackSide': '&Оборотная Сторона',
        'cardFrontSide': '&Лицевая Сторона карточки',
        'cardBackSide': '&Оборотная Сторона карточки',
        'gotoFrontSide': 'Перейти на &Лицевую Сторону',
        'gotoBackSide': 'Перейти на &Оборотную Сторону',
        'goFrontSide': 'на &Лицевую Сторону',
        'goBackSide': 'на &Оборотную Сторону',
        }
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

# 'позже' if lang == 'ru' else _('later')
# 'не сейчас' if lang == 'ru' else _('not now')
# _(u'&Карточки') if lang == 'ru' else _(u'&Cards')
# u'Позж&е, не сейчас' if lang == 'ru' else _(u'&Later, not now')

# _('&Вид') if lang == 'ru' else _('&View')
# '&Кнопки оценок - без меток' if lang == 'ru'
#   else _('&Answer buttons without labels')
# '&nbsp;не&nbsp;сейчас&nbsp;'
#   if lang == 'ru' else _('&nbsp;not&nbsp;now&nbsp;')

HOTKEY = {
    'no_smiles': QKeySequence('Ctrl+Alt+Shift+O'),
    'no_styles': QKeySequence('Ctrl+Alt+Shift+B'),
    'no_labels': QKeySequence('Ctrl+Alt+Shift+L'),
    'later_not_now': 'Escape',
    'hide_later': QKeySequence('Ctrl+Alt+Shift+Esc'),
    'HideButtons': QKeySequence('Ctrl+Alt+Shift+M'),
    'no_extra_buttons': QKeySequence('Ctrl+Alt+Shift+N'),

    'All':  QKeySequence('Ctrl+Alt+Shift+0'),
    'Again': QKeySequence('Ctrl+Alt+Shift+1'),
    'Hard': QKeySequence('Ctrl+Alt+Shift+2'),
    'Good': QKeySequence('Ctrl+Alt+Shift+3'),
    'Easy': QKeySequence('Ctrl+Alt+Shift+4'),

    'Edit_HTML': 'F4',         # Ctrl+Shift+X
    'Edit_Fields': 'F4',         # e
    'Edit_Cards': 'Shift+F4',
    'Edit_Fieldz': 'Ctrl+F4',    # Alt+F4 == Close Window == ^F4 on Mac
    'flat_buttons': 'Ctrl+Alt+Shift+F',

    "next_cloze": 'Ctrl+Space',
    "same_cloze": 'Ctrl+Alt+Space',

    'same_without_Alt': 'F1',
    "next_closure": 'F2',  # 'Ctrl+Shift+C'
    "same_closure": 'Alt+F2',  # 'Ctrl+Alt+Shift+C' -- old style

    # Ctrl+F11 does not work
    "LaTeX": 'Alt+F11',  # "Ctrl+T, T"
    "LaTeX$": 'F11',       # "Ctrl+T, E"
    "LaTeX$$": 'Shift+F11',  # "Ctrl+T, M"

    'showFrontSide': Qt.Key_F7,
    'showBackSide': 'F8',
    'viewFrontSide': "Ctrl+PgUp",
    'viewBackSide': QKeySequence(Qt.CTRL + Qt.Key_PageDown),
    'cardFrontSide': QKeySequence('Ctrl+9'),
    'cardBackSide': Qt.CTRL + Qt.Key_3,  # 'Ctrl+3'
    'gotoFrontSide': "Ctrl+Up",
    'gotoBackSide': "Ctrl+Down",
    'goFrontSide': "Ctrl+8",
    'goBackSide': "Ctrl+2",
    }

# It is a part of '• Must Have' addon's functionality:
#  --musthave.py
#   https://ankiweb.net/shared/info/67643234

# based on
#  _Again_Hard.py
#   https://ankiweb.net/shared/info/1996229983
#   old name of this one
#  _Later_not_now_button.py
#   https://ankiweb.net/shared/info/777151722
#  ' Again Hard Good Easy wide big buttons
#   https://ankiweb.net/shared/info/1508882486
#  ' F4 Edit
#   https://ankiweb.net/shared/info/2085904433

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
#  Low Key Anki: Pass/Fail
#   https://ankiweb.net/shared/info/477405355

black = 'none'  # Night_Mode compatibility
orange = '#c90'  # darkgoldenrod
red = '#c33'  # #c33
green = '#3c3'  # #090
blue = '#69f'  # #66f

remap = 'All'
remaps = {'Again':
          {1:  [None, 1, 1, 1, 1],     # nil     Again   Again   Again   Again
           2:  [None, 1, 1, 1, 1],     # nil     Again   Again   Again   Again
           3:  [None, 1, 1, 1, 1],     # nil     Again   Again   Again   Again
           4:  [None, 1, 1, 1, 1]},    # nil     Again   Again   Again   Again
          'Hard':
          {1:  [None, 1, 1, 1, 1],     # nil     Again   Again   Again   Again
           2:  [None, 1, 2, 2, 2],     # nil     Again   Good    Good    Good
           3:  [None, 1, 2, 2, 2],     # nil     Again   Good    Good    Good
           4:  [None, 1, 2, 2, 2]},    # nil     Again   Hard    Hard    Hard
          'Good':
          {1:  [None, 1, 1, 1, 1],     # nil     Again   Again   Again   Again
           2:  [None, 1, 2, 2, 2],     # nil     Again   Good    Good    Good
           3:  [None, 1, 2, 2, 2],     # nil     Again   Good    Good    Good
           4:  [None, 1, 3, 3, 3]},    # nil     Again   Good    Good    Good
          'Easy':
          {1:  [None, 1, 1, 1, 1],     # nil     Again   Again   Again   Again
           2:  [None, 1, 2, 2, 2],     # nil     Again   Good    Good    Good
           3:  [None, 1, 3, 3, 3],     # nil     Again   Easy    Easy    Easy
           4:  [None, 1, 4, 4, 4]},    # nil     Again   Easy    Easy    Easy
          'All':
          {1:  [None, 1, 1, 1, 1],     # nil     Again   Again   Again   Again
           2:  [None, 1, 2, 2, 2],     # nil     Again   Good    Good    Good
           3:  [None, 1, 2, 2, 3],     # nil     Again   Good    Good    Easy
           4:  [None, 1, 2, 3, 4]}}    # nil     Again   Hard    Good    Easy

# -- width of Show Answer button, triple, double and single answers buttons
BEAMS4 = '99%'
BEAMS3 = '74%'
BEAMS2 = '48%'
BEAMS1 = '24%'

USE_INTERVALS_AS_LABELS = False  # True  #
EDIT_MORE_BUTTONS = True  # False  #
HIDE_LATER = False  # True  #
swAdded = True  # False  #
NO_SMILES = False  # True  #
NO_STYLES = False  # True  #

##

BUTTON_COLOR = {'Again': [black, red, red, red, red],
                'Hard': [black, red, orange, orange, orange],
                'Good': [black, red, green, green, green],
                'Easy': [black, red, blue, blue, blue],
                'All': [black, red, orange, green, blue]}

BTN_CLR = {'Again': red, 'Hard': orange, 'Good': green, 'Easy': blue}

BUTTON_LABEL = {'Again': '<span style="color:' + red + ';">o_0</span>',
                'Hard': '<b style="color:' + orange + ';">:-(</b>',
                'Good': '<b style="color:' + green + ';">:-|</b>',
                'Easy': '<b style="color:' + blue + ';">:-)</b>'}

BTN_LABL = {
    'en': {
            'Again': _('Again').upper(),
            'Hard': _('Hard').upper(),
            'Good': _('Good').upper(),
            'Easy': _('Easy').upper(),
        },
    'ru': {
            'Again': 'СНОВА',
            'Hard': 'ТРУДНО',
            'Good': 'ХОРОШО',
            'Easy': 'ЛЕГКО',
        }
    }

try:
    import Night_Mode

    Night_Mode.nm_css_bottom = Night_Mode.nm_css_buttons \
        + Night_Mode.nm_css_color_replacer + \
        """
body {
 background:-webkit-gradient(linear,
    left top, left bottom, from(#333), to(#222));
 border-top-color: #000;
}
.stattxt {
 color: #ccc;
}
        """
except ImportError:
    pass

FLIP_FLOP = True
# FLIP_FLOP = False

ANKI_MENU_ICONS = True
# ANKI_MENU_ICONS = False

try:
    MUSTHAVE_COLOR_ICONS = os.path.join(
        aqt.mw.pm.addonFolder(), 'handbook')
except:
    MUSTHAVE_COLOR_ICONS = ''

if MUSTHAVE_COLOR_ICONS == '':
    try:
        MUSTHAVE_COLOR_ICONS = os.path.join(
            aqt.mw.pm.addonFolder(), 'musthave_icons')
    except:
        MUSTHAVE_COLOR_ICONS = ''

ZERO_KEY_TO_SHOW_ANSWER = True
# ZERO_KEY_TO_SHOW_ANSWER = False

##

__addon__ = "'" + __name__.replace('_', ' ')
__version__ = "2.0.44a"

if __name__ == '__main__':
    print("This is " + __name__ + " add-on for the Anki program" +
          "and it can't be run directly.")
    print('Please download Anki 2.0 from https://apps.ankiweb.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2':  # Python 3 is utf8 only already.
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf8')

##

old_addons = (
    'Answer_Key_Remap.py',
    'Bigger_Show_Answer_Button.py',
    'Button_Colours_Good_Again.py',
    'Bigger_Show_All_Answer_Buttons.py',
    'More_Answer_Buttons_for_New_Cards.py',
    '_F4_Edit.py',
    '_Again_Hard.py',
    # '_Editor_Fontsize.py',
    '_Again_Hard_Good_Easy_wide_big_buttons.py',
    '_Alternative_hotkeys_to_cloze_selected_text_in_Add_or_Editor_window.py',
    '_Later_not_now_button.py',
    'More_Answer_Buttons_for_New_Cards.py',
    '_More_Answer_Buttons_for_ALL_Cards.py',
    'Low_Key_Anki_PassFail.py',
    '_Flip-flop.py',
)

old_addons2delete = ''
for old_addon in old_addons:
    if len(old_addon) > 0:
        old_filename = os.path.join(aqt.mw.pm.addonFolder(), old_addon)
        if os.path.exists(old_filename):
            old_addons2delete += old_addon[:-3] + ' \n'

if old_addons2delete != '':
    if lang == 'ru':
        aqt.utils.showText(
            'В каталоге\n\n ' + aqt.mw.pm.addonFolder() +
            '\n\nнайдены дополнения, которые уже включены в дополнение\n' +
            " Again Good HUGE buttons \n" +
            'и поэтому будут конфликтовать с ним.\n\n' +
            old_addons2delete +
            '\nУдалите эти дополнения и перезапустите Anki.')
    else:
        aqt.utils.showText(
            '<big>There are some add-ons in the folder <br>\n<br>\n' +
            ' &nbsp; ' + aqt.mw.pm.addonFolder() +
            '<pre>' + old_addons2delete + '</pre>' +
            'They are already part of<br>\n' +
            " <b> &nbsp; Again Good HUGE buttons</b>" +
            ' addon.<br>\n' +
            'Please, delete them and restart Anki.</big>', type="html")

act = [None, None, None, None, None]

# Anki uses a single digit to track which button has been clicked.
NOT_NOW_BASE = 5

# We will use shortcut number from the first extra button
#  and above to track the extra buttons.
INTERCEPT_EASE_BASE = 6

# Must be four or less
assert len(extra_buttons) <= 4

SWAP_TAG = False
# SWAP_TAG = datetime.datetime.now().strftime(
#    'rescheduled::re-%Y-%m-%d::re-card')
# SWAP_TAG = datetime.datetime.now().strftime('re-%y-%m-%d-c')

USE_INTERVALS_AS_LABELS = False  # True  #

FLAT_BUTTONS = True  # False  #

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


def laterNotNow(self, showAnswer):
    ret = '<style>td{vertical-align:bottom;}' +\
        'html, body, table { width: 100%; height: 100%;' +\
        ' margin: 0px; padding: 0px; box-sizing: content-box; }' +\
        '/*html,*/ body { overflow: hidden; } ' +\
        '</style>'

    if not NO_STYLES:
        ret += '<style>' +\
            'td button{font-size:large;}' +\
            'td.x button{font-size:x-large;color:#888;}' +\
            'td.xx button{font-size:xx-large;}' +\
            '</style>'

    if not NO_STYLES and FLAT_BUTTONS:
        ret += '<style>' +\
            'td.esc,td.xxx,td.stat{border:none;}' +\
            'td.esc button, td.xxx button, td.stat button {border:none;}' +\
            '/*td.stat,td.stat button{background-color:Ivory;}*/' +\
            'td.xxx, td.xxx button {background-color:aliceblue;}' +\
            'td.esc, td.esc button {background-color:whitesmoke;}' +\
            'td.but1, td.but1 button {background-color:#D72D2E;}' +\
            'td.but2, td.but2 button {background-color:#465A65;}' +\
            'td.but3, td.but3 button {background-color:#4CB050;}' +\
            'td.but4, td.but4 button {background-color:#03A9F5;}' +\
            'td.but button span, td.but button b, td.but, ' +\
            'td.but button {color:#ffFFff!important;border:none;}' +\
            'td.but button:focus {outline: orange 1px dashed;}' +\
            '</style>'

    if not NO_STYLES and FLAT_BUTTONS and (swAdded or not HIDE_LATER):
        ret += '<style>' +\
            'td.esc,td.xxx,td.stat{border-left:solid 1px silver;}' +\
            'td:first-child.stat{border-left:none;}' +\
            '</style>'

    if not NO_STYLES and USE_INTERVALS_AS_LABELS and FLAT_BUTTONS:
        ret += '<style>' +\
            '.stattxt, .nobold {display:none;}' +\
            ' button { width: 100%; height: 100%;} ' +\
            '</style>'

    ret += '<table cellpadding=0 cellspacing=0 width=100%><tr>'

    if HIDE_LATER:
        return ret

    ret = ret.replace('%', '%%') +\
        '<td align=center class="x esc" style="padding-right:.35em;" ' +\
        """onclick="py.link('ease%d');"><span class="stattxt">%s</span>""" +\
        '''<button title=" %s " onclick="py.link('ease%d');" ''' +\
        'style="width:99%%;%s">%s</button></td>'  # <td>&nbsp;</td>

    if showAnswer:
        if self.mw.col.conf['dueCounts']:
            retv = True
        else:
            retv = False
    else:
        if self.mw.col.conf['estTimes']:
            retv = True
        else:
            retv = False
    if USE_INTERVALS_AS_LABELS:
        retv = False

    if retv:
        return ret % (NOT_NOW_BASE, MSG[lang]['later'],
                      _("Shortcut key: %s") % (HOTKEY['later_not_now']),
                      NOT_NOW_BASE,
                      'color:' + black + ';', (MSG[lang]['later_not_now']))
    else:
        return ret % (NOT_NOW_BASE, "",
                      _("Shortcut key: %s") % (HOTKEY['later_not_now']),
                      NOT_NOW_BASE,
                      'color:' + black + ';', (MSG[lang]['later']))


def myShowAnswerButton(self, _old):
    if newRemaining(self):
        self.mw.moveToState('overview')
    self._bottomReady = True
    if not self.typeCorrect:
        self.bottom.web.setFocus()

    if USE_INTERVALS_AS_LABELS:
        middle = laterNotNow(self, True) + (
            '<td align=center style="width:%s;" class="xx xxx"' +
            ''' onclick="py.link('ans');"><span''' +
            ' class="stattxt">&nbsp;</span><button %s id=ansbut ' +
            '''style="width:100%%;%s" onclick="py.link('ans');" ''' +
            '>%s</button></td>' +
            '</tr></table>') % (
                BEAMS4,
                ' title=" ' + (_('Shortcut key: %s') % _('Space')) + ' " ',
                ' color:' + black + ';', self._remaining())
    else:
        middle = laterNotNow(self, True) + (
            '<td align=center style="width:%s;" class="xx xxx"' +
            ' onclick="py.link(\'ans\');"><span' +
            ' class="stattxt">%s</span><button %s id=ansbut ' +
            '''style="width:100%%;%s" onclick="py.link('ans');" ''' +
            '>%s</button></td>' +
            '</tr></table>') % (
                BEAMS4, self._remaining(),
                ' title=" ' + (_('Shortcut key: %s') % _('Space')) + ' " ',
                ' color:' + black + ';', _('Show Answer'))

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
    aqt.reviewer.Reviewer._showAnswerButton = anki.hooks.wrap(
        aqt.reviewer.Reviewer._showAnswerButton, myShowAnswerButton, 'around')

    # This wraps existing Reviewer._answerCard function.

    def answer_card_intercepting(self, actual_ease, _old):
        ease = actual_ease
        if actual_ease == NOT_NOW_BASE:
            self.nextCard()
            return True
        elif actual_ease < NOT_NOW_BASE:
            count = self.mw.col.sched.answerButtons(self.card)
            try:
                ease = remaps[remap][count][ease]
            except (KeyError, IndexError):
                pass
            return _old(self, ease)
        else:
            was_new_card = self.card.type in (0, 1, 2, 3)
            is_extra_button = was_new_card and \
                actual_ease >= INTERCEPT_EASE_BASE
            if is_extra_button:
                # Make sure this is as expected.
                # assert self.mw.col.sched.answerButtons(self.card) == 3
                # So this is one of our buttons.
                # First answer the card as if 'Easy' clicked.
                ease = 3
                # We will need this to reschedule it.
                prev_card_id = self.card.id
                prev_card_factor = self.card.factor
                #
                buttonItem = extra_buttons[actual_ease - INTERCEPT_EASE_BASE]
                # Do the reschedule.
                self.mw.checkpoint(_('Reschedule card'))
                # self.mw.col.sched.reschedCards([prev_card_id],
                #   buttonItem['ReschedMin'], buttonItem['ReschedMax'])
                _reschedCards(
                    self.mw.col.sched, [prev_card_id],
                    buttonItem['ReschedMin'], buttonItem['ReschedMax'],
                    indi=prev_card_factor)
                aqt.utils.tooltip(
                    '<center>Rescheduled:' + '<br>' +
                    buttonItem['Description'] + '</center>')

                SwapTag = SWAP_TAG
                if SwapTag:
                    SwapTag += unicode(self.mw.reviewer.card.ord + 1)
                    note = self.mw.reviewer.card.note()
                    if not note.hasTag(SwapTag):
                        note.addTag(SwapTag)
                        note.flush()  # never forget to flush

                self.mw.reset()
                return True
            else:
                ret = _old(self, ease)
                return ret

    aqt.reviewer.Reviewer._answerCard = anki.hooks.wrap(
        aqt.reviewer.Reviewer._answerCard,
        answer_card_intercepting, 'around')
# 'before' does not working as intended cause ease is changing inside AKR


# to remove <span class=nobold>
def _bottomTimes(self, i):
    if not self.mw.col.conf['estTimes']:
        return '&nbsp;'
    txt = self.mw.col.sched.nextIvlStr(self.card, i, True) or '&nbsp;'
    return txt.replace("<", "&lt;")


# always show interval despite user's preferences
def _bottomTime(self, i):
    # if not self.mw.col.conf['estTimes']:
    #    return '&nbsp;'
    txt = self.mw.col.sched.nextIvlStr(self.card, i, True) or '&nbsp;'
    return txt.replace("<", "&lt;")


def BTN_LBL(title):
    if NO_STYLES:
        return '<b style="color:%s;">' % (BTN_CLR[title]) + \
            _(title) + '</b>'
    elif NO_SMILES:
        return '<span style="color:%s;">' % (BTN_CLR[title]) + \
            BTN_LABL[lang][title] + '</span>'
    else:
        return BUTTON_LABEL[title]


# Replace _answerButtonList method
def answerButtonList(self):
    if remap == 'All':
        l = ((1, '' + BTN_LBL('Again') + '', BEAMS1),)
        cnt = self.mw.col.sched.answerButtons(self.card)
    elif remap == 'Again':
        l = ((1, '' + BTN_LBL('Again') + '', BEAMS4),)
        cnt = 1
        return l
    else:
        l = ((1, '' + BTN_LBL('Again') + '', BEAMS2),)
        cnt = 2
    if cnt == 2:
        if remap == 'All':
            return l + ((2, '' + BTN_LBL('Good') + '', BEAMS3),)
        else:
            return l + ((2, '' + BTN_LBL(remap) + '', BEAMS2),)
        # the comma at the end is mandatory, a subtle bug occurs without it
    elif cnt == 3:
        return l + ((2, '' + BTN_LBL('Good') + '', BEAMS2),
                    (3, '' + BTN_LBL('Easy') + '', BEAMS1))
    else:
        return l + ((2, '' + BTN_LBL('Hard') + '', BEAMS1),
                    (3, '' + BTN_LBL('Good') + '', BEAMS1),
                    (4, '' + BTN_LBL('Easy') + '', BEAMS1))
# all buttons are with coloured text
# and have an equal width with buttons in Night Mode


def answerCard_tooltip(self, ease):
    l = self._answerButtonList()
    a = [item for item in l if item[0] == ease]
    if len(a) > 0:
        return a[0][1]
    else:
        return ''


def myAnswerButtons(self, _old):
    times = []
    default = self._defaultEase()

    cnt = self.mw.col.sched.answerButtons(self.card)

    def but(i, label, beam):
        if i == default:
            extra = 'id=defease'
        else:
            extra = ''
        # due = self._buttonTime(i)

        j = i
        cnt = self.mw.col.sched.answerButtons(self.card)
        if remap == 'All':
            if cnt == 2:
                if i == 2:
                    j = 3
            elif cnt == 3:
                if i == 2:
                    j = 3
                if i == 3:
                    j = 4
            due = _bottomTimes(self, i)
            ij = j
        else:
            ij = j
            if i == 2:
                if remap == 'Good':
                    ij = 3
                    if cnt == 4:
                        j = 3
                    else:
                        j = 2
                if remap == 'Easy':
                    ij = 4
                    j = cnt
            due = _bottomTimes(self, j)

        text_label = anki.utils.stripHTML(label)
        if text_label != answerCard_tooltip(self, i):
            text_label += '   ' + answerCard_tooltip(self, i)
        text_label += '   '

        if USE_INTERVALS_AS_LABELS:
            return '''
<td align=center class="but but%s xx" style="width:%s;"
 onclick="py.link('ease%d');"><span class="stattxt">&nbsp;</span
><button %s title="%s" style="width:99%%;%s" onclick="py.link('ease%d');"
><b>%s</b></button></td>''' % (
                        ij, beam, j, extra,
                        ('  ' + text_label + due +
                         ' -- ' + _('Shortcut key: %s') % j +
                         '  ').replace(' ', ' '),
                        "color:"+BUTTON_COLOR[remap][j]+";", j, due)
        else:
            return '''
<td align=center class="but but%s xx" style="width:%s;"
 onclick="py.link('ease%d');"><span class="stattxt">%s</span
><button %s title="%s" style="width:99%%;%s" onclick="py.link('ease%d');"
>%s</button></td>''' % (ij, beam, j, due, extra,
                        ('  ' + text_label + due +
                         ' -- ' + _('Shortcut key: %s') % j +
                         '  ').replace(' ', ' '),
                        "", j, label)

    buf = laterNotNow(self, False)

    for ease, lbl, beams in answerButtonList(self):
        buf += but(ease, lbl, beams)

    # swAdded start ====>
    # Only for cards in the new queue
    if swAdded and self.card.type in (0, 1, 2, 3):  # New, Learn, Day learning
        # Check that the number of answer buttons is as expected.
        #  assert self.mw.col.sched.answerButtons(self.card) == 3
        # python lists are 0 based
        for i, buttonItem in enumerate(extra_buttons):
            if USE_INTERVALS_AS_LABELS:
                buf += '''
<td align=center class="x xxx"
 onclick="py.link('ease%d');"><span class="stattxt">&nbsp;</span
><button title="%s" onclick="py.link('ease%d');">\
%s</button></td>''' % (i + INTERCEPT_EASE_BASE,
                       _('Shortcut key: %s') % buttonItem['ShortCut'],
                       i + INTERCEPT_EASE_BASE,
                       buttonItem['Description'])
            else:
                buf += '''
<td align=center class="x xxx"
 onclick="py.link('ease%d');"><span class="stattxt">%s</span
><button title="%s" onclick="py.link('ease%d');">\
%s</button></td>''' % (
                    i + INTERCEPT_EASE_BASE,
                    buttonItem['Description'],
                    _('Shortcut key: %s') % buttonItem['ShortCut'],
                    i + INTERCEPT_EASE_BASE,
                    buttonItem['Label'])
    # swAdded end   ====>

    return (
        buf + "</tr></table>" +
        "<script>$(function(){$('#defease').focus();});</script>")


def answer_card_intercepting_WTF(self, actual_ease, _old):
    ease = actual_ease
    if actual_ease >= NOT_NOW_BASE:
        self.nextCard()
        return True
    else:
        return _old(self, ease)


def save_wide_buttons():
    aqt.mw.pm.profile['wide_big_buttons'] = (
        more_action.isChecked())
    aqt.mw.pm.profile['remap_buttons'] = (
        remap)
    aqt.mw.pm.profile['hide_later'] = (
        HIDE_LATER)
    aqt.mw.pm.profile['swAdded'] = (
        swAdded)
    aqt.mw.pm.profile['NO_SMILES'] = (
        NO_SMILES)
    aqt.mw.pm.profile['NO_STYLES'] = (
        NO_STYLES)
    aqt.mw.pm.profile['ctb_edit_more'] = (
        EDIT_MORE_BUTTONS)
    aqt.mw.pm.profile['flat_buttons'] = (
        FLAT_BUTTONS)


def load_wide_buttons():
    global USE_INTERVALS_AS_LABELS, more_action, remap, act, HIDE_LATER,\
        hide_later_action, EDIT_MORE_BUTTONS, edit_more_action, swAdded,\
        swAdded_action, NO_STYLES, styles_action, FLAT_BUTTONS, flat_action,\
        NO_SMILES, smiles_action
    try:
        remap = aqt.mw.pm.profile['remap_buttons']
    except KeyError:
        remap = 'All'
    try:
        USE_INTERVALS_AS_LABELS = aqt.mw.pm.profile['wide_big_buttons']
    except KeyError:
        USE_INTERVALS_AS_LABELS = False
    more_action.setChecked(USE_INTERVALS_AS_LABELS)

    if remap == 'All':
        act[0].setChecked(True)
    if remap == 'Again':
        act[1].setChecked(True)
    if remap == 'Hard':
        act[2].setChecked(True)
    if remap == 'Good':
        act[3].setChecked(True)
    if remap == 'Easy':
        act[4].setChecked(True)

    try:
        EDIT_MORE_BUTTONS = aqt.mw.pm.profile['ctb_edit_more']
    except KeyError:
        EDIT_MORE_BUTTONS = True

    edit_more_action.setChecked(not EDIT_MORE_BUTTONS)
    edit_more_proc()

    try:
        HIDE_LATER = aqt.mw.pm.profile['hide_later']
    except KeyError:
        HIDE_LATER = False

    hide_later_action.setChecked(HIDE_LATER)

    try:
        swAdded = aqt.mw.pm.profile['swAdded']
    except KeyError:
        swAdded = True

    swAdded_action.setChecked(not swAdded)

    try:
        NO_SMILES = aqt.mw.pm.profile['NO_SMILES']
    except KeyError:
        NO_SMILES = False

    smiles_action.setChecked(NO_SMILES)

    try:
        NO_STYLES = aqt.mw.pm.profile['NO_STYLES']
    except KeyError:
        NO_STYLES = False

    styles_action.setChecked(NO_STYLES)

    try:
        FLAT_BUTTONS = aqt.mw.pm.profile['flat_buttons']
    except KeyError:
        FLAT_BUTTONS = True

    flat_action.setChecked(FLAT_BUTTONS)

    if NO_STYLES or USE_INTERVALS_AS_LABELS:
        smiles_action.setEnabled(False)

##

if old_addons2delete == '':
    anki.hooks.addHook("unloadProfile", save_wide_buttons)
    anki.hooks.addHook("profileLoaded", load_wide_buttons)

    try:
        aqt.mw.addon_view_menu
    except AttributeError:
        aqt.mw.addon_view_menu = QMenu(MSG[lang]['View'], aqt.mw)
        aqt.mw.form.menubar.insertMenu(
            aqt.mw.form.menuTools.menuAction(), aqt.mw.addon_view_menu)

    try:
        aqt.mw.huge_buttons
    except AttributeError:
        aqt.mw.huge_buttons = QMenu(MSG[lang]['HUGE_buttons'], aqt.mw)
        aqt.mw.addon_view_menu.addMenu(aqt.mw.huge_buttons)

    aqt.mw.huge_buttons.addSeparator()

    def onSmiles():
        global NO_SMILES
        NO_SMILES = smiles_action.isChecked()

        rst = aqt.mw.reviewer.state == 'answer'
        aqt.mw.reset()
        if rst:
            aqt.mw.reviewer._showAnswerHack()

    def onStyles():
        global NO_STYLES, FLAT_BUTTONS, flat_action, smiles_action
        NO_STYLES = styles_action.isChecked()
        if NO_STYLES:
            flat_action.setChecked(False)
            FLAT_BUTTONS = False
            smiles_action.setEnabled(False)
        else:
            smiles_action.setEnabled(True)

        rst = aqt.mw.reviewer.state == 'answer'
        aqt.mw.reset()
        if rst:
            aqt.mw.reviewer._showAnswerHack()

    def flat_proc():
        global NO_STYLES, FLAT_BUTTONS, styles_action

        if flat_action.isChecked():
            styles_action.setChecked(False)
            NO_STYLES = False
            FLAT_BUTTONS = True
        else:
            FLAT_BUTTONS = False

        rst = aqt.mw.reviewer.state == 'answer'
        aqt.mw.reset()
        if rst:
            aqt.mw.reviewer._showAnswerHack()

    def more_proc():
        global USE_INTERVALS_AS_LABELS, smiles_action
        if more_action.isChecked():
            USE_INTERVALS_AS_LABELS = True
            smiles_action.setEnabled(False)
        else:
            USE_INTERVALS_AS_LABELS = False
            smiles_action.setEnabled(True)

        rst = aqt.mw.reviewer.state == 'answer'
        aqt.mw.reset()
        if rst:
            aqt.mw.reviewer._showAnswerHack()

    smiles_action = QAction(MSG[lang]['no_smiles'], aqt.mw)
    smiles_action.setShortcut(HOTKEY['no_smiles'])
    smiles_action.setCheckable(True)
    smiles_action.setCheckable(True)
    smiles_action.setChecked(NO_SMILES)
    aqt.mw.connect(smiles_action, SIGNAL('triggered()'), onSmiles)

    styles_action = QAction(MSG[lang]['no_styles'], aqt.mw)
    styles_action.setShortcut(HOTKEY['no_styles'])
    styles_action.setCheckable(True)
    styles_action.setChecked(NO_STYLES)
    aqt.mw.connect(styles_action, SIGNAL('triggered()'), onStyles)

    flat_action = QAction(MSG[lang]['flat_buttons'], aqt.mw)
    flat_action.setShortcut(HOTKEY['flat_buttons'])
    flat_action.setCheckable(True)
    flat_action.setChecked(FLAT_BUTTONS)
    aqt.mw.connect(flat_action, SIGNAL('triggered()'), flat_proc)

    more_action = QAction(MSG[lang]['no_labels'], aqt.mw)
    more_action.setShortcut(HOTKEY['no_labels'])
    more_action.setCheckable(True)
    more_action.setChecked(USE_INTERVALS_AS_LABELS)
    aqt.mw.connect(more_action, SIGNAL('triggered()'), more_proc)

    aqt.mw.huge_buttons.addAction(styles_action)
    aqt.mw.huge_buttons.addAction(flat_action)
    aqt.mw.huge_buttons.addAction(more_action)
    aqt.mw.huge_buttons.addAction(smiles_action)

    aqt.reviewer.Reviewer._answerButtons = anki.hooks.wrap(
        aqt.reviewer.Reviewer._answerButtons, myAnswerButtons, 'around')

    def onEscape():
        aqt.mw.reviewer.nextCard()

    try:
        aqt.mw.addon_cards_menu
    except AttributeError:
        aqt.mw.addon_cards_menu = QMenu(MSG[lang]['Cards'], aqt.mw)
        aqt.mw.form.menubar.insertMenu(
            aqt.mw.form.menuTools.menuAction(), aqt.mw.addon_cards_menu)

    escape_action = QAction(aqt.mw)
    escape_action.setText(MSG[lang]['Later, not now'])
    escape_action.setShortcut(HOTKEY['later_not_now'])
    escape_action.setEnabled(False)
    aqt.mw.connect(escape_action, SIGNAL('triggered()'), onEscape)

    aqt.mw.addon_cards_menu.addAction(escape_action)

    aqt.mw.deckBrowser.show = anki.hooks.wrap(
        aqt.mw.deckBrowser.show, lambda: escape_action.setEnabled(False))
    aqt.mw.overview.show = anki.hooks.wrap(
        aqt.mw.overview.show, lambda: escape_action.setEnabled(False))
    aqt.mw.reviewer.show = anki.hooks.wrap(
        aqt.mw.reviewer.show, lambda: escape_action.setEnabled(True))

    def setup_menu():
        # Add a submenu to a view menu.
        # Add a submenu that lists the available answer buttons
        global act_all, act_hard, act_good, act_easy

        aqt.mw.extra_class_submenu = QMenu(
            '&'+MSG[lang]['HardGoodEasy'], aqt.mw)

        # aqt.mw.huge_buttons.addSeparator()
        aqt.mw.huge_buttons.addMenu(aqt.mw.extra_class_submenu)

        def set_buttons(parm_btn, parm_act):
            global remap
            remap = parm_btn

            rst = aqt.mw.reviewer.state == 'answer'
            aqt.mw.reset()
            if rst:
                aqt.mw.reviewer._showAnswerHack()

        def setup_ag(parm_msg, parm_btns, parm_chk, parm_act, n):
            parm_act[n] = action_group.addAction(
                QAction(parm_msg, aqt.mw, checkable=True))
            parm_act[n].setChecked(parm_chk)
            parm_act[n].setShortcut(HOTKEY[parm_btns])
            aqt.mw.extra_class_submenu.addAction(parm_act[n])
            aqt.mw.connect(parm_act[n], SIGNAL("triggered()"),
                           lambda: set_buttons(parm_btns, parm_act[n]))

        action_group = QActionGroup(aqt.mw, exclusive=True)

        setup_ag(MSG[lang]['HardGoodEasy'], 'All', remap == 'All', act, 0)

        aqt.mw.extra_class_submenu.addSeparator()

        setup_ag(MSG[lang]['Again'], 'Again', remap == 'Again', act, 1)
        setup_ag(MSG[lang]['AgainHard'], 'Hard', remap == 'Hard', act, 2)
        setup_ag(MSG[lang]['AgainGood'], 'Good', remap == 'Good', act, 3)
        setup_ag(MSG[lang]['AgainEasy'], 'Easy', remap == 'Easy', act, 4)

    setup_menu()

    def onHideLater():
        global HIDE_LATER
        HIDE_LATER = hide_later_action.isChecked()

        rst = aqt.mw.reviewer.state == 'answer'
        aqt.mw.reset()
        if rst:
            aqt.mw.reviewer._showAnswerHack()

    hide_later_action = QAction(aqt.mw)
    hide_later_action.setText(
        MSG[lang]['Hide button: '] + ' ' + MSG[lang]['Later, not now'])
    hide_later_action.setShortcut(HOTKEY['hide_later'])
    hide_later_action.setCheckable(True)
    aqt.mw.connect(hide_later_action, SIGNAL('triggered()'), onHideLater)
    aqt.mw.huge_buttons.addAction(hide_later_action)

    ##

    EDIT_MORE_BUTTONS = False  # True  #

    MORE_EDIT = " td.stat button { visibility: hidden; } "
    EDIT_MORE = " td\.stat button \{ visibility\: hidden\; \} "

    MORE_EDIT = " td.stat { display: none; } "
    EDIT_MORE = " td\.stat \{ display\: none\; \} "

    def initEditMore(editMore):
        global EDIT_MORE_BUTTONS
        EDIT_MORE_BUTTONS = editMore
        if not editMore:
            aqt.mw.reviewer._bottomCSS += MORE_EDIT
        else:
            aqt.mw.reviewer._bottomCSS = re.sub(
                EDIT_MORE, "", aqt.mw.reviewer._bottomCSS)

    initEditMore(EDIT_MORE_BUTTONS)

    def edit_more_proc():
        global EDIT_MORE_BUTTONS
        EDIT_MORE_BUTTONS = edit_more_action.isChecked()

        initEditMore(not EDIT_MORE_BUTTONS)

        rst = aqt.mw.reviewer.state == 'answer'
        aqt.mw.reset()
        if rst:
            aqt.mw.reviewer._showAnswerHack()

    edit_more_action = QAction(
        MSG[lang]['Hide buttons'] + MSG[lang]['Edit'] + ' ' +
        MSG[lang]['More'], aqt.mw)
    edit_more_action.setShortcut(HOTKEY['HideButtons'])
    edit_more_action.setCheckable(True)
    edit_more_action.setChecked(not EDIT_MORE_BUTTONS)
    aqt.mw.connect(edit_more_action, SIGNAL('triggered()'), edit_more_proc)
    aqt.mw.huge_buttons.addAction(edit_more_action)

    def swAdded_proc():
        global swAdded
        swAdded = not swAdded_action.isChecked()

        rst = aqt.mw.reviewer.state == 'answer'
        aqt.mw.reset()
        if rst:
            aqt.mw.reviewer._showAnswerHack()

    swAdded_action = QAction(
        MSG[lang]['no_extra_buttons'], aqt.mw)
    swAdded_action.setShortcut(HOTKEY['no_extra_buttons'])
    swAdded_action.setCheckable(True)
    swAdded_action.setChecked(not EDIT_MORE_BUTTONS)
    aqt.mw.connect(swAdded_action, SIGNAL('triggered()'), swAdded_proc)
    aqt.mw.huge_buttons.addAction(swAdded_action)

    def about_addon():
        """
        Show "About addon" message popup window.
        """
        aa_about_box = QMessageBox()
        aa_about_box.setText(
            __addon__ + "   " + __version__ + "\n" + __doc__)
        aa_width, aa_height = (1024, 768)
        # aa_width, aa_height = (1920, 1080)
        aa_left = (aa_width-480)/2
        aa_right = (aa_height-640)/2
        aa_about_box.setGeometry(aa_left, aa_right, 480, 640)
        aa_about_box.setWindowTitle(MSG[lang]['aa'] + __addon__)
        aa_about_box.exec_()

    about_addon_action = QAction(MSG[lang]['aa'] + __addon__, aqt.mw)
    aqt.mw.connect(about_addon_action, SIGNAL('triggered()'), about_addon)
    aqt.mw.huge_buttons.addSeparator()
    aqt.mw.huge_buttons.addAction(about_addon_action)

    # F4

    try:
        MUSTHAVE_COLOR_ICONS = os.path.join(
            aqt.mw.pm.addonFolder(), 'handbook')
    except:
        MUSTHAVE_COLOR_ICONS = ''

    def go_edit_current():
        """Edit the current card when there is one."""
        try:
            aqt.mw.onEditCurrent()
        except AttributeError:
            pass

    def go_edit_layout():
        """Edit the current card's note's layout if there is one."""
        try:
            ccard = aqt.mw.reviewer.card
            CardLayout(aqt.mw, ccard.note(), ord=ccard.ord)
        except AttributeError:
            return

    def go_edit_fields():
        aqt.editor.onFields(aqt.mw)

    F4_edit_current_action = QAction(aqt.mw)
    F4_edit_current_action.setText(MSG[lang]['Edit'])
    F4_edit_current_action.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_current.png')))
    F4_edit_current_action.setShortcut(HOTKEY['Edit_Fields'])
    F4_edit_current_action.setEnabled(False)

    F4_edit_layout_action = QAction(aqt.mw)
    F4_edit_layout_action.setText(MSG[lang]['Edit Layout'])
    F4_edit_layout_action.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_layout.png')))
    F4_edit_layout_action.setShortcut(HOTKEY['Edit_Cards'])
    F4_edit_layout_action.setEnabled(False)

    F4_edit_fields_action = QAction(aqt.mw)
    F4_edit_fields_action.setText(MSG[lang]['Edit Fields'])
    F4_edit_fields_action.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_fields.png')))
    F4_edit_fields_action.setShortcut(HOTKEY['Edit_Fieldz'])
    F4_edit_fields_action.setEnabled(False)

    def swap_off():
        F4_edit_current_action.setEnabled(False)
        F4_edit_layout_action.setEnabled(False)
        F4_edit_fields_action.setEnabled(False)

    def swap_on():
        F4_edit_current_action.setEnabled(True)
        F4_edit_layout_action.setEnabled(True)
        F4_edit_fields_action.setEnabled(True)

    def onFields(self):
        from aqt.fields import FieldDialog
        FieldDialog(self, self.card.note(), parent=aqt.mw)

    F4_Edit_exists = os.path.exists(
        os.path.join(aqt.mw.pm.addonFolder(), '_F4_Edit.py')) or \
        os.path.exists(
            os.path.join(aqt.mw.pm.addonFolder(), '_Editor_Fontsize.py'))

    if not F4_Edit_exists:
        aqt.mw.connect(
            F4_edit_current_action, SIGNAL('triggered()'), go_edit_current)
        aqt.mw.connect(
            F4_edit_layout_action, SIGNAL('triggered()'), go_edit_layout)
        aqt.mw.connect(
            F4_edit_fields_action, SIGNAL('triggered()'),
            lambda: onFields(aqt.mw.reviewer))

        aqt.mw.addon_cards_menu.addSeparator()
        aqt.mw.addon_cards_menu.addAction(F4_edit_current_action)
        aqt.mw.addon_cards_menu.addAction(F4_edit_layout_action)
        aqt.mw.addon_cards_menu.addAction(F4_edit_fields_action)
        aqt.mw.addon_cards_menu.addSeparator()

        aqt.mw.deckBrowser.show = anki.hooks.wrap(
            aqt.mw.deckBrowser.show, swap_off)
        aqt.mw.overview.show = anki.hooks.wrap(
            aqt.mw.overview.show, swap_off)
        aqt.mw.reviewer.show = anki.hooks.wrap(
            aqt.mw.reviewer.show, swap_on)

    # F4 as well as Ctrl+Shift+X in Fields Editor
    #   (Add Card, Edit Card, Browse)
    def myHTMLeditF4(self):
        f4 = QShortcut(
            QKeySequence(HOTKEY['Edit_HTML']), self.parentWindow)
        f4.connect(f4, SIGNAL('activated()'), self.onHtmlEdit)

    aqt.editor.Editor.setupButtons = anki.hooks.wrap(
        aqt.editor.Editor.setupButtons, myHTMLeditF4)

##

    def onAltCloze(self, delta):
        # check that the model is set up for cloze deletion
        if not re.search('{{(.*:)*cloze:',
                         self.note.model()['tmpls'][0]['qfmt']):
            if self.addMode:
                aqt.utils.tooltip(
                    _("Warning, cloze deletions will not work until " +
                      "you switch the type at the top to Cloze."))
            else:
                aqt.utils.showInfo(_("""\
    To make a cloze deletion on an existing note, you need to change it \
    to a cloze type first, via Edit>Change Note Type."""))
                return
        # find the highest existing cloze
        highest = 0
        for name, val in self.note.items():
            m = re.findall("\{\{c(\d+)::", val)
            if m:
                highest = max(highest, sorted([int(x) for x in m])[-1])
        # reuse last?
        # if not self.mw.app.keyboardModifiers() & Qt.AltModifier:
        highest += delta
        # must start at 1
        highest = max(1, highest)
        self.web.eval("wrap('{{c%d::', '}}');" % highest)

    def setupButtonz(self):
        s = QShortcut(
            QKeySequence(HOTKEY["next_cloze"]), self.parentWindow)
        s.connect(s, SIGNAL('activated()'), self.onCloze)

        s = QShortcut(
            QKeySequence(HOTKEY["same_cloze"]), self.parentWindow)
        s.connect(s, SIGNAL('activated()'), self.onCloze)

        s = QShortcut(QKeySequence(
            HOTKEY['same_without_Alt']), self.parentWindow)
        s.connect(s, SIGNAL('activated()'), lambda: onAltCloze(self, 0))

        s = QShortcut(QKeySequence(
            HOTKEY["next_closure"]), self.parentWindow)
        s.connect(s, SIGNAL('activated()'), self.onCloze)

        s = QShortcut(QKeySequence(
            HOTKEY["same_closure"]), self.parentWindow)
        s.connect(s, SIGNAL('activated()'), self.onCloze)

        s = QShortcut(QKeySequence(HOTKEY["LaTeX"]), self.widget)
        s.connect(s, SIGNAL("activated()"), self.insertLatex)
        s = QShortcut(QKeySequence(HOTKEY["LaTeX$"]), self.widget)
        s.connect(s, SIGNAL("activated()"), self.insertLatexEqn)
        s = QShortcut(QKeySequence(HOTKEY["LaTeX$$"]), self.widget)
        s.connect(s, SIGNAL("activated()"), self.insertLatexMathEnv)

    aqt.editor.Editor.setupButtons = anki.hooks.wrap(
        aqt.editor.Editor.setupButtons, setupButtonz)

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
button, but in addition, they reschedule the card to different interval,
 which is randomly assigned between a lower and upper limit that is preset
  by the user (see below).

By default 3 buttons are added, with intervals: "3-4d" , "5-7d" , "8-15d"
This can be changed below.

I wanted this addon because many of my new cards do not need to be
"Learned" as I created and added them myself, typically an hour or so before
my first review session. I often add around 100-200 new cards per day, all on
a related topic, and this addon allows me to spread the next review
 of the new cards that don't need learning out in time.

How it works: This addon works by intercepting the creation of the reviewer
  buttons and adds up to 4 extra buttons to the review window.
   The answer function
  is wrapped and the ease parameter is checked to see if it one of the new
  buttons. If it is, the standard answer function is used to add the card
  as an easy card, and then the browser 'reschedCards' function is used
  to reschedule it to the desired interval.

In summary, this functions as if you click the "Easy" button on a new card,
  and then go to the browser and reschedule the card.

Warning: This completely replaces the Reviewer._answerButtons fn,
 so any changes
   to that function in future updates will be lost. Could ask for a hook?
Warning: buyer beware ... The author is not a python, nor a qt programmer

Support: None. Use at your own risk. If you do find a problem please email me
at steveawa@gmail.com

Setup data
List of dicts, where each item of the list (a dict) is the data
for a new button.
This can be edited to suit, but there can not be more than 4 buttons.

Description ... appears above the button
Label ... the label of the button
ShortCut ... the shortcut key for the button

ReschedMin ... same as the lower number
    in the Browser's "Edit/Rescedule" command
ReschedMax ... same as the higher number
    in the Browser's "Edit/Rescedule" command
"""

##

if old_addons2delete == '':

    def _reschedCards(self, ids, imin, imax, indi=2500):
        "Put cards in review queue with a new interval in days (min, max)."
        d = []
        t = self.today
        mod = anki.utils.intTime()
        for id in ids:
            r = random.randint(imin, imax)
            d.append(dict(id=id, due=r + t, ivl=max(1, r), mod=mod,
                          usn=self.col.usn(), fact=indi))
        self.remFromDyn(ids)
        self.col.db.executemany("""
    update cards set type=2,queue=2,ivl=:ivl,due=:due,odue=0,
    usn=:usn,mod=:mod,factor=:fact where id=:id""", d)
        self.col.log(ids)

    def keyHandler(self, evt, _old):
        key = unicode(evt.text())
        if self.state == 'answer':
            for i, buttonItem in enumerate(extra_buttons):
                if key == buttonItem['ShortCut']:
                    # early exit ok in python?
                    return self._answerCard(i + INTERCEPT_EASE_BASE)
        return _old(self, evt)

    aqt.reviewer.Reviewer._keyHandler = anki.hooks.wrap(
        aqt.reviewer.Reviewer._keyHandler, keyHandler, 'around')

##############
# • Flip-flop


def go_question():
    if aqt.mw.state == 'review':
        if (aqt.mw.reviewer.state == 'answer' or
                aqt.mw.reviewer.state == 'question'):
            # refresh FrontSide on PageUp
            anki.sound.stopMplayer()
            aqt.mw.reviewer._showQuestion()


def go_answer():
    if aqt.mw.state == 'review':
        if aqt.mw.reviewer.state == 'question':
            anki.sound.stopMplayer()
            aqt.mw.reviewer._showAnswer()

PageUp_icon = QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'PageUp.png'))
PageDown_icon = QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'PageDown.png'))

#
if FLIP_FLOP:

    show_question_auction = QAction(aqt.mw)
    show_question_auction.setText(MSG[lang]['showFrontSide'])
    show_question_auction.setShortcut(QKeySequence(HOTKEY['showFrontSide']))
    if ANKI_MENU_ICONS:
        show_question_auction.setIcon(PageUp_icon)
    aqt.mw.connect(show_question_auction, SIGNAL('triggered()'), go_question)

    show_answer_auction = QAction(aqt.mw)
    show_answer_auction.setText(MSG[lang]['showBackSide'])
    show_answer_auction.setShortcut(HOTKEY['showBackSide'])
    if ANKI_MENU_ICONS:
        show_answer_auction.setIcon(PageDown_icon)
    aqt.mw.connect(show_answer_auction, SIGNAL('triggered()'), go_answer)

    aqt.mw.form.menuEdit.addSeparator()
    aqt.mw.form.menuEdit.addAction(show_question_auction)
    aqt.mw.form.menuEdit.addAction(show_answer_auction)
    aqt.mw.form.menuEdit.addSeparator()

##

mw_addon_view_menu_exists = hasattr(aqt.mw, 'addon_view_menu')

if FLIP_FLOP and mw_addon_view_menu_exists:

    show_question_aktion = QAction(aqt.mw)
    show_question_aktion.setText(MSG[lang]['viewFrontSide'])
    show_question_aktion.setShortcut(HOTKEY['viewFrontSide'])
    if ANKI_MENU_ICONS:
        show_question_aktion.setIcon(PageUp_icon)
    aqt.mw.connect(show_question_aktion, SIGNAL('triggered()'), go_question)

    show_answer_aktion = QAction(aqt.mw)
    show_answer_aktion.setText(MSG[lang]['viewBackSide'])
    show_answer_aktion.setShortcut(HOTKEY['viewBackSide'])
    if ANKI_MENU_ICONS:
        show_answer_aktion.setIcon(PageDown_icon)
    aqt.mw.connect(show_answer_aktion, SIGNAL('triggered()'), go_answer)

    aqt.mw.addon_view_menu.addSeparator()
    aqt.mw.addon_view_menu.addAction(show_question_aktion)
    aqt.mw.addon_view_menu.addAction(show_answer_aktion)
    aqt.mw.addon_view_menu.addSeparator()

##

mw_addon_cards_menu_exists = hasattr(aqt.mw, 'addon_cards_menu')

if FLIP_FLOP and mw_addon_cards_menu_exists:

    snow_question_action = QAction(aqt.mw)
    snow_question_action.setText(MSG[lang]['cardFrontSide'])
    snow_question_action.setShortcut(HOTKEY['cardFrontSide'])
    if ANKI_MENU_ICONS:
        snow_question_action.setIcon(PageUp_icon)
    aqt.mw.connect(
        snow_question_action, SIGNAL("triggered()"), go_question)

    snow_answer_action = QAction(aqt.mw)
    snow_answer_action.setText(MSG[lang]['cardBackSide'])
    snow_answer_action.setShortcut(HOTKEY['cardBackSide'])
    if ANKI_MENU_ICONS:
        snow_answer_action.setIcon(PageDown_icon)
    aqt.mw.connect(
        snow_answer_action, SIGNAL("triggered()"), go_answer)

    aqt.mw.addon_cards_menu.addSeparator()
    aqt.mw.addon_cards_menu.addAction(snow_question_action)
    aqt.mw.addon_cards_menu.addAction(snow_answer_action)
    aqt.mw.addon_cards_menu.addSeparator()

##

try:
    aqt.mw.addon_sound_menu.addSeparator()
except AttributeError:
    aqt.mw.addon_sound_menu = QMenu(MSG[lang]['Sound'], aqt.mw)
    aqt.mw.form.menubar.insertMenu(
        aqt.mw.form.menuTools.menuAction(), aqt.mw.addon_sound_menu)

mw_addon_sound_menu_exists = hasattr(aqt.mw, 'addon_sound_menu')

if FLIP_FLOP and mw_addon_sound_menu_exists:

    show_question_action = QAction(aqt.mw)
    show_question_action.setText(MSG[lang]['gotoFrontSide'])
    show_question_action.setShortcut(HOTKEY['gotoFrontSide'])
    if ANKI_MENU_ICONS:
        show_question_action.setIcon(PageUp_icon)
    aqt.mw.connect(
        show_question_action, SIGNAL('triggered()'), go_question)

    show_answer_action = QAction(aqt.mw)
    show_answer_action.setText(MSG[lang]['gotoBackSide'])
    show_answer_action.setShortcut(HOTKEY['gotoBackSide'])
    if ANKI_MENU_ICONS:
        show_answer_action.setIcon(PageDown_icon)
    aqt.mw.connect(
        show_answer_action, SIGNAL('triggered()'), go_answer)

    aqt.mw.addon_sound_menu.addSeparator()
    aqt.mw.addon_sound_menu.addAction(show_question_action)
    aqt.mw.addon_sound_menu.addAction(show_answer_action)
    aqt.mw.addon_sound_menu.addSeparator()

##

try:
    aqt.mw.addon_go_menu.addSeparator()
except AttributeError:
    aqt.mw.addon_go_menu = QMenu(MSG[lang]['Go'], aqt.mw)
    aqt.mw.form.menubar.insertMenu(
        aqt.mw.form.menuTools.menuAction(), aqt.mw.addon_go_menu)

mw_addon_go_menu_exists = hasattr(aqt.mw, 'addon_go_menu')

if FLIP_FLOP and mw_addon_go_menu_exists:

    show_question_action = QAction(aqt.mw)
    show_question_action.setText(MSG[lang]['goFrontSide'])
    show_question_action.setShortcut(HOTKEY['goFrontSide'])
    if ANKI_MENU_ICONS:
        show_question_action.setIcon(PageUp_icon)
    aqt.mw.connect(
        show_question_action, SIGNAL('triggered()'), go_question)

    show_answer_action = QAction(aqt.mw)
    show_answer_action.setText(MSG[lang]['goBackSide'])
    show_answer_action.setShortcut(HOTKEY['goBackSide'])
    if ANKI_MENU_ICONS:
        show_answer_action.setIcon(PageDown_icon)
    aqt.mw.connect(
        show_answer_action, SIGNAL('triggered()'), go_answer)

    aqt.mw.addon_go_menu.addSeparator()
    aqt.mw.addon_go_menu.addAction(show_question_action)
    aqt.mw.addon_go_menu.addAction(show_answer_action)
    aqt.mw.addon_go_menu.addSeparator()

##

if ZERO_KEY_TO_SHOW_ANSWER:
    # -------------------------------
    # key handler for reviewer window
    # -------------------------------
    def newKeyHandler(self, evt):
        key = evt.key()
        # text = unicode(evt.text())
        Keys0 = [Qt.Key_0, Qt.Key_Insert]  # Show Answer
        if key in Keys0:
            if self.state == 'question':
                go_answer()
            else:
                go_question()
    aqt.reviewer.Reviewer._keyHandler = anki.hooks.wrap(
        aqt.reviewer.Reviewer._keyHandler, newKeyHandler, 'before')

##
