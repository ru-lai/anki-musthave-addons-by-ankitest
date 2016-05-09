# -*- mode: Python ; coding: utf-8 -*-
# • Promt and set days interval
# https://ankiweb.net/shared/info/2031109761
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
from __future__ import division
from __future__ import unicode_literals

import os
from aqt import mw
from aqt.utils import tooltip, getText #, showWarning
from anki.hooks import addHook, wrap, runHook

MUSTHAVE_COLOR_ICONS = 'reschedule_icons'
try:
    MUSTHAVE_COLOR_ICONS = os.path.join(mw.pm.addonFolder(), MUSTHAVE_COLOR_ICONS)
except:
    MUSTHAVE_COLOR_ICONS = ''

import anki.lang
lang = anki.lang.getLang()

from PyQt4.QtGui import *
from PyQt4.QtCore import *

HOTKEY = {      # in mw Main Window (Reviewer)
    'F2_ctrl'   : ["Ctrl+Alt+Space"],  
}

# inspired by
# Date:     January 27, 2016
# Author:   Benjamin Gray
# File:     Quick_Reschedule.py
# Purpose:  Quickly reschedule cards in anki to a user specified interval using sched.reschedCards()

import random

# prompt for new interval, and set it
def promptNewInterval():
    if mw.state != 'review':
        tooltip("Задавать дни до следующего просмотра можно только при просмотре карточек!" if lang=='ru' else \
            'Prompt for new interval available only on answer side (BackSide) of card\'s reviewer.')
    else:
        suffix = ''
        days = unicode(mw.reviewer.card.ivl+1)
        dayString = getText((u"Дней до следующего просмотра карточки (текущий интервал + 1 = %s ):" \
            if lang=='ru' else \
            "Number of days until next review (current interval + 1 = %s ):") % (days), default=days)
        if dayString[1]:
            dayString0 = dayString[0].strip().lower()
            dayStringM = False
            dayStringW = False
            dayStringI = False
            if dayString0.endswith('m') or dayString0.endswith(u'м'):
                dayString0 = dayString0[:-1].strip()
                dayStringM = True
            if dayString0.endswith('w') or dayString0.endswith(u'н'):
                dayString0 = dayString0[:-1].strip()
                dayStringW = True
            if dayString0.endswith('d') or dayString0.endswith(u'д'):
                dayString0 = dayString0[:-1].strip()
            if len(dayString0)==0:
                dayString0 = '1'

            try:
                days = int(dayString0)
                dayz = float(0)
                if dayStringM:
                    dayz = abs(float(days))
                    days = 0
                if dayStringW:
                    dayz = float(0)
                    days = abs(days) * 7
                if days < 0:
                    dayStringI = True
            except ValueError:
                days = mw.reviewer.card.ivl+1
                try:
                    dayz = abs(float(dayString0))
                    if 0<dayz and dayz<1:
                        days = int(dayz*10) * 7
                        dayz = 0
                        dayStringW = True
                    else:
                        days = 0
                        dayStringM = True
                except ValueError:
                    dayz = float(0)

            if dayz > 0: # 3.1 or 1.2 is monthes
                suffix = '&plusmn;15'
                days = int(31*dayz)+random.randrange(-15, 15+1, 1)
            elif dayStringW: # .2 is two weeks
                suffix = '&plusmn;3'
                days = abs(days)+random.randrange(-3, 3+1, 1)
            elif days > 10:
                suffix = '&plusmn;1'
                days = days + random.randrange(-1, 1+1, 1)
            elif days > 0: # from 1 to 9 setup exact number of day
                suffix = ''
                pass # days = days 
            elif days <= 0:
                suffix = ''
                days = mw.reviewer.card.ivl+1
                #days = days * 60 # num<0 == interval in seconds

            #showWarning(unicode(dayString)+' '+str(dayz)+' '+str(days))

            mw.checkpoint(_("Reschedule card"))

            mw.col.sched.reschedCards( [mw.reviewer.card.id], days-1 if days>1 else 1, days+1 )

            days_mod = (days % 10) if ( (days%100) < 11 or (days%100) > 14) else (days % 100)
            tooltip( (u"Запланирован просмотр через <b>%s</b> %s "+\
                ("день" if days_mod==1 else ("дня" if days_mod>=2 and days_mod<=4 else "дней")) if lang=='ru' else \
                'Rescheduled for review in <b>%s</b> %s days') % \
                (days, ' (%s%s) '%(dayString[0],suffix) if len(suffix) else '') )

            mw.reset()

if True:
    try:
        mw.addon_cards_menu
    except AttributeError:
        mw.addon_cards_menu = QMenu(_(u"&Карточки") if lang == 'ru' else _(u"&Cards"), mw)
        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(), mw.addon_cards_menu)

    set_new_int_action = QAction(mw)
    set_new_int_action.setText(u'&Через ... дней' if lang=='ru' else _(u"&Prompt and Set ... days interval"))
    set_new_int_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'schedule.png')))
    set_new_int_action.setShortcut(QKeySequence(HOTKEY['F2_ctrl'][0]))
    set_new_int_action.setEnabled(False)
    mw.connect(set_new_int_action, SIGNAL("triggered()"), promptNewInterval)

    if hasattr(mw,'addon_cards_menu'):
        mw.addon_cards_menu.addAction(set_new_int_action)
        mw.addon_cards_menu.addSeparator()

    def edit_actions_off():
        set_new_int_action.setEnabled(False)
    def edit_actions_on():
        set_new_int_action.setEnabled(True)
    mw.deckBrowser.show = wrap(mw.deckBrowser.show, edit_actions_off)
    mw.overview.show = wrap(mw.overview.show, edit_actions_off)
    mw.reviewer.show = wrap(mw.reviewer.show, edit_actions_on)

