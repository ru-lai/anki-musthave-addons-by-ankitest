# -*- mode: Python ; coding: utf-8 -*-
# • Promt and set days interval
# https://ankiweb.net/shared/info/2031109761
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# new interval equals current interval
#  plus + Number of days until next review (because no answer will be given).
#
# No support. Use it AS IS on your own risk.
from __future__ import division
from __future__ import unicode_literals
import os
import sys
import datetime
import random

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from anki.utils import intTime
from anki.hooks import addHook, wrap, runHook
from aqt import mw, browser
from aqt.utils import tooltip, getText, showInfo

import anki.lang
lang = anki.lang.getLang()

HOTKEY = {      # in mw Main Window (Reviewer)
    'F2_ctrl': ['Alt+Shift+Space'],
}

if __name__ == '__main__':
    print("This is _Swap add-on for the Anki program " +
          "and it can't be run directly.")
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2':  # Python 3 is utf8 only already.
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf8')

MUSTHAVE_COLOR_ICONS = 'handbook'
try:
    MUSTHAVE_COLOR_ICONS = os.path.join(
        mw.pm.addonFolder(), MUSTHAVE_COLOR_ICONS)
except:
    MUSTHAVE_COLOR_ICONS = ''


def _reschedCards(self, ids, imin, imax, indi=2500):
    'Put cards in review queue with a new interval in days (min, max).'
    d = []
    t = self.today
    mod = intTime()
    for id in ids:
        r = random.randint(imin, imax)
        d.append(dict(id=id, due=r + t, ivl=max(1, r), mod=mod,
                      usn=self.col.usn(), fact=indi))
    self.remFromDyn(ids)
    self.col.db.executemany("""
update cards set type=2,queue=2,ivl=:ivl,due=:due,odue=0,
usn=:usn,mod=:mod,factor=:fact where id=:id""", d)
    self.col.log(ids)

def _refactorCards(self, ids, indi=2500):
    'Put cards in review queue with a new interval in days (min, max).'
    d = []
    mod = intTime()
    for id in ids:
        d.append(dict(id=id, mod=mod,
                      usn=self.col.usn(), fact=indi))
    self.remFromDyn(ids)
    self.col.db.executemany("""
update cards set queue=2,odue=0,
usn=:usn,mod=:mod,factor=:fact where id=:id and type=2""", d)
    self.col.log(ids)

def _nofactorCards(self, ids, imin, imax):
    'Put cards in review queue with a new interval in days (min, max).'
    d = []
    t = self.today
    mod = intTime()
    for id in ids:
        r = random.randint(imin, imax)
        d.append(dict(id=id, due=r + t, ivl=max(1, r), mod=mod,
                      usn=self.col.usn()))
    self.remFromDyn(ids)
    self.col.db.executemany("""
update cards set type=2,queue=2,ivl=:ivl,due=:due,odue=0,
usn=:usn,mod=:mod where id=:id""", d)
    self.col.log(ids)

# inspired by
# Date:     January 27, 2016
# Author:   Benjamin Gray
# File:     Quick_Reschedule.py
# Purpose:  Quickly reschedule cards in anki to a user specified interval
# using sched.reschedCards()

# prompt for new interval, and set it


