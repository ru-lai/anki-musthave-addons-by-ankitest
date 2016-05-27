# -*- mode: Python ; coding: utf-8 -*-
# • Zooming
# https://ankiweb.net/shared/info/1071179937
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# The image is enlarged up to a maximum of 95% of the height or width
#  of the card's window.
#
from __future__ import division
from __future__ import unicode_literals
import os
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from aqt import mw
from aqt.qt import *
from aqt.utils import showText, showWarning, showCritical
from anki.hooks import addHook, wrap, runHook
import aqt.browser

# Get language class
import anki.lang
lang = anki.lang.getLang()

if __name__ == '__main__':
    print("This is _Zooming add-on for the Anki program" +
          " and it can't be run directly.")
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2':  # Python 3 is utf8 only already.
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf8')

ZOOM_IMAGES = True  # False #

# Standard zoom factors for the main views of the central area:
deck_browser_standard_zoom = 1.2
overview_standard_zoom = 1.3
reviewer_standard_zoom = 1.4
# Before you change the reviewer_standard_zoom size, maybe you should
# use larger fonts in your decks.

# inspired by Force custom font
# https://ankiweb.net/shared/info/2103013902
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

FONT = False  # Use font as it comes from Anki
FONTSIZE = 0  # Use default font size

FONT = 'Calibri'  # Use custom typeface
FONTSIZE = 16  # 12 #18 #20 #24


def changeFont():
    f = QFontInfo(QFont(FONT))
    ws = QWebSettings.globalSettings()
    mw.fontHeight = FONTSIZE if FONTSIZE else f.pixelSize()
    mw.fontFamily = f.family()
    mw.fontHeightDelta = max(0, mw.fontHeight - 13)
    ws.setFontFamily(QWebSettings.StandardFont, mw.fontFamily)
    ws.setFontSize(QWebSettings.DefaultFontSize, mw.fontHeight)
    mw.reset()

if FONT or FONTSIZE:
    changeFont()

try:
    MUSTHAVE_COLOR_ICONS = os.path.join(mw.pm.addonFolder(), 'zooming_icons')
except:
    MUSTHAVE_COLOR_ICONS = ''

HOTKEY = {      # in mw Main Window (deckBrowser, Overview, Reviewer)
    'zoom_info':    ['Alt+0', '', '', ''' ''', """ """],
    'zoom_in':      ['Ctrl++', '', '', ''' ''', """ """],
    'zoom_out':     ['Ctrl+-', '', '', ''' ''', """ """],
    'zoom_reset':   ['Ctrl+0', '', '', ''' ''', """ """],
    'zoom_init':    ['Ctrl+Alt+0', '', '', ''' ''', """ """],
}

##################################################################
# inspired by ZOOM
# https://ankiweb.net/shared/info/1956318463

# improved:
# remember user choice
# step 10% (not 20%)
# View - Zoom submenu items
# info about current values

deck_browser_current_zoom = deck_browser_standard_zoom
overview_current_zoom = overview_standard_zoom
reviewer_current_zoom = reviewer_standard_zoom

# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html

'''Add-on for Anki 2 to zoom in or out.'''


def reset_current_zoom():
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    deck_browser_current_zoom = deck_browser_standard_zoom
    overview_current_zoom = overview_standard_zoom
    reviewer_current_zoom = reviewer_standard_zoom

# How much to increase or decrease the zoom FACTOR with each step. The
# a little odd looking number is the fourth root of two. That means
# with four clicks you double or half the size, as precisely as possible.
zoom_step = .1  # 1.1
# min 0.5 after 1.9 next 2.1
# 1.5**.15 min 0.8 # 2.0**0.25


