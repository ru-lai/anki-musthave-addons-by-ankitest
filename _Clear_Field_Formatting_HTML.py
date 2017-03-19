# -*- mode: Python ; coding: utf-8 -*-
# ~ Clear Fields Formatting HTML
# https://ankiweb.net/shared/info/1114708966
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# NB! Create backup copy before bulk changes!
#
# This one creates a new items  Clear Field Formatting HTML ...
# in the Notes menu of the card Browser and Reviewer.
#
# Using this, notes of all selected cards will be cleared of any html tags,
# resulting in the removal of any formatting directly in the fields.
# This does NOT change the card template (layout) itself,
# but only the notes you selected in the card browser.
#
# Html tag   img   always stays inplace cause it's used to add pictures.
# HTML tags   br div   may be not removed because they are used to line break
# ( style= and other attributes from   DIV   would be deleted ).
# Also you can remove only new lines
# (it means html tags   br div   will be removed
#   with their styles and attributes)
# but all other markup will stay in place.
#
# FIELDS_ONLY list limits changes of fields to the certain scope.
#
# Support Remove some html tags: A B I U P S sub sup FONT.
# Also you can remove or replace colors, getted by F7/F8.
#
# In Add and Edit windows (under down arrow)
#  this one acts in current field only.
#
#  Made by request:
#   Clear Field Formatting (HTML) in Bulk needs improvement
#    https://anki.tenderapp.com/discussions/add-ons/
#    7526-clear-field-formatting-html-in-bulk-needs-improvement
# Based on
# https://ankiweb.net/shared/info/728131107
# Removes the field formatting of all selected notes.
# Author: xelif@icqmail.com
# Inspired by
# https://ankiweb.net/shared/info/1290231794
# RemoveLinebreak
#
# No support. Use it AS IS on your own risk.
from __future__ import division
from __future__ import unicode_literals
import os
import sys
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import aqt.deckbrowser
import aqt.editor
from aqt.utils import showText, tooltip, askUser, getText, showInfo

from anki.hooks import addHook, wrap, runHook
from aqt import mw

# Get language class
import anki.lang
lang = anki.lang.getLang()

# Empty list means:
# "Apply changes to all fields in the note"
FIELDS_ONLY = []  # [_('Front'), 'Front']  #
FIELDS_ACCEPTED = False

