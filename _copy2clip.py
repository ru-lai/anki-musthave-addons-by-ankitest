# -*- mode: Python ; coding: utf-8 -*-
# ~ copy2clip
# https://ankiweb.net/shared/info/165982901
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# does not work on Windows XP
#
# No support. Use it AS IS on your own risk.
from __future__ import unicode_literals

import sys
import subprocess

from anki.hooks import wrap  # , addHook, remHook
from anki.utils import tmpdir, isWin, isMac

from aqt import mw
from aqt.qt import *
# from aqt.reviewer import Reviewer
from aqt.utils import showCritical

# in priority order
field_names = [
    # user defined field names
    'test',

    # field names to be found by default
    _('Front'),
    'Front',
    ]
    # if not found then
    #    first field would be copied

if sys.version[0] == '2':  # Python 3 is utf8 only already.
  if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf8')

def onFastTranslate():

    note = mw.reviewer.card.note()

    fldn = note.model()['flds']
    fldl = len(note.fields)

    field_index = -1
    for fld in field_names:
        for fldi, flde in enumerate(fldn):
            if fld == flde['name']:
               field_index = fldi
               break
        if field_index > -1:
            break
    else:
        field_index = 0

    if isWin:
        # p = subprocess.Popen(['clip', ''], stdin=subprocess.PIPE)
        # does not work with empty parameters
        p = subprocess.Popen('clip', stdin=subprocess.PIPE)
    elif isMac:
        p = subprocess.Popen('pbclip', stdin=subprocess.PIPE)
    else:
        p = subprocess.Popen(['xclip', '-i'], stdin=subprocess.PIPE)

    msg = note.fields[field_index]
    msg8 = msg.encode('utf-8')
    # showCritical(msg + '<br>' + msg8)
    res = p.communicate(msg8)

    if p.returncode:
        showCritical('_copy2clip has return code ' +
                     'from pipe subprocess clip:<br>' + 
                     unicode(p.returncode) + '<br>' + unicode(res))

# define a new hotkey

#c = QShortcut(QKeySequence("c"), mw)
#c.connect(c, SIGNAL("activated()"), onFastTranslate)

auction = QAction(mw)
auction.setText('copy2clip')
auction.setShortcut(QKeySequence('c'))
mw.connect(auction, SIGNAL('triggered()'), onFastTranslate)
mw.form.menuEdit.addAction(auction)


def swap_off():
    auction.setEnabled(False)


def swap_on():
    auction.setEnabled(True)

mw.deckBrowser.show = wrap(mw.deckBrowser.show, swap_off)
mw.overview.show = wrap(mw.overview.show, swap_off)
mw.reviewer.show = wrap(mw.reviewer.show, swap_on)
