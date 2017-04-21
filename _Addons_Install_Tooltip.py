# -*- mode: Python ; coding: utf-8 -*-
# • Addons Install Tooltip
# https://ankiweb.net/shared/info/1738282325
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 Some hotkeys:
  Check Database...  Ctrl+Delete
  Check Media...  Alt+Shift+Delete
  Empty Cards...  Ctrl+Shift+Delete
  Add-ons Browse and Install...  Ctrl+Shift+Ins

 rated:90:1 will be available with this addon.

 You can enter more than one addon number in install dialog
  with spaces: 1238745 2378903 9875237

 You can add some {{info:...}} stencil in your templates.

 This is a simple monkey patch add-on that inserts day learning cards
 (learning cards with intervals that crossed the day turnover)
 always before new cards without depending due reviews.

 By default Anki do so:
  learning; new if before; due; day learning; new if after
 With this add-on card will be displayed in the following order:
  learning; (day learning; new) if before; due; (day learning; new) if after

 Normally these cards go after due, but I want them to go before new.

 If Tools -> Preferences... -> Basic -> Show new cards before reviews
    learning; day learning; new; due
 If Tools -> Preferences... -> Basic -> Show new cards after reviews
    learning; due; day learning; new

 How to make Anki insensitive case when using {{type:field}}
 Upper case, lower case and {{type:}} /monkey patch/

 You can use it together with
 Multiple type fields on card
 https://ankiweb.net/shared/info/689574440

 Inspired by
 Select Buttons Automatically If Correct Answer, Wrong Answer or Nothing
 https://ankiweb.net/shared/info/2074758752
"""
from __future__ import unicode_literals
from __future__ import division

import anki
import aqt

import aqt.customstudy
import anki.sched  # why?

from anki.collection import _Collection

from anki.consts import *
from aqt.qt import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import os
import re
import unicodedata
import copy
import time
import HTMLParser

# Get language class
# Выбранный пользователем язык программной оболочки
lang = anki.lang.getLang()

MSG = {
    'en': {
        'Cards': _('&Cards'),
        'show_install': _("Show Browse and Install... &Again"),
        'open_ankiweb': _("Open Anki&Web shared add-ons site"),
        'exact': 'type: compare exactly',
        },
    'ru': {
        'Cards': '&Карточки',
        'show_install': "Показывать Обзор и установка... &Снова",
        'open_ankiweb': 'Открыть сайт AnkiWeb с &дополнениями',
        'exact': 'type: точное сравнение при проверке',
        },
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

HOTKEY = {
    'Install': QKeySequence('Ctrl+Shift+Insert'),
    }

install_tooltip = True  # False  #
install_hotkeys = True  # False  #
install_again = False  # True  #
install_menu = True  # False  #

__addon__ = "'" + __name__.replace('_', ' ')
__version__ = "2.0.44a"

##


def timefn(tm):
    str = ''
    if tm >= 60:
        str = anki.utils.fmtTimeSpan(
            (tm / 60) * 60, short=True, point=-1, unit=1)
    if tm % 60 != 0 or not str:
        str += anki.utils.fmtTimeSpan(
            tm % 60, point=2 if not str else -1, short=True)
    return str

# Here are hotkeys for
#  https://github.com/dae/anki/blob/master/designer/main.ui

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
            'info:ord', 'info:did', 'info:due',
            'info:odid', 'info:odue', 'info:cid', 'info:left',
            'info:ivl', 'info:queue', 'info:Reviews', 'info:reps',
            'info:lapses', 'info:flags', 'info:data',
            'info:FirstReview', 'info:LastReview', 'info:TimeAvg',
            'info:TimeTotal', 'info:Young', 'info:Mature',
            'info:type', 'info:nid', 'info:mod', 'info:usn', 'info:factor',
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
            card.did, card.due, card.odid, card.odue, card.id, card.left,
            card.ivl, card.queue, card.reps, card.reps, card.lapses,
            card.flags, card.data])
        (first, last, cnt, total) = self.db.first(
            'select min(id), max(id), count(), sum(time)/1000 ' +
            'from revlog where cid = :cid',
            cid=card.id)
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
        additionalFields += [''] * 28
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


def _getCardReordered(self):
    """
    'Return the next due card id, or None.'

 inspired by Anki user rjgoif
 https://ankiweb.net/shared/info/1810271825
 put ALL due "learning" cards first ×
 ####################################################################
 That is a simple add-on that inserts the daily-learning cards, i.e.
 cards in the learning queue with intervals that crossed the day turnover,
 before starting other reviews (new cards, review cards). \
 Normally these cards go last, but I want them to go first.
 ####################################################################
    """

    # learning card due?
    c = self._getLrnCard()
    if c:
        return c

    # new first, or time for one?
    if self._timeForNewCard():

        # day learning card due?
        c = self._getLrnDayCard()
        if c:
            return c

        c = self._getNewCard()
        if c:
            return c

    # card due for review?
    c = self._getRevCard()
    if c:
        return c

    # day learning card due?
    c = self._getLrnDayCard()
    if c:
        return c

    # new cards left?
    c = self._getNewCard()
    if c:
        return c

    # collapse or finish
    return self._getLrnCard(collapse=True)

anki.sched.Scheduler._getCard = _getCardReordered

#################################################
# • Insensitive case type field

# from Ignore accents in browser search add-on
# https://ankiweb.net/shared/info/1924690148

UPPER_CASE = False
# UPPER_CASE = True

EXACT_COMPARING = False
# EXACT_COMPARING = True


def onExact():
    global EXACT_COMPARING
    EXACT_COMPARING = exact_action.isChecked()


def save_exact():
    aqt.mw.pm.profile['EXACT_COMPARING'] = (
        EXACT_COMPARING)


def load_exact():
    global EXACT_COMPARING, exact_action
    try:
        EXACT_COMPARING = aqt.mw.pm.profile['EXACT_COMPARING']
    except KeyError:
        EXACT_COMPARING = False
    exact_action.setChecked(EXACT_COMPARING)

if install_menu:  # create menu item in Cards
    try:
        aqt.mw.addon_cards_menu
    except AttributeError:
        aqt.mw.addon_cards_menu = QMenu(MSG[lang]['Cards'], aqt.mw)
        aqt.mw.form.menubar.insertMenu(
            aqt.mw.form.menuTools.menuAction(), aqt.mw.addon_cards_menu)

    anki.hooks.addHook("unloadProfile", save_exact)
    anki.hooks.addHook("profileLoaded", load_exact)

    exact_action = QAction(aqt.mw)
    exact_action.setText(MSG[lang]['exact'])
    exact_action.setCheckable(True)
    exact_action.setChecked(EXACT_COMPARING)
    aqt.mw.connect(exact_action, SIGNAL('triggered()'), onExact)
    aqt.mw.addon_cards_menu.addAction(exact_action)

##


def stripCombining(txt):
    """Return txt with all combining characters removed."""
    norm = unicodedata.normalize('NFKD', txt)
    return ''.join([c for c in norm if not unicodedata.combining(c)])


def maTypeAnsAnswerFilter(self, buf):
    # tell webview to call us back with the input content
    self.web.eval('_getTypedText();')
    if not self.typeCorrect:
        return buf
    origSize = len(buf)
    buf = buf.replace('<hr id=answer>', '')
    hadHR = len(buf) != origSize
    # munge correct value
    parser = HTMLParser.HTMLParser()
    cor = anki.utils.stripHTML(
        self.mw.col.media.strip(self.typeCorrect))
    # ensure we don't chomp multiple whitespace
    cor = cor.replace(' ', '&nbsp;')
    cor = parser.unescape(cor)
    cor = cor.replace(u'\xa0', ' ')
    given = self.typedAnswer

    if not EXACT_COMPARING:
        cor = stripCombining(cor)
        given = stripCombining(given)

    # compare with typed answer
    if EXACT_COMPARING:
        res = self.correct(given, cor, showBad=False)
    elif UPPER_CASE:
        res = self.correct(given.strip().upper(),
                           cor.strip().upper(), showBad=False)
    else:
        res = self.correct(given.strip().lower(),
                           cor.strip().lower(), showBad=False)
    # and update the type answer area

    def repl(match):
        # can't pass a string in directly, and can't use re.escape as it
        # escapes too much
        s = """
