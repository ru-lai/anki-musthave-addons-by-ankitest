# -*- coding: utf-8 -*-
# ~ Search Google for selected text in Reviewer
# https://ankiweb.net/shared/info/1514982403
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
# 14.05.2016 -- not only Google now!
"""
Adds Search For Selected Text to the Reviewer Window's context/popup menu

https://ankiweb.net/shared/info/1514982403

Copyright: Steve AW <steveawa@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

Support: Use at your own risk. If you do find a problem please email me
or use one the following forums, however there are certain periods
throughout the year when I will not have time to do any work on
these addons.

Github page:  https://github.com/steveaw/anki_addons
24.07.2013
"""
from __future__ import unicode_literals

SEARCH = (
    ('Google',  'https://www.google.com/search?q=%s&ie=utf-8&oe=utf-8'),
    ('Yandex',  'https://www.yandex.com/search/?text=%s'),
    ('Bing',    'https://www.bing.com/search?q=%s'),
)

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip
from aqt.webview import AnkiWebView
from anki.hooks import runHook, addHook
import urllib

def selected_text_as_query(web_view):
    sel = web_view.page().selectedText()
    return " ".join(sel.split())

def on_search_for_selection(web_view, location):
    sel_encode = selected_text_as_query(web_view).encode('utf8', 'ignore')
    #need to do this the long way around to avoid double % encoding
    adres = QUrl.fromEncoded(location % urllib.quote(sel_encode))
    #openLink(SEARCH_URL + sel_encode)
    tooltip(_("Loading..."), period=1000)
    QDesktopServices.openUrl(adres)

def insert_search_menu_action(anki_web_view, m):
  if mw.state != 'review':
     return
  for SE in SEARCH:
    SEARCH_PROVIDER = SE[0]
    SEARCH_URL      = SE[1]
    selected = selected_text_as_query(anki_web_view)
    truncated = (selected[:40] + '..') if len(selected) > 40 else selected
    a = m.addAction('Search %s for "%s" ' % (SEARCH_PROVIDER, truncated))
    if len(selected) == 0:
        a.setDisabled(True)
    a.connect(a, SIGNAL("triggered()"),
              lambda wv=anki_web_view, loc=SEARCH_URL: on_search_for_selection(wv, loc))

addHook("AnkiWebView.contextMenuEvent", insert_search_menu_action)