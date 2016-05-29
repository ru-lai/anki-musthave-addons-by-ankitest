# -*- coding: utf-8 -*-
# ~ Clear Fields Formatting HTML
# https://ankiweb.net/shared/info/1114708966
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#  Made by request:
#   Clear Field Formatting (HTML) in Bulk needs improvement
#    https://anki.tenderapp.com/discussions/add-ons/
#    7526-clear-field-formatting-html-in-bulk-needs-improvement
# Based on
# https://ankiweb.net/shared/info/728131107
# Removes the field formatting of all selected notes.
# Author: xelif@icqmail.com
#
from __future__ import division
from __future__ import unicode_literals
import os
import sys
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import aqt.deckbrowser
import aqt.editor
from aqt.utils import showText, tooltip

from anki.hooks import addHook, wrap, runHook
from aqt import mw

# Get language class
import anki.lang
lang = anki.lang.getLang()

HOTKEY = {      # workds in card Browser, card Reviewer and note Editor (Add?)
    'clear':    ['Ctrl+F12', '', '', ''' ''', """ """],
    'full':     ['Ctrl+Shift+F12', '', '', ''' ''', """ """],
    'brdiv':    ['Alt+Shift+F12', '', '', ''' ''', """ """],
}

##

if __name__ == '__main__':
    print("""This is _Clear_Fields_Formatting_HTML.py add-on \
for the Anki program and it can't be run directly.""")
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2':  # Python 3 is utf8 only already.
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf8')

##


def stripFormatting(txt, imgbr, divbr):
    """
    Removes all html tags, except if they begin like this:
        <img...> <br...> <div > </div>
    This allows inserted images and line breaks to remain.

    Parameters
    ----------
    txt : string
        the string containing the html tags to be filtered
    Returns
    -------
    string
        the modified string as described above

    # if result != field:
    #     sys.stderr.write('Changed: \"' + field
    #                      + '\' ==> \"' + result + '\"')
    """
    if not txt:
        return ''
    result = re.sub(
        imgbr, '',
        re.sub(
            divbr, '\n',
            re.sub('<div.*?>', '<div>', txt)
            )
        )
    return result


def clearFormatting(self, nids=None, dids=None, note=None,
                      removeTags='', newlineTags=''):
    """
    Clears the formatting for every selected note.
    Also creates a restore point, allowing a single undo operation.

    Parameters
    ----------
    self : Browser
        the anki self from which the function is called
    """
    mw.checkpoint('Clear Fields Formatting HTML')
    mw.progress.start()

    if dids:
        nids = []
        for did in dids:
            deck = self.mw.col.decks.nameOrNone(did)
            query = 'deck:"%s"' % (deck)
            nids.extend(self.mw.col.findNotes(query))

    if nids:
        for nid in nids:  # self.selectedNotes():
            note = mw.col.getNote(nid)
            note.fields = map(
                lambda x: stripFormatting(x, removeTags, newlineTags),
                note.fields)
            note.flush()
    elif note:
        note.fields = map(
            lambda x: stripFormatting(x, removeTags, newlineTags),
            note.fields)
        note.flush()

    mw.progress.finish()
    if mw.state == 'review':
        rst = mw.reviewer.state
    else:
        rst = None
    mw.reset()
    if rst == 'answer':
        mw.reviewer._showAnswerHack()
    tooltip('Clear Fields Formatting HTML done.', period=1500)


def onClearFormat(self, nids=None, dids=None, note=None):
    clearFormatting(
        self, nids=nids, dids=dids, note=note,
        removeTags='<(?!img|br|div|/div).*?>',
        newlineTags='(^$)')


def onClearFormatting(self, nids=None, dids=None, note=None):
    clearFormatting(
        self, nids=nids, dids=dids, note=note,
        removeTags='<(?!img).*?>',
        newlineTags='</div><div>|</div>|<div>|<br />')