def zoom_in(step=None):
    # Increase the text size.
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    if not step:
        step = zoom_step

    if 'deckBrowser' == mw.state:
        # deck_browser_current_zoom = \
        #    round(deck_browser_current_zoom * zoom_step, 1)
        deck_browser_current_zoom = round(
            deck_browser_current_zoom + zoom_step, 1)
        current_zoom = deck_browser_current_zoom
    if 'overview' == mw.state or 'requestRequired' == mw.state:
        overview_current_zoom = round(overview_current_zoom + zoom_step, 1)
        current_zoom = overview_current_zoom
    if 'review' == mw.state:
        reviewer_current_zoom = round(reviewer_current_zoom + zoom_step, 1)
        current_zoom = reviewer_current_zoom

    if ZOOM_IMAGES:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)


def zoom_out(step=None):
    # Decrease the text size.
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    if not step:
        step = zoom_step

    if 'deckBrowser' == mw.state:
        # deck_browser_current_zoom = \
        #    round(deck_browser_current_zoom / zoom_step, 1)
        deck_browser_current_zoom = max(.1, round(
            deck_browser_current_zoom - zoom_step, 1))
        current_zoom = deck_browser_current_zoom
    if 'overview' == mw.state or 'requestRequired' == mw.state:
        overview_current_zoom = max(.1, round(
            overview_current_zoom - zoom_step, 1))
        current_zoom = overview_current_zoom
    if 'review' == mw.state:
        reviewer_current_zoom = max(.1, round(
            reviewer_current_zoom - zoom_step, 1))
        current_zoom = reviewer_current_zoom

    if ZOOM_IMAGES:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)


def zoom_init(state=None, *args):
    # Reset the text size.
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    current_zoom = 1.0

    deck_browser_current_zoom = 1.0
    overview_current_zoom = 1.0
    reviewer_current_zoom = 1.0

    if ZOOM_IMAGES:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)


def zoom_reset(state=None, *args):
    # Reset the text size.
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    current_zoom = 1.0

    if 'deckBrowser' == mw.state:
        current_zoom = deck_browser_standard_zoom
    if 'overview' == mw.state or 'requestRequired' == mw.state:
        current_zoom = overview_standard_zoom
    if 'review' == mw.state:
        current_zoom = reviewer_standard_zoom
    reset_current_zoom()

    if ZOOM_IMAGES:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)


def current_reset_zoom(state=None, *args):
    # Reset the text size.
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    current_zoom = 1

    if 'deckBrowser' == mw.state:
        current_zoom = deck_browser_current_zoom
    if 'overview' == mw.state or 'requestRequired' == mw.state:
        current_zoom = overview_current_zoom
    if 'review' == mw.state:
        current_zoom = reviewer_current_zoom

    if ZOOM_IMAGES:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)


def zoom_info():
    showText(
        '<table><tbody>\n' +
        '<tr><td align=right><big>deck_browser_standard_zoom = </big>' +
        '</td><td><big><b>' + str(deck_browser_current_zoom) +
        '</b></big></td></tr>\n' +
        '<tr><td align=right><big>overview_standard_zoom = </big>' +
        '</td><td><big><b>' + str(overview_current_zoom) +
        '</b></td></tr>\n' +
        '<tr><td align=right><big>reviewer_standard_zoom = </big>' +
        '</td><td><big><b>' + str(reviewer_current_zoom) +
        '</b></big></td></tr>\n' +
        '<tr><td align=right><br>ZOOM_IMAGES = </td><td><br><b>' +
        unicode(ZOOM_IMAGES) + '</b></td></tr>\n' +
        '<tr><td align=right>textSizeMultiplier = </td><td><b>' +
        str(mw.web.textSizeMultiplier()) + '</b></td></tr>' +
        '<tr><td align=right>zoomFactor = </td><td><b>' +
        str(mw.web.zoomFactor()) + '</b></td></tr>' +
        '</tbody></table>', type='HTML')


def zoom_images(act):
    global ZOOM_IMAGES
    ZOOM_IMAGES = act.isChecked()
    if ZOOM_IMAGES:
        showWarning('Чтобы изменения вступили в силу —<br> пожалуйста, ' +
                    '<b>перезапустите Anki</b>' if lang == 'ru'
                    else 'Please, <b>restart Anki</b><br> to apply changes.')
    current_reset_zoom()

try:
    mw.addon_view_menu