def promptNewInterval(cids):
    '''
    if mw.state != 'review':
        tooltip(
            'Задавать дни до следующего просмотра можно ' +
            'только при просмотре карточек!' if lang=='ru' else
            'Prompt for new interval available only on answer side ' +
            '(BackSide) of card\'s reviewer.')
        return
    '''
    if cids is None:
        cids = [mw.reviewer.card.id]
    SWAP_TAG = False
    cardEase = None
    infotip = ''
    prefix = ''
    suffix = ''
    total = 0
    dayz = float(0)
    try:
        days = unicode(mw.reviewer.card.ivl + 1)
    except AttributeError:
        days = u'1'
    dayString = getText(
        ('Дней до следующего просмотра карточки ' +
         '(текущий интервал + 1 = %s ):' if lang == 'ru' else
         'Number of days until next review ' +
         '(current interval + 1 = %s ):') % (days), default=days)

    stringY = False
    stringM = False
    stringW = False
    stringD = False

    if dayString[1]:
        daysList = dayString[0].strip().lower().split()
        for nextWord in daysList:
            nextDate = nextWord.strip()
            if len(nextDate) == 0:
                continue

            dayStringY = False
            dayStringM = False
            dayStringW = False
            dayStringD = False

            if nextDate.endswith('y') or nextDate.endswith(u'г'):
                nextDate = nextDate[:-1].strip()
                dayStringY = True
                stringY = True
            if nextDate.endswith('m') or nextDate.endswith(u'м'):
                nextDate = nextDate[:-1].strip()
                dayStringM = True
                stringM = True
            if nextDate.endswith('w') or nextDate.endswith(u'н'):
                nextDate = nextDate[:-1].strip()
                dayStringW = True
                stringW = True
            if nextDate.endswith('d') or nextDate.endswith(u'д'):
                nextDate = nextDate[:-1].strip()
                dayStringD = True
                stringD = True
            if len(nextDate) == 0:
                nextDate = '1'
                dayStringD = True
                stringD = True

            if nextDate.endswith('%'):
                nextDate = nextDate[:-1].strip()
                if nextDate == '':
                    nextDate = '250'
                try:
                    cardEase = max(130, abs(int(nextDate)))
                except ValueError:
                    cardEase = 130
            else:
                prefix += nextWord + ' '
                try:
                    dayz = float(0)
                    days = int(nextDate)
                    if dayStringM:
                        dayz = abs(float(days))
                        days = 0
                    if dayStringY:
                        dayz = abs(float(days)) * 12.0
                        days = 0
                        dayStringM = True
                    if dayStringW:
                        days = abs(days) * 7
                except ValueError:
                    days = 1  # mw.reviewer.card.ivl + 1
                    try:
                        dayz = abs(float(nextDate))
                        if 0 < dayz and dayz < 1:
                            days = int(dayz * 10) * 7
                            dayz = float(0)
                            dayStringW = True
                            stringW = True
                        else:
                            days = 0
                            dayStringM = True
                            stringM = True
                            if dayStringY:
                                dayz = dayz * 12.0
                    except ValueError:
                        dayz = float(0)

                if dayStringM:
                    total += int(30 * abs(dayz))
                else:
                    total += abs(days)

        mw.checkpoint(_('Reschedule card'))

        days = total

        if stringD or (not stringD and not stringW and not stringM):
            if days > 9:
                suffix = '&plusmn;1'
                total = days + random.randrange(-1, 1 + 1, 1)
            else:  # from 1 to 9 setup exact number of day
                suffix = ''
                total = days  # days = days
        elif stringW:  # .2 is two weeks
            suffix = '&plusmn;3'
            total = abs(days) + random.randrange(-3, 3 + 1, 1)
        elif stringM:  # 3.1 or 1.2 is monthes
            suffix = '&plusmn;15'
            total = abs(days) + random.randrange(-15, 15 + 1, 1)

        if cardEase is None:
            if not total:  # empty request line == drop cards to new queue
                mw.col.sched.forgetCards(cids)
                mw.reset()
                return
            infotip = ''
            # try:
            #     cardEase = mw.reviewer.card.factor  # 2500
            # except AttributeError:
            #     cardEase = 2500
        else:
            infotip = ('Лёгкость карточки <b>%s</b>%%<br><br>'
                       if lang == 'ru' else
                       'Card ease <b>%s</b>%%<br><br>') % (cardEase)
            cardEase *= 10

        if total:
            # mw.col.sched.reschedCards(
            #   [mw.reviewer.card.id], total-1 if total>1 else 1, total+1 )
            if cardEase is not None:
                if total < 10:
                    _reschedCards(
                        mw.col.sched, cids, total, total, indi=cardEase)
                else:
                    _reschedCards(
                        mw.col.sched, cids, total -
                        1 if total > 1 else 1, total + 1, indi=cardEase)
            else:
                if total < 10:
                    _nofactorCards(
                        mw.col.sched, cids, total, total)
                else:
                    _nofactorCards(
                        mw.col.sched, cids, total -
                        1 if total > 1 else 1, total + 1)

            days_mod = (total % 10) if ((total % 100) < 11 or (
                total % 100) > 14) else (total % 100)
            tooltip(
                infotip + (
                    'Запланирован просмотр через <b>%s</b> %s ' +
                    ('день' if days_mod == 1 else (
                        'дня' if days_mod >= 2 and
                        days_mod <= 4 else 'дней'))
                    if lang == 'ru' else
                    'Rescheduled for review in <b>%s</b> %s days') % (
                        total, ' ( <b style="color:#666;">%s</b> %s ) ' %
                        (prefix.strip(), suffix) if len(suffix) else ''),
                period=2000)

            # SWAP_TAG = datetime.datetime.now().strftime(
            #   'rescheduled::re-%Y-%m-%d::re-card')
            # SWAP_TAG = datetime.datetime.now().strftime(
            #   're-%y-%m-%d-c')
            if SWAP_TAG:
                SWAP_TAG += unicode(mw.reviewer.card.ord + 1)
                note = mw.reviewer.card.note()
                if not note.hasTag(SWAP_TAG):
                    note.addTag(SWAP_TAG)
                    note.flush()  # never forget to flush

        elif cardEase is not None:
            tooltip((
                'Лёгкость карточки <b>%s</b>%%<br><br>'
                if lang == 'ru' else
                'Card ease <b>%s</b>%%<br><br>') %
                int(cardEase / 10), period=2000)
            _refactorCards(mw.col.sched, cids, indi=cardEase)
            # mw.reviewer.card.factor = cardEase
            # mw.reviewer.card.flush()

        mw.reset()

