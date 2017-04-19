# -*- mode: Python ; coding: utf-8 -*-
# • Flip-flop
# https://ankiweb.net/shared/info/519426347
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 -- Flip-flop card (Show FrontSide/BackSide
    by F7/F8 or Ctrl+PgUp/Control+PageDown or ^9/^3 or Insert/0)
"""
from __future__ import division
from __future__ import unicode_literals
import os
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from aqt import mw
import anki.sound
from anki.hooks import wrap
from aqt.reviewer import Reviewer

# Get language class
import anki.lang
lang = anki.lang.getLang()

MSG = {
    'en': {
        'later': _('later'),
        'not now': _('not now'),
        'Cards': _('&Cards'),
        'View': _('&View'),
        'Go': _('&Go'),
        'FrontSide': _("Card's &FrontSide"),
        'BackSide': _("Card's &BackSide"),
        'showFrontSide': _('Show &FrontSide'),
        'showBackSide': _('Show &BackSide'),
        'gotoFrontSide': _('Goto &FrontSide'),
        'gotoBackSide': _('Goto &BackSide'),
        },
    'ru': {
        'later': 'позже',
        'not now': 'не сейчас',
        'Cards': '&Карточки',
        'View': '&Вид',
        'Go': 'П&ереход',
        'FrontSide': '&Лицевая Сторона карточки',
        'BackSide': '&Оборотная Сторона карточки',
        'showFrontSide': 'Показать &Лицевую Сторону',
        'showBackSide': 'Показать &Оборотную Сторону',
        'gotoFrontSide': 'Перейти на &Лицевую Сторону',
        'gotoBackSide': 'Перейти на &Оборотную Сторону',
        },
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

# '&Лицевая Сторона карточки' if lang == 'ru' else _("Card's &FrontSide")
# '&Оборотная Сторона карточки' if lang == 'ru' else _("Card's &BackSide")
# 'Показать &Лицевую Сторону' if lang == 'ru' else _('Show &FrontSide')
# 'Показать &Оборотную Сторону' if lang == 'ru' else _('Show &BackSide')
# 'П&ереход' if lang == 'ru' else _('&Go')
# 'Перейти на &Лицевую Сторону' if lang == 'ru' else _('Goto &FrontSide')
# 'Перейти на &Оборотную Сторону' if lang == 'ru' else _('Goto &BackSide')

HOTKEY = {
    'goto_FrontSide': "Ctrl+PgUp",
    'goto_BackSide': QKeySequence(Qt.CTRL + Qt.Key_PageDown),
    'goto_Backward': QKeySequence('Ctrl+9'),
    'goto_Forward': Qt.CTRL + Qt.Key_3,  # 'Ctrl+3'
    'goto_Q': Qt.Key_F7,
    'goto_A': 'F8',
}

FLIP_FLOP = True
# FLIP_FLOP = False

ANKI_MENU_ICONS = True
# ANKI_MENU_ICONS = False

try:
    MUSTHAVE_COLOR_ICONS = os.path.join(mw.pm.addonFolder(), 'handbook')
except:
    MUSTHAVE_COLOR_ICONS = ''

ZERO_KEY_TO_SHOW_ANSWER = True
# ZERO_KEY_TO_SHOW_ANSWER = False

__addon__ = "'" + __name__.replace('_',' ')
__version__ = "2.0.44a"

if __name__ == '__main__':
    print("This is the _Flip-flop add-on for the Anki program" +
          " and it can't be run directly.")
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2':  # Python 3 is utf8 only already.
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf8')

##


def go_question():
    if mw.state == 'review':
        if mw.reviewer.state == 'answer' or mw.reviewer.state == 'question':
            # refresh FrontSide on PageUp
            anki.sound.stopMplayer()
            mw.reviewer._showQuestion()


def go_answer():
    if mw.state == 'review':
        if mw.reviewer.state == 'question':
            anki.sound.stopMplayer()
            mw.reviewer._showAnswer()

PageUp_icon = QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'PageUp.png'))
PageDown_icon = QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'PageDown.png'))

##

if FLIP_FLOP:

    show_question_auction = QAction(mw)
    show_question_auction.setText(MSG[lang]['FrontSide'])
    show_question_auction.setShortcut(QKeySequence(HOTKEY['goto_FrontSide']))
    if ANKI_MENU_ICONS:
        show_question_auction.setIcon(PageUp_icon)
    mw.connect(show_question_auction, SIGNAL('triggered()'), go_question)

    show_answer_auction = QAction(mw)
    show_answer_auction.setText(MSG[lang]['BackSide'])
    show_answer_auction.setShortcut(HOTKEY['goto_BackSide'])
    if ANKI_MENU_ICONS:
        show_answer_auction.setIcon(PageDown_icon)
    mw.connect(show_answer_auction, SIGNAL('triggered()'), go_answer)

    mw.form.menuEdit.addSeparator()
    mw.form.menuEdit.addAction(show_question_auction)
    mw.form.menuEdit.addAction(show_answer_auction)
    mw.form.menuEdit.addSeparator()

##

try:
    mw.addon_view_menu
except AttributeError:
    mw.addon_view_menu = QMenu(MSG[lang]['View'], mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_view_menu)

mw_addon_view_menu_exists = hasattr(mw, 'addon_view_menu')

if FLIP_FLOP and mw_addon_view_menu_exists:

    show_question_aktion = QAction(mw)
    show_question_aktion.setText(MSG[lang]['showFrontSide'])
    show_question_aktion.setShortcut(HOTKEY['goto_Backward'])
    if ANKI_MENU_ICONS:
        show_question_aktion.setIcon(PageUp_icon)
    mw.connect(show_question_aktion, SIGNAL('triggered()'), go_question)

    show_answer_aktion = QAction(mw)
    show_answer_aktion.setText(MSG[lang]['showBackSide'])
    show_answer_aktion.setShortcut(HOTKEY['goto_Forward'])
    if ANKI_MENU_ICONS:
        show_answer_aktion.setIcon(PageDown_icon)
    mw.connect(show_answer_aktion, SIGNAL('triggered()'), go_answer)

    mw.addon_view_menu.addSeparator()
    mw.addon_view_menu.addAction(show_question_aktion)
    mw.addon_view_menu.addAction(show_answer_aktion)
    mw.addon_view_menu.addSeparator()

##

try:
    mw.addon_go_menu.addSeparator()
except AttributeError:
    mw.addon_go_menu = QMenu(MSG[lang]['Go'], mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_go_menu)

mw_addon_go_menu_exists = hasattr(mw, 'addon_go_menu')

if FLIP_FLOP and mw_addon_go_menu_exists:

    show_question_action = QAction(mw)
    show_question_action.setText(MSG[lang]['gotoFrontSide'])
    show_question_action.setShortcut(HOTKEY['goto_Q'])
    if ANKI_MENU_ICONS:
        show_question_action.setIcon(PageUp_icon)
    mw.connect(
        show_question_action, SIGNAL('triggered()'), go_question)

    show_answer_action = QAction(mw)
    show_answer_action.setText(MSG[lang]['gotoBackSide'])
    show_answer_action.setShortcut(HOTKEY['goto_A'])
    if ANKI_MENU_ICONS:
        show_answer_action.setIcon(PageDown_icon)
    mw.connect(show_answer_action, SIGNAL('triggered()'), go_answer)

    mw.addon_go_menu.addSeparator()
    mw.addon_go_menu.addAction(show_question_action)
    mw.addon_go_menu.addAction(show_answer_action)
    mw.addon_go_menu.addSeparator()

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
    Reviewer._keyHandler = wrap(
        Reviewer._keyHandler, newKeyHandler, 'before')