<span style="font-family: '%s'; font-size: %spx">%s</span>""" % (
            self.typeFont, self.typeSize, res)
        if hadHR:
            # a hack to ensure the q/a separator falls before the answer
            # comparison when user is using {{FrontSide}}
            s = '<hr id=answer>' + s
        return s
    return re.sub(self.typeAnsPat, repl, buf)


def myTypeAnsAnswerFilter(self, buf, i):
    if i >= len(self.typeCorrect):
        return re.sub(self.typeAnsPat, '', buf)
    # tell webview to call us back with the input content
    self.web.eval('_getTypedText(%d);' % i)
    if not self.typeCorrect:
        return buf
    origSize = len(buf)
    buf = buf.replace('<hr id=answer>', '')
    hadHR = len(buf) != origSize
    # munge correct value
    parser = HTMLParser.HTMLParser()
    cor = anki.utils.stripHTML(
        self.mw.col.media.strip(self.typeCorrect[i]))
    # ensure we don't chomp multiple whitespace
    cor = cor.replace(' ', '&nbsp;')
    cor = parser.unescape(cor)
    cor = cor.replace(u'\xa0', ' ')
    given = self.typedAnswer

    if not EXACT_COMPARING:
        cor = stripCombining(cor)
        given = stripCombining(given)

    # compare with typed answer
    if EXACT_COMPARING:
        res = self.correct(given, cor, showBad=False)
    elif UPPER_CASE:
        res = self.correct(given.strip().upper(),
                           cor.strip().upper(), showBad=False)
    else:
        res = self.correct(given.strip().lower(),
                           cor.strip().lower(), showBad=False)
    # and update the type answer area

    def repl(match):
        # can't pass a string in directly, and can't use re.escape as it
        # escapes too much
        s = """