if True:
    try:
        mw.addon_cards_menu
    except AttributeError:
        mw.addon_cards_menu = QMenu(
            _(u'&Карточки') if lang == 'ru' else _(u'&Cards'), mw)
        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(), mw.addon_cards_menu)

    set_new_int_action = QAction(mw)
    set_new_int_action.setText(u'&Через ... дней' if lang == 'ru' else _(
        u'&Prompt and Set ... days interval'))
    set_new_int_action.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'schedule.png')))
    set_new_int_action.setShortcut(QKeySequence(HOTKEY['F2_ctrl'][0]))
    set_new_int_action.setEnabled(False)
    mw.connect(set_new_int_action, SIGNAL('triggered()'),
               lambda: promptNewInterval(None))

    if hasattr(mw, 'addon_cards_menu'):
        mw.addon_cards_menu.addAction(set_new_int_action)
        mw.addon_cards_menu.addSeparator()

    def edit_actions_off():
        set_new_int_action.setEnabled(False)

    def edit_actions_on():
        set_new_int_action.setEnabled(True)
    mw.deckBrowser.show = wrap(mw.deckBrowser.show, edit_actions_off)
    mw.overview.show = wrap(mw.overview.show, edit_actions_off)
    mw.reviewer.show = wrap(mw.reviewer.show, edit_actions_on)

# reset_card_scheduling.py
# https://ankiweb.net/shared/info/1432861881
# Reset card(s) scheduling information / progress
#######################################################

# Col is a collection of cards, cids are the ids of the cards to reset.


def resetSelectedCardScheduling(self):
    """
    Resets statistics for selected cards,
    and removes them from learning queues.
    """
    cids = self.selectedCards()
    if not cids:
        return
    # Allow undo
    self.mw.checkpoint(_('Promt and set days interval'))
    self.mw.progress.start(immediate=True)
    # Not sure if beginReset is required
    self.model.beginReset()

    # Resets selected cards in current collection
    # self.col.sched.resetCards(cids)
    # Removes card from dynamic deck?
    # self.col.sched.remFromDyn(cids)
    # Removes card from learning queues
    # self.col.sched.removeLrn(cids)

    promptNewInterval(cids=cids)

    self.model.endReset()
    self.mw.progress.finish()
    # Update the main UI window to reflect changes in card status
    self.mw.reset()


def addMenuItem(self):
    """ Adds hook to the Edit menu in the note browser """
    newInt_action = QAction('Promt and set days interval', self)
    newInt_action.setShortcut(QKeySequence(HOTKEY['F2_ctrl'][0]))
    self.resetSelectedCardScheduling = resetSelectedCardScheduling
    self.connect(newInt_action, SIGNAL('triggered()'),
                 lambda s=self: resetSelectedCardScheduling(self))
    self.form.menuEdit.addAction(newInt_action)

# Add-in hook; called by the AQT Browser object when it is ready for the
# add-on to modify the menus
addHook('browser.setupMenus', addMenuItem)