def onClearFormatted(self, nids=None, dids=None, note=None):
    clearFormatting(
        self, nids=nids, dids=dids, note=note,
        removeTags='</div><div>|</div>|<div>|<br />',
        newlineTags='(^$)')
        # надо заменять на пробел, а не просто удалять
        # ну и неплохо сначала div заменять на span


def setupMenu(self):
    """
    Add the items to the browser menu Edit
    """
    try:
        self.form.addon_notes_menu
    except AttributeError:
        self.form.addon_notes_menu = QMenu(
            _(u'&Записи') if lang == 'ru' else _(u'&Notes'), mw)
        self.form.menubar.insertMenu(
            self.form.menu_Help.menuAction(), self.form.addon_notes_menu)

    # self.form.menuEdit.addSeparator()
    self.form.addon_notes_menu.addSeparator()

    a = QAction(_('Clear Fields Formatting HTML (remain new lines)'), self)
    a.setShortcut(QKeySequence(HOTKEY['clear'][0]))
    self.connect(a, SIGNAL('triggered()'),
                 lambda e=self: onClearFormat(e, nids=e.selectedNotes()))
    self.form.addon_notes_menu.addAction(a)

    b = QAction(_('Clear Fields Formatting HTML (at all)'), self)
    b.setShortcut(QKeySequence(HOTKEY['full'][0]))
    self.connect(b, SIGNAL('triggered()'),
                 lambda e=self: onClearFormatting(e, nids=e.selectedNotes()))
    self.form.addon_notes_menu.addAction(b)

    c = QAction(_('Clear Fields Format HTML (remove new lines only)'), self)
    c.setShortcut(QKeySequence(HOTKEY['brdiv'][0]))
    self.connect(c, SIGNAL('triggered()'),
                 lambda e=self: onClearFormatted(e, nids=e.selectedNotes()))
    self.form.addon_notes_menu.addAction(c)

    self.form.addon_notes_menu.addSeparator()

addHook('browser.setupMenus', setupMenu)

# Options
##########################################################################