<span style="font-family: '%s'; font-size: %spx">%s</span>""" % (
            self.typeFont, self.typeSize, res)
        if hadHR:
            # a hack to ensure the q/a separator falls before the answer
            # comparison when user is using {{FrontSide}}
            s = '<hr id=answer>' + s
        return s
    buf = re.sub(self.typeAnsPat, repl, buf, 1)
    return self.typeAnsAnswerFilter(buf, i + 1)

if os.path.exists(os.path.join(aqt.mw.pm.addonFolder(),
                  'Multiple_type_fields_on_card.py')):
    aqt.reviewer.Reviewer.typeAnsAnswerFilter = myTypeAnsAnswerFilter
else:
    aqt.reviewer.Reviewer.typeAnsAnswerFilter = maTypeAnsAnswerFilter

##################################################################
# Select_Buttons_Automatically_If_Correct_Answer_Wrong_Answer_or_Nothing.py
# https://ankiweb.net/shared/info/2074758752
# Select Buttons Automatically If Correct Answer, Wrong Answer or Nothing


def maybe_skip_question(self):
    self.typedAnswers = []

aqt.reviewer.Reviewer._showQuestion = anki.hooks.wrap(
    aqt.reviewer.Reviewer._showQuestion, maybe_skip_question)


def maLinkHandler(self, url):

    if ':' in url:
        (cmd, arg) = url.split(':', 1)
    else:
        cmd = url
        arg = ''

    if cmd == 'study':
        my_studyDeck(self, arg)
    elif url.startswith('typeans:'):
        self.typedAnswers.append(unicode(arg))

aqt.reviewer.Reviewer._linkHandler = anki.hooks.wrap(
    aqt.reviewer.Reviewer._linkHandler, maLinkHandler)


def JustDoIt(parm):
    try:
        arg = anki.utils.stripHTML(aqt.mw.col.media.strip(unicode(parm)))
        arg = parm.replace(' ', '&nbsp;')
    except UnicodeDecodeError:
        arg = ''
    # ensure we don't chomp multiple whitespace
    arg = HTMLParser.HTMLParser().unescape(arg)
    return arg  # unicode(arg.replace(u'\xa0', ' ')) #arg


def myDefaultEase(self, _old):
    # if self.mw.reviewer.state == 'question':
    #    return _old(self)
    # tooltip(self.mw.reviewer.state)
    # it's always called on answer side, but three times

    given = ''
    if hasattr(self, 'typedAnswer'):
        if hasattr(self, 'typeCorrect'):
            if self.typeCorrect:  # not None
                if hasattr(self, 'typedAnswers'):

                    self.typedAnswer = JustDoIt(
                        unicode(self.typedAnswer))
                    if not len(self.typedAnswers):
                        gvn = [self.typedAnswer]
                    else:
                        for i in range(len(self.typedAnswers)):
                            self.typedAnswers[i] = JustDoIt(
                                unicode(self.typedAnswers[i]))
                        gvn = self.typedAnswers

                    if not type(self.typeCorrect) is list:
                        self.typeCorrect = JustDoIt(
                            unicode(self.typeCorrect))
                        cor = [self.typeCorrect]
                        # in native Anki it is a string
                    else:
                        for i in range(len(self.typeCorrect)):
                            # <div>Indiana</div>
                            # It happens very often
                            # after unexpected pushing Enter key.
                            self.typeCorrect[i] = JustDoIt(
                                anki.utils.stripHTML(
                                    unicode(self.typeCorrect[i])))
                        cor = self.typeCorrect
                        # with Multiple_type_fields_on_card.py it becomes
                        # a list of strings

                    if (len(gvn) == 0):
                        res = False
                    else:
                        if (len(gvn) > 1 and len(gvn) != len(cor)):
                            res = False
                            # something went wrong
                        else:
                            res = True
                            for i in range(0, len(cor)):

                                if EXACT_COMPARING:
                                    pass
                                elif UPPER_CASE:
                                    gvn[i] = gvn[i].strip().upper()
                                    cor[i] = cor[i].strip().upper()
                                else:
                                    gvn[i] = gvn[i].strip().lower()
                                    cor[i] = cor[i].strip().lower()

                                if not EXACT_COMPARING:
                                    cor[i] = stripCombining(cor[i])
                                    gvn[i] = stripCombining(gvn[i])

                                if (gvn[i] != '' and gvn[i] != cor[i]):
                                    res = False
                                if (gvn[i] != ''):
                                    given += gvn[i]

                    retv = self.mw.col.sched.answerButtons(self.card)
                    if res or given == '':
                        if retv == 4:
                            retv = 3
                        else:
                            retv = 2
                    else:
                        retv = 1
                        """
                        if retv == 4:
                            retv = 2
                        else:
                            retv = 1
                        """
                else:
                    # tooltip ('No typedAnswers')
                    retv = _old(self)
            else:
                    # tooltip ('typeCorrect is None')
                retv = _old(self)
        else:
            # tooltip ('No typeCorrect')
            retv = _old(self)
    else:
        # tooltip ('No typedAnswer')
        retv = _old(self)

    return retv

aqt.reviewer.Reviewer._defaultEase = anki.hooks.wrap(
    aqt.reviewer.Reviewer._defaultEase, myDefaultEase, 'around')