except AttributeError:
    mw.addon_view_menu = QMenu(
        _('&Вид') if lang == 'ru' else _('&View'), mw.menuBar())
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_view_menu)

zoom_images_action = None  # global


def zoom_setup_menu():
    global zoom_images_action

    mw.zoom_submenu = QMenu('Мас&штаб' if lang ==
                            'ru' else _('&Zoom'), mw.menuBar())
    mw.zoom_submenu.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'zoom.png')))

    zoom_info_action = QAction(
        'Масштаб &показать' if lang == 'ru' else _('Zoom In&fo'), mw)
    # Ctrl+Shift+0 doesn't work on NumPad
    zoom_info_action.setShortcut(QKeySequence(HOTKEY['zoom_info'][0]))
    mw.connect(zoom_info_action, SIGNAL('triggered()'), zoom_info)

    zoom_images_action = QAction(
        'Масштаб &картинок менять' if lang == 'ru' else _('&Zoom Images'), mw)
    # zoom_images_action.setShortcut(QKeySequence(HOTKEY['zoom_images'][0]))
    zoom_images_action.setCheckable(True)
    zoom_images_action.setChecked(ZOOM_IMAGES)
    mw.connect(zoom_images_action, SIGNAL('triggered()'),
               lambda AKT=zoom_images_action: zoom_images(AKT))

    zoom_in_action = QAction(
        'Масштаб у&величить' if lang == 'ru' else _('Zoom &In'), mw)
    zoom_in_action.setShortcut(QKeySequence(HOTKEY['zoom_in'][0]))
    zoom_in_action.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'zoom_in.png')))
    mw.connect(zoom_in_action, SIGNAL('triggered()'), zoom_in)

    zoom_out_action = QAction(
        'Масштаб у&меньшить' if lang == 'ru' else _('Zoom &Out'), mw)
    zoom_out_action.setShortcut(QKeySequence(HOTKEY['zoom_out'][0]))
    zoom_out_action.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'zoom_out.png')))
    mw.connect(zoom_out_action, SIGNAL('triggered()'), zoom_out)

    reset_zoom_action = QAction(
        'Масштаб на&чальный ( =' + str(deck_browser_standard_zoom) +
        ' =' + str(overview_standard_zoom) + ' =' +
        str(reviewer_standard_zoom) + ' )'
        if lang == 'ru' else _('&Reset Initial ') +
        '( =' + str(deck_browser_standard_zoom) + ' =' +
        str(overview_standard_zoom) + ' =' +
        str(reviewer_standard_zoom) + ' )', mw)
    # Shift+0 does not work on NumPad
    reset_zoom_action.setShortcut(QKeySequence(HOTKEY['zoom_reset'][0]))
    mw.connect(reset_zoom_action, SIGNAL('triggered()'), zoom_reset)

    reset_zoom_init_action = QAction(
        'Мас&штаб 1:1 100% ( =1.0 =1.0 =1.0 )' if lang == 'ru'
        else _('Reset &1:1 100% ( =1.0 =1.0 =1.0 )'), mw)
    reset_zoom_init_action.setShortcut(QKeySequence(HOTKEY['zoom_init'][0]))
    mw.connect(reset_zoom_init_action, SIGNAL('triggered()'), zoom_init)

    if hasattr(mw, 'addon_view_menu'):
        mw.addon_view_menu.addMenu(mw.zoom_submenu)
        mw.zoom_submenu.addAction(zoom_info_action)
        mw.zoom_submenu.addAction(zoom_images_action)
        mw.zoom_submenu.addSeparator()
        mw.zoom_submenu.addAction(zoom_in_action)
        mw.zoom_submenu.addAction(zoom_out_action)
        mw.zoom_submenu.addSeparator()
        if deck_browser_standard_zoom != 1.0 or \
           overview_standard_zoom != 1.0 or \
           reviewer_standard_zoom != 1.0:
            mw.zoom_submenu.addAction(reset_zoom_action)
        mw.zoom_submenu.addAction(reset_zoom_init_action)

