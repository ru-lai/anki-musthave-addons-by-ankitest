# -*- mode: Python ; coding: utf-8 -*-
# • View HTML source with JavaScript and CSS styles 
# https://ankiweb.net/shared/info/1128123950
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
from __future__ import division
from __future__ import unicode_literals
import os, sys

from aqt import mw
from aqt.utils import showText

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import anki.lang
lang = anki.lang.getLang()

HOTKEY = {      # in mw Main Window (deckBrowser, Overview, Reviewer)
    'F3_source'      : ["Alt+F3", '', "Alt+К, Х", ''' ''', """ """], 
}

try:
    mw.addon_cards_menu
except AttributeError:
    mw.addon_cards_menu = QMenu(_(u"&Карточки") if lang == 'ru' else _(u"&Cards"), mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_cards_menu)

def _getSource():
    """To look at sourcne HTML+CSS code."""
    html = mw.web.page().mainFrame().evaluateJavaScript("""
        (function(){
             return document.documentElement.outerHTML
         }())
    """)
    showText(html) #,minW=999,title="HTML5+CSS3+JavaScript + jQuery 1.5 Source Code")

get_HTML_Source_action = QAction(mw)
get_HTML_Source_action.setText("Показать Ис&ходник HTML" if lang == 'ru' else "&View Source code")
get_HTML_Source_action.setShortcut(QKeySequence(HOTKEY['F3_source'][0]))
mw.connect(get_HTML_Source_action, SIGNAL("triggered()"), _getSource)

if hasattr(mw,'addon_cards_menu'):
    mw.addon_cards_menu.addSeparator()
    mw.addon_cards_menu.addAction(get_HTML_Source_action)
    mw.addon_cards_menu.addSeparator()
