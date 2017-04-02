# -*- mode: Python ; coding: utf-8 -*-
# ' Addons Install Tooltip
#
# You can add some {{info:...}} stencil in your templates.
#
# https://ankiweb.net/shared/info/1738282325
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2017 Dmitry Mikheev, http://finpapa.ucoz.ru/index.html
# No support. Use it AS IS on your own risk.
from __future__ import unicode_literals
from __future__ import division

import anki
import aqt

import aqt.customstudy

from anki.consts import *
from aqt.qt import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *

install_tooltip = True  # False  #
install_hotkeys = True  # False  #
install_again = False  # True  #
install_menu = True  # False  #

import copy
import time
from anki.collection import _Collection

def timefn(tm):
    str = ''
    if tm >= 60:
        str = anki.utils.fmtTimeSpan((tm / 60) * 60, short=True, point=-1, unit=1)
    if tm % 60 != 0 or not str:
        str += anki.utils.fmtTimeSpan(tm % 60, point=2 if not str else -1, short=True)
    return str

# Get language class
# Выбранный пользователем язык программной оболочки
lang = anki.lang.getLang()

MSG = {
    'en': {
        'show_install': _("Show Browse and Install... &Again"),
        'open_ankiweb': _("Open Anki&Web shared add-ons site"),
        },
    'ru': {
        'show_install': "Показывать Обзор и установка... &Снова",
        'open_ankiweb': 'Открыть сайт AnkiWeb с &дополнениями',
        },
    'es': {
        'show_install': "Ver el Examen y la instalación... de &Nuevo",
        'open_ankiweb': 'Abrir el sitio de Anki&Web, con las complementos',
        },
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

HOTKEY = {
    'Install': QKeySequence('Ctrl+Shift+Insert'),
    }

# Here are hotkeys for https://github.com/dae/anki/blob/master/designer/main.ui

aqt.mw.form.actionFullDatabaseCheck.setShortcut(
    QKeySequence('Ctrl+Delete'))  # Check Database...

aqt.mw.form.actionCheckMediaDatabase.setShortcut(
    QKeySequence('Alt+Shift+Delete'))  # Check Media...

aqt.mw.form.actionEmptyCards.setShortcut(
    QKeySequence('Ctrl+Shift+Delete'))  # Empty Cards...


# anki-master\aqt\addons.py
#  Monkey Patching
#   showInfo -> tooltip
def _accept1(self):
    # go_AnkiWeb_addons()
    # This way starts after dialog window were closed, not before.

    QDialog.accept(self)
    # create downloader thread

    txt = self.form.code.text().split()
    for x in txt:
        ret = aqt.downloader.download(self.mw, x)
        if not ret:
            return
        data, fname = ret
        self.mw.addonManager.install(data, fname)
        self.mw.progress.finish()

    aqt.utils.tooltip(
        _("Download successful. Please restart Anki."),
        period=3000)

    if install_again:
        aqt.addons.AddonManager.onGetAddons(self.mw.addonManager)

if install_tooltip:
    aqt.addons.GetAddons.accept = _accept1

# hotkeys

if install_hotkeys:
    aqt.mw.form.actionDownloadSharedPlugin.setShortcut(HOTKEY['Install'])


# menu
def go_AnkiWeb_addons():
    aqt.utils.openLink("https://ankiweb.net/shared/addons/")


def toggle_install_again():
    global install_again
    install_again = show_install_again_action.isChecked()

    aqt.addons.AddonManager.onGetAddons(aqt.mw.addonManager)

show_install_again_action = QAction(aqt.mw)
show_install_again_action.setText(MSG[lang]['show_install'])
show_install_again_action.setCheckable(True)
show_install_again_action.setChecked(install_again)
aqt.mw.connect(show_install_again_action, SIGNAL("triggered()"),
               toggle_install_again)


def save_install_again():
    aqt.mw.pm.profile['addons_install_again'] = (
        show_install_again_action.isChecked())


def load_install_again():
    global install_again, show_install_again_action
    try:
        install_again = aqt.mw.pm.profile['addons_install_again']
    except KeyError:
        install_again = False
    show_install_again_action.setChecked(install_again)

if install_menu:
    anki.hooks.addHook("unloadProfile", save_install_again)
    anki.hooks.addHook("profileLoaded", load_install_again)

    aqt.mw.form.menuPlugins.insertAction(aqt.mw.form.actionOpenPluginFolder,
                                         show_install_again_action)

    open_ankiweb_shared_action = QAction(aqt.mw)
    open_ankiweb_shared_action.setText(MSG[lang]['open_ankiweb'])
    aqt.mw.connect(open_ankiweb_shared_action, SIGNAL("triggered()"),
                   go_AnkiWeb_addons)
    aqt.mw.form.menuPlugins.insertAction(aqt.mw.form.actionOpenPluginFolder,
                                         open_ankiweb_shared_action)

else:
    install_again = False

# menuPlugins
# designer/main.ui

# Browse & Install...
# <string>Browse &amp;&amp; Install...</string>
# actionDownloadSharedPlugin

# <string>&amp;Open Add-ons Folder...</string>
# actionOpenPluginFolder

##############################################################
# rated:30:1
# https://anki.tenderapp.com/discussions/add-ons/9032-rated301

# RADIO_FORGOT: 30 -> 36500

# aqt/customstudy.py
# Copyright: Damien Elmes <anki@ichi2.net>

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
    f = self.form
    sp = f.spin
    smin = 1
    smax = DYN_MAX_SIZE
    sval = 1
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
        # tit = _("After pressing OK, you can choose which tags to include.")
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

##

_old_renderQA = _Collection._renderQA


def _renderQA(self, data, qfmt=None, afmt=None):
    origFieldMap = self.models.fieldMap
    model = self.models.get(data[2])
    if data[0] is None:
        card = None
    elif data[0] == 1:
        card = None
    else:
        try:
            card = self.getCard(data[0])
        except:
            card = None

    def tmpFieldMap(m):
        """Mapping of field name -> (ord, field)."""
        d = dict((f['name'], (f['ord'], f)) for f in m['flds'])
        newFields = [
            'info:Ord', 'info:Did', 'info:Due', 'info:Id',
            'info:Ivl', 'info:Queue', 'info:Reviews', 'info:Lapses',
            'info:FirstReview', 'info:LastReview', 'info:TimeAvg',
            'info:TimeTotal', 'info:Young', 'info:Mature', 'info:CardType',
            'info:Nid', 'info:Mod', 'info:Usn', 'info:Factor',
            'info:New', 'info:Learning', 'info:dayLearning', 'info:Review',
        ]
        for i, f in enumerate(newFields):
            d[f] = (len(m['flds']) + i, 0)
        return d
    self.models.fieldMap = tmpFieldMap
    origdata = copy.copy(data)
    data[6] += '\x1f'
    additionalFields = [str(data[4])]
    if card is not None:
        additionalFields += map(str, [
            card.did, card.due, card.id,
            card.ivl, card.queue, card.reps, card.lapses])
        (first, last, cnt, total) = self.db.first(
            'select min(id), max(id), count(), sum(time)/1000 ' +
            'from revlog where cid = :id',
            id=card.id)
        if cnt:
            additionalFields.append(time.strftime(
                '%Y-%m-%d', time.localtime(first / 1000)))
            additionalFields.append(time.strftime(
                '%Y-%m-%d', time.localtime(last / 1000)))
            additionalFields.append(timefn(total / float(cnt)))
            additionalFields.append(timefn(total))
        else:
            additionalFields += [''] * 4
        if card.type == 2 and card.ivl < 21:
            additionalFields += [_('Young')]
        else:
            additionalFields += ['']
        if card.type == 2 and card.ivl > 20:
            additionalFields += [_('Mature')]
        else:
            additionalFields += ['']
        additionalFields += [str(card.type)]
        additionalFields += [str(card.nid)]
        # additionalFields += [str(card.mod)]
        additionalFields.append(time.strftime(
            '%Y-%m-%d', time.localtime(card.mod)))
        additionalFields += [str(card.usn)]
        additionalFields += [str(card.factor)]
        if card.type == 0:
            additionalFields += [_('New')]
        else:
            additionalFields += ['']
        if card.type == 1:
            additionalFields += [_('Learn')]
        else:
            additionalFields += ['']
        if card.type == 1 and card.queue == 3:
            additionalFields += [_('Learning')]
        else:
            additionalFields += ['']
        if card.type == 2:
            additionalFields += [_('Review')]
        else:
            additionalFields += ['']
    else:
        additionalFields += [''] * 22
    data[6] += '\x1f'.join(additionalFields)

    result = _old_renderQA(self, data, qfmt=qfmt, afmt=afmt)

    data = origdata
    self.models.fieldMap = origFieldMap
    return result

##

_Collection._renderQA = _renderQA


def previewCards(self, note, type=0):
    existingTemplates = {c.template()[u'name']: c for c in note.cards()}
    if type == 0:
        cms = self.findTemplates(note)
    elif type == 1:
        cms = [c.template().name() for c in note.cards()]
    else:
        cms = note.model()['tmpls']
    if not cms:
        return []
    cards = []
    for template in cms:
        if template[u'name'] in existingTemplates:
            card = existingTemplates[template[u'name']]
        else:
            card = self._newCard(note, template, 1, flush=False)
        cards.append(card)
    return cards

_Collection.previewCards = previewCards