################################
#


def handle_wheel_event(event):
    """Zoom on mouse wheel events with Ctrl.

    Zoom in our out on mouse wheel events when Ctrl is pressed.
    A standard mouse wheel click is 120/8 degree.
    ZOOM by one step for that amount.
    """

    if event.modifiers() & Qt.ControlModifier:
        step = event.delta() / 120 * zoom_step
        if step < 0:
            zoom_in(-step)
        else:
            zoom_out(step)
    else:
        original_mw_web_wheelEvent(event)


def run_move_to_state_hook(state, *args):
    '''Run a hook whenever we have changed the state.'''
    runHook('movedToState', state)

mw.moveToState = wrap(mw.moveToState, run_move_to_state_hook)
addHook('movedToState', current_reset_zoom)
original_mw_web_wheelEvent = mw.web.wheelEvent
mw.web.wheelEvent = handle_wheel_event

zoom_setup_menu()

##


def save_toolbarz_visible():
    mw.pm.profile['ctb_deck_browser_zoom'] = deck_browser_current_zoom
    mw.pm.profile['ctb_overview_zoom'] = overview_current_zoom
    mw.pm.profile['ctb_reviewer_zoom'] = reviewer_current_zoom
    mw.pm.profile['ctb_images_zoom'] = ZOOM_IMAGES


def load_toolbarz_visible():
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom, zoom_images_action, ZOOM_IMAGES

    try:
        key_value = mw.pm.profile['ctb_deck_browser_zoom']
        deck_browser_current_zoom = key_value
    except KeyError:
        pass
    #    deck_browser_current_zoom = deck_browser_standard_zoom

    try:
        key_value = mw.pm.profile['ctb_overview_zoom']
        overview_current_zoom = key_value
    except KeyError:
        pass
    #   overview_current_zoom = overview_standard_zoom

    try:
        key_value = mw.pm.profile['ctb_reviewer_zoom']
        reviewer_current_zoom = key_value
    except KeyError:
        pass
    #   reviewer_current_zoom = reviewer_standard_zoom

    try:
        key_value = mw.pm.profile['ctb_images_zoom']
        ZOOM_IMAGES = key_value
    except KeyError:
        pass

    zoom_images_action.setChecked(ZOOM_IMAGES)
    current_reset_zoom()

addHook('unloadProfile', save_toolbarz_visible)
addHook('profileLoaded', load_toolbarz_visible)

##


def openPreview(self):
    current_zoom = reviewer_current_zoom

    if ZOOM_IMAGES:
        # self._previewWindow.setZoomFactor(current_zoom)
        # AttributeError: 'QDialog' object has no attribute 'setZoomFactor'
        self._previewWeb.setZoomFactor(current_zoom)
    else:
        self._previewWeb.setTextSizeMultiplier(current_zoom)

aqt.browser.Browser._openPreview = wrap(
    aqt.browser.Browser._openPreview, openPreview)


def browserInit(self, mw):
    # self.form.setupUi
    current_zoom = deck_browser_current_zoom

    if ZOOM_IMAGES:
        self.form.tree.setZoomFactor(current_zoom)
    else:
        self.form.tree.setTextSizeMultiplier(current_zoom)


# aqt.browser.Browser.__init__ = wrap(
#   aqt.browser.Browser.__init__, browserInit )

if os.path.exists(os.path.join(mw.pm.addonFolder(), 'Zoom.py')):
    showCritical(
        'Найдено старое дополнение <b>Zoom</b> <br><br>' +
        ' Оно несовместимо с новым дополнением <i>_Zooming</i><br>' +
        ' &nbsp; Для нормальной работы:<br>' +
        ' &nbsp;  &nbsp; - удалите старое дополнение<br>' +
        '  &nbsp; &nbsp; &nbsp; - перезапустите Anki.' if lang == 'ru'
        else 'The old version of <b>Zoom</b> add-on <br><br>' +
        ' is incompatible with new edition of <i>_Zooming</i>. <br>' +
        ' Please, remove old file and restart Anki.')