def showOptions(self, did):
    m = QMenu(self.mw)
    a = m.addAction(_("Rename"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._rename(did))
    a = m.addAction(_("Options"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._options(did))
    a = m.addAction(_("Export"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._export(did))
    a = m.addAction(_("Delete"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._delete(did))
    #
    runHook("deckHooker", self, did, m)
    #
    m.exec_(QCursor.pos())

aqt.deckbrowser.DeckBrowser._showOptions = showOptions


def deckHooker(self, did, m):
    m.addSeparator()

    a = m.addAction(_('Clear Fields Formatting HTML (remain new lines)'))
    a.connect(a, SIGNAL("triggered()"), lambda e=self, did=did:
              onClearFormat(e, dids=[did]))

    a = m.addAction(_('Clear Fields Formatting HTML (at all)'))
    a.connect(a, SIGNAL("triggered()"), lambda e=self, did=did:
              onClearFormatting(e, dids=[did]))

    a = m.addAction(_('Clear Fields Format HTML (remove new lines only)'))
    a.connect(a, SIGNAL("triggered()"), lambda e=self, did=did:
              onClearFormatted(e, dids=[did]))

    m.addSeparator()

addHook('deckHooker', deckHooker)

# Advanced menu
######################################################################


def onAdvanced(self):
    m = QMenu(self.mw)
    a = m.addAction(_("LaTeX"))
    a.setShortcut(QKeySequence("Ctrl+T, T"))
    a.connect(a, SIGNAL("triggered()"), self.insertLatex)
    a = m.addAction(_("LaTeX equation"))
    a.setShortcut(QKeySequence("Ctrl+T, E"))
    a.connect(a, SIGNAL("triggered()"), self.insertLatexEqn)
    a = m.addAction(_("LaTeX math env."))
    a.setShortcut(QKeySequence("Ctrl+T, M"))
    a.connect(a, SIGNAL("triggered()"), self.insertLatexMathEnv)
    a = m.addAction(_("Edit HTML"))
    a.setShortcut(QKeySequence("Ctrl+Shift+X"))
    a.connect(a, SIGNAL("triggered()"), self.onHtmlEdit)

    m.addSeparator()

    a = m.addAction(_('Clear Fields Formatting HTML (remain new lines)'))
    # a.setShortcut(QKeySequence(HOTKEY['clear'][0]))
    a.connect(a, SIGNAL("triggered()"), lambda e=self:
              onClearFormat(e, note=self.note))

    a = m.addAction(_('Clear Fields Formatting HTML (at all)'))
    # a.setShortcut(QKeySequence(HOTKEY['full'][0]))
    a.connect(a, SIGNAL("triggered()"), lambda e=self:
              onClearFormatting(e, note=self.note))

    a = m.addAction(_('Clear Fields Format HTML (remove new lines only)'))
    # a.setShortcut(QKeySequence(HOTKEY['brdiv'][0]))
    a.connect(a, SIGNAL("triggered()"), lambda e=self:
              onClearFormatted(e, note=self.note))

    m.addSeparator()

    m.exec_(QCursor.pos())

aqt.editor.Editor.onAdvanced = onAdvanced

##

aa = QAction(_('Clear Fields Formatting HTML (remain new lines)'), mw)
aa.setShortcut(QKeySequence(HOTKEY['clear'][0]))
mw.connect(aa, SIGNAL('triggered()'), lambda e=mw:
           onClearFormat(e, nids=[e.reviewer.card.nid]))

bb = QAction(_('Clear Fields Formatting HTML (at all)'), mw)
bb.setShortcut(QKeySequence(HOTKEY['full'][0]))
mw.connect(bb, SIGNAL('triggered()'), lambda e=mw:
           onClearFormatting(e, nids=[e.reviewer.card.nid]))

cc = QAction(_('Clear Fields Format HTML (remove new lines only)'), mw)
cc.setShortcut(QKeySequence(HOTKEY['brdiv'][0]))
mw.connect(cc, SIGNAL('triggered()'), lambda e=mw:
           onClearFormatted(e, nids=[e.reviewer.card.nid]))

try:
    mw.addon_notes_menu
except AttributeError:
    mw.addon_notes_menu = QMenu(
        _(u'&Записи') if lang == 'ru' else _(u'&Notes'), mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_notes_menu)

# mw.form.menuEdit.addSeparator()
mw.addon_notes_menu.addSeparator()
mw.addon_notes_menu.addAction(aa)
mw.addon_notes_menu.addAction(bb)
mw.addon_notes_menu.addAction(cc)
mw.addon_notes_menu.addSeparator()


def swap_off():
    aa.setEnabled(False)
    bb.setEnabled(False)
    cc.setEnabled(False)


def swap_on():
    aa.setEnabled(True)
    bb.setEnabled(True)
    cc.setEnabled(True)

mw.deckBrowser.show = wrap(mw.deckBrowser.show, swap_off)
mw.overview.show = wrap(mw.overview.show, swap_off)
mw.reviewer.show = wrap(mw.reviewer.show, swap_on)

##

old_addons = (
    'Clear_Field_Formatting_HTML_in_Bulk.py',
    '_Clear_Field_Formatting_HTML_in_Bulk.py',
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
            ' ~ Clear Fields Formatting HTML \n' +
            'и поэтому будут конфликтовать с ним.\n\n' +
            old_addons2delete +
            '\nУдалите эти дополнения и перезапустите Anki.')
    else:
        showText(
            '<big>There are some add-ons in the folder <br>\n<br>\n' +
            ' &nbsp; ' + mw.pm.addonFolder() +
            '<pre>' + old_addons2delete + '</pre>' +
            'They are already part of<br>\n' +
            ' <b> &nbsp; ~ Clear Fields Formatting HTML</b> addon.<br>\n' +
            'Please, delete them and restart Anki.</big>', type='html')