HOTKEY = {      # workds in card Browser, card Reviewer and note Editor (Add?)
    'clear':    'Ctrl+F12',
    'full':     'Ctrl+Shift+F12',
    'brdiv':    'Alt+Shift+F12',
    'retags':   'Ctrl+Alt+Shift+F12',
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


def stripFormatting(txt, removeTags, newlineTags, replaceTags):
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
    """

    result = ''
    if not txt:
        return ''
    if newlineTags:
        result = re.sub(newlineTags, '\n', txt)
    else:
        result = txt
    if removeTags:
        if replaceTags:
            result = re.sub(removeTags, replaceTags, result)
        else:
            result = re.sub(removeTags, '', result)
    # if result != txt:
    #     sys.stderr.write('Changed: \"' + txt
    #                      + '\' ==> \"' + result + '\"')
    return result


def clearFormatting(self, nids=None, dids=None, note=None, chk=True,
                    removeTags='', newlineTags='', replaceTags=''):
    """
    Clears the formatting for every selected note.
    Also creates a restore point, allowing a single undo operation.

    Parameters
    ----------
    self : Browser
        the anki self from which the function is called
    """
    global FIELDS_ONLY, FIELDS_ACCEPTED
    delAllTags = (removeTags == '' and newlineTags == '' and replaceTags == '')

    if dids:
        nids = []
        for did in dids:
            deck = self.mw.col.decks.nameOrNone(did)
            query = 'deck:"%s"' % (deck)
            nids.extend(self.mw.col.findNotes(query))

    if nids and not delAllTags and not FIELDS_ACCEPTED:
        demand = getText(
            'Список очищаемых полей через запятую\n' +
            '(для обработки всех полей — оставьте пустым)'
            if lang == 'ru' else
            'Comma delimited list of fields\n' +
            '(leave blank to process all fields)',
            default=', '.join(FIELDS_ONLY))
        if not demand[1]:
            tooltip('  <i>Clear Field Formatting HTML</i>   cancelled by user',
                    period=2500)
            return
        FIELDS_ONLY = map(unicode.strip, demand[0].strip().split(','))
        if FIELDS_ONLY == ['']:
            FIELDS_ONLY = []
        FIELDS_ACCEPTED = True

    if nids:
        if chk:
            mw.checkpoint('Clear Fields Formatting HTML')
            mw.progress.start()

        for nid in nids:  # self.selectedNotes():
            note = mw.col.getNote(nid)
            if delAllTags:
                note.tags = []
            elif FIELDS_ONLY:
                flds = note.model()['flds']
                for FIELD_ONLY in FIELDS_ONLY:
                    for fldi, fld in enumerate(flds):
                        if fld['name'].lower() == FIELD_ONLY.lower().strip():
                            note.fields[fldi] = stripFormatting(
                                note.fields[fldi],
                                removeTags, newlineTags, replaceTags)
            else:
                note.fields = map(
                    lambda x: stripFormatting(
                        x, removeTags, newlineTags, replaceTags),
                    note.fields)
            note.flush()
        if chk:
            mw.progress.finish()
    elif note:
        if delAllTags:
            note.tags = []
        else:
            note.fields[self.currentField] = stripFormatting(
                note.fields[self.currentField],
                removeTags, newlineTags, replaceTags)
        note.flush()

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
        removeTags='<(?!img|br|div|/div).*?>',)


def onClearFormatting(self, nids=None, dids=None, note=None):
    clearFormatting(
        self, nids=nids, dids=dids, note=note,
        removeTags='<(?!img).*?>',
        newlineTags='</div><div.*?>|</div>|<div.*?>|<br.*?>')


def onClearFormatted(self, nids=None, dids=None, note=None):
    clearFormatting(
        self, nids=nids, dids=dids, note=note,
        newlineTags='</div><div.*?>|</div>|<div.*?>|<br.*?>')
    # to keep attr=... first replace DIV with SPAN


def onClearFormattag(self, nids=None, dids=None, note=None):
    global FIELDS_ACCEPTED
    FIELDS_ACCEPTED = False

    OLDcolor = ''
    NEWcolor = ''
    removeAllTags = False

    valid = (
        'a', 'b', 'i', 'u', 'p', 's', 'sub', 'sup', 'font', 'img', 'sound')
    demand = getText(
        'Remove some of HTML tags <b>' + ' '.join(valid) +
        '</b><br>   or replace   <i>OLDcolor NEWcolor</i>' +
        '</b><br>   or delete    <i>OLDcolor</i>' +
        '<br>   or enter <b>tags</b> keyword  ' +
        ' to remove   All   Note <i>Tags</i>')
    stencil = []
    if not demand[1]:  # cancelled by user
        return

    mw.checkpoint('Clear Fields Formatting HTML')
    mw.progress.start()

    requests = demand[0].strip().lower().split()
    for req in requests:
        if req in valid:
            if req in ('sound'):
                stencil.extend(['\[sound\:.*?\]'])
            elif req in ('img'):
                stencil.extend(['<%s.*?>' % (req)])
            else:
                stencil.extend(['<%s.*?>|</%s>' % (req, req)])
        elif req == 'tags':
            removeAllTags = True
        else:
            if not OLDcolor:
                OLDcolor = req
            else:
                NEWcolor = req
        if req == 'b':
            stencil.extend(['<strong.*?>|</strong>'])
        if req == 'i':
            stencil.extend(['<em.*?>|</em>'])
        if req == 's':
            stencil.extend(['<strike.*?>|</strike>|' +
                           '<del.*?>|</del>|<ins.*?>|</ins>'])

    join_stencil = '|'.join(stencil)
    if stencil and askUser('Delete %s?' % (join_stencil)):
        clearFormatting(
            self, nids=nids, dids=dids, note=note, chk=False,
            removeTags=join_stencil)

    if OLDcolor:
        # tooltip('Sorry, not implemented yet.')
        # return

        oldTag = '''\s+?color\s*?\=\s*?["']??(%s)["']??''' % \
            (OLDcolor)
        if NEWcolor:
            if askUser(
                    ('Replace color <b style="color:%s;">%s</b>' +
                     ' with <b style="color:%s;">%s</b>?') %
                    (OLDcolor, OLDcolor, NEWcolor, NEWcolor)):
                newTag = ' color="%s"' % (NEWcolor)
                clearFormatting(
                    self, nids=nids, dids=dids, note=note, chk=False,
                    removeTags=oldTag, replaceTags=newTag)
        else:
            if askUser(
                    'Delete color <b style="color:%s;">%s</b>?' %
                    (OLDcolor, OLDcolor)):
                clearFormatting(
                    self, nids=nids, dids=dids, note=note, chk=False,
                    removeTags=oldTag)

    if removeAllTags and askUser('Delete all Tags?'):
        clearFormatting(
            self, nids=nids, dids=dids, note=note, chk=False)

    mw.progress.finish()


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

    a = QAction(_('Clear Fields Formatting (Remain New Lines)'), self)
    a.setShortcut(QKeySequence(HOTKEY['clear']))
    self.connect(a, SIGNAL('triggered()'),
                 lambda e=self: onClearFormat(e, nids=e.selectedNotes()))
    self.form.addon_notes_menu.addAction(a)

    b = QAction(_('Clear Fields Formatting HTML (at all)'), self)
    b.setShortcut(QKeySequence(HOTKEY['full']))
    self.connect(b, SIGNAL('triggered()'),
                 lambda e=self: onClearFormatting(e, nids=e.selectedNotes()))
    self.form.addon_notes_menu.addAction(b)

    c = QAction(_('Clear Fields Format (Remove New Lines only)'), self)
    c.setShortcut(QKeySequence(HOTKEY['brdiv']))
    self.connect(c, SIGNAL('triggered()'),
                 lambda e=self: onClearFormatted(e, nids=e.selectedNotes()))
    self.form.addon_notes_menu.addAction(c)

    d = QAction(_('Clear Fields (remove tags or change color)'), self)
    d.setShortcut(QKeySequence(HOTKEY['retags']))
    self.connect(d, SIGNAL('triggered()'),
                 lambda e=self: onClearFormattag(e, nids=e.selectedNotes()))
    self.form.addon_notes_menu.addAction(d)

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

    a = m.addAction(_('Clear Fields Formatting (Remain New Lines)'))
    a.connect(a, SIGNAL("triggered()"), lambda e=self, did=did:
              onClearFormat(e, dids=[did]))

    a = m.addAction(_('Clear Fields Formatting HTML (at all)'))
    a.connect(a, SIGNAL("triggered()"), lambda e=self, did=did:
              onClearFormatting(e, dids=[did]))

    a = m.addAction(_('Clear Fields Format (Remove New Lines only)'))
    a.connect(a, SIGNAL("triggered()"), lambda e=self, did=did:
              onClearFormatted(e, dids=[did]))

    a = m.addAction(_('Clear Fields (remove tags or change color)'))
    a.connect(a, SIGNAL("triggered()"), lambda e=self, did=did:
              onClearFormattag(e, dids=[did]))

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

    runHook("latexHooker", self, m)

    m.exec_(QCursor.pos())

aqt.editor.Editor.onAdvanced = onAdvanced


def latexHooker(self, m):
    m.addSeparator()

    a = m.addAction(_('Clear Field Formatting (remain new lines)'))
    # a.setShortcut(QKeySequence(HOTKEY['clear']))
    a.connect(a, SIGNAL("triggered()"), lambda e=self:
              onClearFormat(e, note=self.note))

    a = m.addAction(_('Clear Field Formatting HTML (at all)'))
    # a.setShortcut(QKeySequence(HOTKEY['full']))
    a.connect(a, SIGNAL("triggered()"), lambda e=self:
              onClearFormatting(e, note=self.note))

    a = m.addAction(_('Clear Field Format (remove new lines only)'))
    # a.setShortcut(QKeySequence(HOTKEY['brdiv']))
    a.connect(a, SIGNAL("triggered()"), lambda e=self:
              onClearFormatted(e, note=self.note))

    a = m.addAction(_('Clear Field (remove tags or change color)'))
    # a.setShortcut(QKeySequence(HOTKEY['retags']))
    a.connect(a, SIGNAL("triggered()"), lambda e=self:
              onClearFormattag(e, note=self.note))

    m.addSeparator()

addHook('latexHooker', latexHooker)

##

aa = QAction(_('Clear Fields Formatting (Remain New Lines)'), mw)
aa.setShortcut(QKeySequence(HOTKEY['clear']))
mw.connect(aa, SIGNAL('triggered()'), lambda e=mw:
           onClearFormat(e, nids=[e.reviewer.card.nid]))

bb = QAction(_('Clear Fields Formatting HTML (at all)'), mw)
bb.setShortcut(QKeySequence(HOTKEY['full']))
mw.connect(bb, SIGNAL('triggered()'), lambda e=mw:
           onClearFormatting(e, nids=[e.reviewer.card.nid]))

cc = QAction(_('Clear Fields Format (Remove New Lines only)'), mw)
cc.setShortcut(QKeySequence(HOTKEY['brdiv']))
mw.connect(cc, SIGNAL('triggered()'), lambda e=mw:
           onClearFormatted(e, nids=[e.reviewer.card.nid]))

dd = QAction(_('Clear Fields (remove tags or change color)'), mw)
dd.setShortcut(QKeySequence(HOTKEY['retags']))
mw.connect(dd, SIGNAL('triggered()'), lambda e=mw:
           onClearFormattag(e, nids=[e.reviewer.card.nid]))

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
mw.addon_notes_menu.addAction(dd)
mw.addon_notes_menu.addSeparator()


def swap_off():
    aa.setEnabled(False)
    bb.setEnabled(False)
    cc.setEnabled(False)
    dd.setEnabled(False)


def swap_on():
    aa.setEnabled(True)
    bb.setEnabled(True)
    cc.setEnabled(True)
    dd.setEnabled(True)

mw.deckBrowser.show = wrap(mw.deckBrowser.show, swap_off)
mw.overview.show = wrap(mw.overview.show, swap_off)
mw.reviewer.show = wrap(mw.reviewer.show, swap_on)

##


def save_FIELDS_ONLY():
    mw.pm.profile['cff_FIELDS_ONLY'] = FIELDS_ONLY


def load_FIELDS_ONLY():
    global FIELDS_ONLY

    try:
        key_value = mw.pm.profile['cff_FIELDS_ONLY']
        FIELDS_ONLY = key_value
    except KeyError:
        pass

addHook('unloadProfile', save_FIELDS_ONLY)
addHook('profileLoaded', load_FIELDS_ONLY)

##

old_addons = (
    'Clear_Field_Formatting_HTML_in_Bulk.py',
    '_Clear_Field_Formatting_HTML_in_Bulk.py',
    'RemoveLinebreak.py',
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
            '\n\nнайдены дополнения, которые уже включены в дополнение\n ' +
            os.path.basename(__file__) + '\n' +
            'и поэтому будут конфликтовать с ним.\n\n' +
            old_addons2delete +
            '\nПереименуйте (добавьте расширение .off) ' +
            '\n или удалите эти дополнения ' +
            '\n   и перезапустите Anki.')
    else:
        showText(
            'There are some add-ons in the folder \n\n ' +
            mw.pm.addonFolder() + '\n\n' +
            old_addons2delete +
            '\n\nThey are already part of this addon,\n ' +
            os.path.basename(__file__) +
            '\n\nPlease, rename them (add .off extension to file)' +
            ' or delete\n and restart Anki.')
