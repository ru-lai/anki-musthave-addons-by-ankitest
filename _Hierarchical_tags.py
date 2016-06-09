# -*- mode: Python ; coding: utf-8 -*-
# ~ Hierarchical tags
# https://ankiweb.net/shared/info/2019995763
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# Correct work of search string on any level of hierarchy.
# Expand/Collapse Whole Browser Tree.
#
# No support. Use it AS IS on your own risk.

"""
Hierarchical Tags for Anki
==========================

This addon adds hierarchical tags to the browser in [Anki][]. The addon is
[published on Ankiweb](https://ankiweb.net/shared/info/1089921461).

To create hierarchies use double-colons in the tag names, for example
"learning::anki" or "language::japanese".

This addon is licensed under the same license as Anki itself (GNU Affero
General Public License 3).


## Known Issues

When clicking on a tag in the hierarchy, an asterisk is added to the search
term. The effect of that is that all notes with that tag and all subtags are
searched for.

But a side-effect is, that all tags with the same prefix are matched. For
example if you have a tag ``it`` and a tag ``italian``, clicking on the tag
``it`` would also show content from ``italian``. Let me know if this affects
you and I'll try to work around this.


## Support

The add-on was written by [Patrice Neff][]. I try to monitor threads in the
[Anki Support forum][]. To be safe you may also want to open a ticket on the
plugin's [GitHub issues][] page.


[Anki]: http://ankisrs.net/
[Patrice Neff]: http://patrice.ch/
[Anki support forum]: https://anki.tenderapp.com/discussions/add-ons
[GitHub issues]: https://github.com/pneff/anki-hierarchical-tags/issues 
"""
from __future__ import unicode_literals
import sys

import PyQt4.QtGui
import PyQt4.QtCore

from aqt.qt import *

import aqt.browser
import anki.hooks

#####################
# Get language class
# Выбранный пользователем язык программной оболочки
import anki.lang
lang = anki.lang.getLang()

CtrlShiftPlus = 'Ctrl+Shift++'  # Expand   Them All
CtrlShiftMinus = 'Ctrl+Shift+-'  # Collapse Them All

if __name__ == '__main__':
    print("This is _Hierarchical_tags add-on for the Anki program " +
          "and it can't be run directly.")
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2':  # Python 3 is utf8 only already.
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf8')

# thanks to Patrice Neff http://patrice.ch/
# https://github.com/pneff/anki-hierarchical-tags
# https://ankiweb.net/shared/info/1089921461

# Separator used between hierarchies
SEPARATOR = '::'

def _userTagTree(self, root):
    tags = sorted(self.col.tags.all())
    tags_tree = {}

    for t in tags:
        if t.lower() == "marked" or t.lower() == "leech":
            continue

        components = t.split(SEPARATOR)
        for idx, c in enumerate(components):
            partial_tag = SEPARATOR.join(components[0:idx + 1])
            if not tags_tree.get(partial_tag):
                if idx == 0:
                    parent = root
                else:
                    parent_tag = SEPARATOR.join(components[0:idx])
                    parent = tags_tree[parent_tag]

                item = self.CallbackItem(
                    parent, c,
                    lambda ptg=partial_tag: self.setFilter(
                        '(tag:"' + ptg + '::*" or tag:"' + ptg + '")'))
                item.setIcon(0, QIcon(":/icons/anki-tag.png"))

                tags_tree[partial_tag] = item


aqt.browser.Browser._userTagTree = _userTagTree


def setupMenu(self):
    menu = self.form.menuJump  # .menuEdit
    menu.addSeparator()

    a = menu.addAction('Развернуть всё дерево' if lang ==
                       'ru' else _('Expand Them All'))
    a.setShortcut(QKeySequence(CtrlShiftPlus))
    self.connect(a, PyQt4.QtCore.SIGNAL('triggered()'),
                 lambda b=self: ExpandThemAll(b, True, False))

    a = menu.addAction('Свернуть все ветки' if lang ==
                       'ru' else _('Collapse Them All'))
    a.setShortcut(QKeySequence(CtrlShiftMinus))
    self.connect(a, PyQt4.QtCore.SIGNAL('triggered()'),
                 lambda b=self: ExpandThemAll(b, False, True))

    menu.addSeparator()


def ExpandThemAll(self, action, atAll):
    if action:
        self.form.tree.expandAll()
    elif atAll:
        self.form.tree.collapseAll()
    else:
        self.form.tree.collapseAll()
        self.form.tree.expandToDepth(0)

anki.hooks.addHook('browser.setupMenus', setupMenu)
