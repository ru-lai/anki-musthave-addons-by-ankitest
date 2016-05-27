# -*- coding: utf-8 -*-
# ~ Clear Fields Formatting HTML
# https://ankiweb.net/shared/info/1114708966
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#  Made by request: 
#   Clear Field Formatting (HTML) in Bulk needs improvement 
#    https://anki.tenderapp.com/discussions/add-ons/7526-clear-field-formatting-html-in-bulk-needs-improvement
# Based on
# https://ankiweb.net/shared/info/728131107
# Removes the field formatting of all selected notes.
# Author: xelif@icqmail.com
#
from __future__ import division
from __future__ import unicode_literals
import os, sys, datetime, re

# Get language class
import anki.lang
lang = anki.lang.getLang()

import aqt.deckbrowser
import aqt.editor
from aqt.utils import showText

from anki.hooks import addHook, wrap, runHook
from aqt import mw

from PyQt4.QtCore import *
from PyQt4.QtGui import *

HOTKEY = {      # workds in card Browser, card Reviewer and note Editor (Add?)
    'clear'  : ['Ctrl+F12', '', '', ''' ''', """ """], 
    'full'   : ['Ctrl+Shift+F12', '', '', ''' ''', """ """], 
    }

##

if __name__ == '__main__':
    print("""This is _Clear_Fields_Formatting_HTML.py add-on \
for the Anki program and it can't be run directly.""")
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2': # Python 3 is utf8 only already.
  if hasattr(sys,'setdefaultencoding'):
    sys.setdefaultencoding('utf8')

##

def stripFormatting(txt, imgbr, divbr):
    """
    Removes all html tags, except if they begin like this: <img...> <br...> <div > </div>
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
    return re.sub(imgbr, '', re.sub(divbr, '\n', re.sub('<div .*?>', '<div>', txt)))

def onClearFormat(self, nids=None, dids=None):
    mw.checkpoint('Clear Fields Format HTML')
    mw.progress.start()
    if dids:
       nids=[]
       for did in dids:
          deck = self.mw.col.decks.nameOrNone(did)
          query = 'deck:"%s"' % ( deck )
          nids.extend(self.mw.col.findNotes(query))
    if nids:
      for nid in nids:
        note = mw.col.getNote(nid)
        def clearFields(field):
            return stripFormatting(field, '<(?!img|br|div|/div).*?>', '(^$)')
        note.fields = map(clearFields, note.fields)
        note.flush()
    mw.progress.finish()
    if mw.state == 'review':
        rst = mw.reviewer.state
    else:
        rst = None
    mw.reset()
    if rst == 'answer':
        mw.reviewer._showAnswerHack()

def onClearFormatting(self, nids=None, dids=None):
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
       nids=[]
       for did in dids:
          deck = self.mw.col.decks.nameOrNone(did)
          query = 'deck:"%s"' % ( deck )
          nids.extend(self.mw.col.findNotes(query))
    if nids:
      for nid in nids: #self.selectedNotes():
        note = mw.col.getNote(nid)
        def clearField(field):
            result = stripFormatting(field, '<(?!img).*?>', '</div><div>|</div>|<div>|<br />');
            # if result != field:
            #     sys.stderr.write('Changed: \"' + field
            #                      + '\' ==> \"' + result + '\"')
            return result
        note.fields = map(clearField, note.fields)
        note.flush()
    mw.progress.finish()
    if mw.state == 'review':
        rst = mw.reviewer.state
    else:
        rst = None
    mw.reset()
    if rst == 'answer':
        mw.reviewer._showAnswerHack()

def setupMenu(self):
    """
    Add the items to the browser menu Edit
    """
    self.form.menuEdit.addSeparator()

    a = QAction(_('Clear Fields Formatting HTML (remain new lines)'), self)
    a.setShortcut(QKeySequence(HOTKEY['clear'][0]))
    self.connect(a, SIGNAL('triggered()'), lambda e=self: onClearFormat(e, nids=e.selectedNotes()))
    self.form.menuEdit.addAction(a)

    b = QAction(_('Clear Fields Formatting HTML (at all)'), self)
    b.setShortcut(QKeySequence(HOTKEY['full'][0]))
    self.connect(b, SIGNAL('triggered()'), lambda e=self: onClearFormatting(e, nids=e.selectedNotes()))
    self.form.menuEdit.addAction(b)

    self.form.menuEdit.addSeparator()

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
    a.connect(a, SIGNAL("triggered()"), lambda e=self, did=did: \
        onClearFormat(e, dids=[did]))

    a = m.addAction(_('Clear Fields Formatting HTML (at all)'))
    a.connect(a, SIGNAL("triggered()"), lambda e=self, did=did: \
        onClearFormatting(e, dids=[did]))

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
    #a.setShortcut(QKeySequence(HOTKEY['clear'][0]))
    a.connect(a, SIGNAL("triggered()"), lambda e=self: \
        onClearFormat(e, nids=[e.note.id]))

    a = m.addAction(_('Clear Fields Formatting HTML (at all)'))
    #a.setShortcut(QKeySequence(HOTKEY['full'][0]))
    a.connect(a, SIGNAL("triggered()"), lambda e=self: \
        onClearFormatting(e, nids=[e.note.id]))

    #m.addSeparator()

    m.exec_(QCursor.pos())

aqt.editor.Editor.onAdvanced = onAdvanced

##

c = QAction(_('Clear Fields Formatting HTML (remain new lines)'), mw)
c.setShortcut(QKeySequence(HOTKEY['clear'][0]))
mw.connect(c, SIGNAL('triggered()'), lambda e=mw: \
    onClearFormat(e, nids=[e.reviewer.card.nid]))

d = QAction(_('Clear Fields Formatting HTML (at all)'), mw)
d.setShortcut(QKeySequence(HOTKEY['full'][0]))
mw.connect(d, SIGNAL('triggered()'), lambda e=mw: \
    onClearFormatting(e, nids=[e.reviewer.card.nid]))

mw.form.menuEdit.addSeparator()
mw.form.menuEdit.addAction(c)
mw.form.menuEdit.addAction(d)
mw.form.menuEdit.addSeparator()

def swap_off():
    c.setEnabled(False)
    d.setEnabled(False)

def swap_on():
    c.setEnabled(True)
    d.setEnabled(True)

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
       showText('В каталоге\n\n '+mw.pm.addonFolder()+\
        '\n\nнайдены дополнения, которые уже включены в дополнение\n'+\
        ' ~ Clear Fields Formatting HTML \nи поэтому будут конфликтовать с ним.\n\n' +\
        old_addons2delete + '\nУдалите эти дополнения и перезапустите Anki.')
    else:
       showText('<big>There are some add-ons in the folder <br>\n<br>\n'+\
       ' &nbsp; '+mw.pm.addonFolder()+\
       '<pre>' + old_addons2delete +'</pre>'+\
       'They are already part of<br>\n'+\
       ' <b> &nbsp; ~ Clear Fields Formatting HTML</b> addon.<br>\n'+\
       'Please, delete them and restart Anki.</big>',type='html')

##
