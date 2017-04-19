# -*- mode: Python ; coding: utf-8 -*-
# • View HTML source with JavaScript and CSS styles
# https://ankiweb.net/shared/info/1128123950
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 Menu Cards - View Source code Body Alt+F3
  shows HTML source with JavaScript and CSS styles
   but without jQuery Menu Cards

 Menu Cards - View Source code Ctrl+F3
  shows full HTML source

 Works for decks panel, deck overview and any card.
"""
from __future__ import division
from __future__ import unicode_literals
import os
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from aqt import mw
from aqt.utils import showText

# Get language class
import anki.lang
lang = anki.lang.getLang()

MSG = {
    'en': {
        'later': _('later'),
        'not now': _('not now'),
        'Cards': _('&Cards'),
        'no_jQuery': _('View Source code &Body'),
        'view_source': _('&View Source code'),
        },
    'ru': {
        'later': 'позже',
        'not now': 'не сейчас',
        'Cards': '&Карточки',
        'no_jQuery': 'Показать Ис&ходник HTML Body',
        'view_source': 'Показать И&сходник HTML',
        },
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

# 'Показать Ис&ходник HTML Body' if lang == 'ru' else 'View Source code &Body'
# 'Показать И&сходник HTML' if lang == 'ru' else '&View Source code'

HOTKEY = {      # in mw Main Window (deckBrowser, Overview, Reviewer)
    'HTML_source': 'Ctrl+F3',
    'Body_source': 'Alt+F3',
}

__addon__ = "'" + __name__.replace('_',' ')
__version__ = "2.0.44a"

try:
    mw.addon_cards_menu
except AttributeError:
    mw.addon_cards_menu = QMenu(MSG[lang]['Cards'], mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_cards_menu)


def _getSourceHTML():
    """To look at sourcne HTML+CSS code."""
    html = mw.web.page().mainFrame().evaluateJavaScript("""
        (function(){
             return document.documentElement.outerHTML
         }())
    """)
    showText(html)


def _getSourceBody():
    """To look at sourcne HTML+CSS code."""
    html = '<html class="' +\
        unicode(mw.web.page().mainFrame().evaluateJavaScript("""
        (function(){
             return document.documentElement.className
         }())
    """)) + '">\n<head>\n' +\
        unicode(
            mw.web.page().mainFrame().evaluateJavaScript(
                """
        (function(){
             return document.getElementsByTagName('head')[0]""" +
                """.getElementsByTagName('style')[0].outerHTML
         }())
    """)) + '\n</head>\n' +\
        unicode(mw.web.page().mainFrame().evaluateJavaScript("""
        (function(){
             return document.body.outerHTML
         }())
    """)) + '\n</html>\n'
    showText(html)

get_Body_Source_action = QAction(mw)
get_Body_Source_action.setText(MSG[lang]['no_jQuery'])
get_Body_Source_action.setShortcut(
    QKeySequence(HOTKEY['Body_source']))
mw.connect(get_Body_Source_action, SIGNAL('triggered()'), _getSourceBody)

get_HTML_Source_action = QAction(mw)
get_HTML_Source_action.setText(MSG[lang]['view_source'])
get_HTML_Source_action.setShortcut(
    QKeySequence(HOTKEY['HTML_source']))
mw.connect(get_HTML_Source_action, SIGNAL('triggered()'), _getSourceHTML)

if hasattr(mw, 'addon_cards_menu'):
    mw.addon_cards_menu.addSeparator()
    mw.addon_cards_menu.addAction(get_Body_Source_action)
    mw.addon_cards_menu.addAction(get_HTML_Source_action)
    mw.addon_cards_menu.addSeparator()
