# -*- mode: Python ; coding: utf-8 -*-
# • Zooming
# https://ankiweb.net/shared/info/1071179937
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 Zooms, unzooms, lets you set a 1:1 (100%)
  or initial (user defined) zoom level. It's pretty cool.
 Work with images as well as with texts.

 The image is enlarged up to a maximum of 95% of the height or width
  of the card's window.

 Zoom in or out with Ctrl++/Ctrl+-
 or with Ctrl+mouse wheel
 or with the View/Zoom submenu.
"""
from __future__ import division
from __future__ import unicode_literals
import os
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import anki
import aqt

from aqt.qt import *
# import aqt.browser

# Get language class
# import anki.lang
lang = anki.lang.getLang()

MSG = {
    'en': {
        'later': _('later'),
        'View': _('&View'),
        'restartAnki': 'Please, <b>restart Anki</b><br> to apply changes.',
        'Zoom': _('&Zoom'),
        'zoom_info': _('Zoom In&fo'),
        'zoom_images': _('&Zoom Images'),
        'zoom_in': _('Zoom &In'),
        'zoom_out': _('Zoom &Out'),
        'zoom_reset': _('&Reset Initial'),
        'zoom_init': _('Reset'),
        'aa': _('About addon  '),
        },
    'ru': {
        'later': 'позже',
        'View': '&Вид',
        'restartAnki':
            'Чтобы изменения вступили в силу —<br>' +
            'пожалуйста, <b>перезапустите Anki</b>',
        'Zoom': 'Мас&штаб',
        'zoom_info': 'Масштаб &показать',
        'zoom_images': 'Масштаб &картинок менять',
        'zoom_in': 'Масштаб у&величить',
        'zoom_out': 'Масштаб у&меньшить',
        'zoom_reset': 'Масштаб на&чальный',
        'zoom_init': 'Масштаб',
        'aa': 'О дополнении  ',
        },
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

# 'Чтобы изменения вступили в силу —<br> пожалуйста, ' +
#   '<b>перезапустите Anki</b>' if lang == 'ru'
#   else 'Please, <b>restart Anki</b><br> to apply changes.'

# 'Мас&штаб' if lang == 'ru' else _('&Zoom')
# 'Масштаб &показать' if lang == 'ru' else _('Zoom In&fo')
# 'Масштаб &картинок менять' if lang == 'ru' else _('&Zoom Images')
# 'Масштаб у&величить' if lang == 'ru' else _('Zoom &In')
# 'Масштаб у&меньшить' if lang == 'ru' else _('Zoom &Out')
# 'Масштаб на&чальный ( =' if lang == 'ru' else _('&Reset Initial ')

HOTKEY = {  # in aqt.mw Main Window (deckBrowser, Overview, Reviewer)
    'zoom_info':    'Alt+0',
    'zoom_in':      'Ctrl++',
    'zoom_out':     'Ctrl+-',
    'zoom_reset':   'Ctrl+0',
    'zoom_init':    'Ctrl+Alt+0',
}

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

__addon__ = "'" + __name__.replace('_',' ')
__version__ = "2.0.44a"

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

try:
    MUSTHAVE_COLOR_ICONS = os.path.join(aqt.mw.pm.addonFolder(), 'handbook')
except:
    MUSTHAVE_COLOR_ICONS = ''


def changeFont():
    f = QFontInfo(QFont(FONT))
    ws = QWebSettings.globalSettings()
    aqt.mw.fontHeight = FONTSIZE if FONTSIZE else f.pixelSize()
    aqt.mw.fontFamily = f.family()
    aqt.mw.fontHeightDelta = max(0, aqt.mw.fontHeight - 13)
    ws.setFontFamily(QWebSettings.StandardFont, aqt.mw.fontFamily)
    ws.setFontSize(QWebSettings.DefaultFontSize, aqt.mw.fontHeight)
    aqt.mw.reset()

if FONT or FONTSIZE:
    changeFont()

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
    """Increase the text size."""
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    if not step:
        step = zoom_step

    if 'deckBrowser' == aqt.mw.state:
        # deck_browser_current_zoom = \
        #    round(deck_browser_current_zoom * zoom_step, 1)
        deck_browser_current_zoom = round(
            deck_browser_current_zoom + zoom_step, 1)
        current_zoom = deck_browser_current_zoom
    if 'overview' == aqt.mw.state or 'requestRequired' == aqt.mw.state:
        overview_current_zoom = round(overview_current_zoom + zoom_step, 1)
        current_zoom = overview_current_zoom
    if 'review' == aqt.mw.state:
        reviewer_current_zoom = round(reviewer_current_zoom + zoom_step, 1)
        current_zoom = reviewer_current_zoom

    if ZOOM_IMAGES:
        aqt.mw.web.setZoomFactor(current_zoom)
    else:
        aqt.mw.web.setTextSizeMultiplier(current_zoom)


def zoom_out(step=None):
    '''Decrease the text size.'''
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    if not step:
        step = zoom_step

    if 'deckBrowser' == aqt.mw.state:
        # deck_browser_current_zoom = \
        #    round(deck_browser_current_zoom / zoom_step, 1)
        deck_browser_current_zoom = max(.1, round(
            deck_browser_current_zoom - zoom_step, 1))
        current_zoom = deck_browser_current_zoom
    if 'overview' == aqt.mw.state or 'requestRequired' == aqt.mw.state:
        overview_current_zoom = max(.1, round(
            overview_current_zoom - zoom_step, 1))
        current_zoom = overview_current_zoom
    if 'review' == aqt.mw.state:
        reviewer_current_zoom = max(.1, round(
            reviewer_current_zoom - zoom_step, 1))
        current_zoom = reviewer_current_zoom

    if ZOOM_IMAGES:
        aqt.mw.web.setZoomFactor(current_zoom)
    else:
        aqt.mw.web.setTextSizeMultiplier(current_zoom)


def zoom_init(state=None, *args):
    """Init the text size."""
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    current_zoom = 1.0

    deck_browser_current_zoom = 1.0
    overview_current_zoom = 1.0
    reviewer_current_zoom = 1.0

    if ZOOM_IMAGES:
        aqt.mw.web.setZoomFactor(current_zoom)
    else:
        aqt.mw.web.setTextSizeMultiplier(current_zoom)


def zoom_reset(state=None, *args):
    '''Reset the text size.'''
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    current_zoom = 1.0

    if 'deckBrowser' == aqt.mw.state:
        current_zoom = deck_browser_standard_zoom
    if 'overview' == aqt.mw.state or 'requestRequired' == aqt.mw.state:
        current_zoom = overview_standard_zoom
    if 'review' == aqt.mw.state:
        current_zoom = reviewer_standard_zoom
    reset_current_zoom()

    if ZOOM_IMAGES:
        aqt.mw.web.setZoomFactor(current_zoom)
    else:
        aqt.mw.web.setTextSizeMultiplier(current_zoom)


def current_reset_zoom(state=None, *args):
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom
    current_zoom = 1

    if 'deckBrowser' == aqt.mw.state:
        current_zoom = deck_browser_current_zoom
    if 'overview' == aqt.mw.state or 'requestRequired' == aqt.mw.state:
        current_zoom = overview_current_zoom
    if 'review' == aqt.mw.state:
        current_zoom = reviewer_current_zoom

    if ZOOM_IMAGES:
        aqt.mw.web.setZoomFactor(current_zoom)
    else:
        aqt.mw.web.setTextSizeMultiplier(current_zoom)


def zoom_info():
    aqt.utils.showText(
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
        str(aqt.mw.web.textSizeMultiplier()) + '</b></td></tr>' +
        '<tr><td align=right>zoomFactor = </td><td><b>' +
        str(aqt.mw.web.zoomFactor()) + '</b></td></tr>' +
        '</tbody></table>', type='HTML')


def zoom_images(act):
    global ZOOM_IMAGES
    ZOOM_IMAGES = act.isChecked()
    if ZOOM_IMAGES:
        aqt.utils.showWarning(MSG[lang]['restartAnki'])
    current_reset_zoom()

try:
    aqt.mw.addon_view_menu
except AttributeError:
    aqt.mw.addon_view_menu = QMenu(MSG[lang]['View'], aqt.mw.menuBar())
    aqt.mw.form.menubar.insertMenu(
        aqt.mw.form.menuTools.menuAction(), aqt.mw.addon_view_menu)

zoom_images_action = None  # global


def zoom_setup_menu():
    global zoom_images_action

    aqt.mw.zoom_submenu = QMenu(MSG[lang]['Zoom'], aqt.mw.menuBar())
    aqt.mw.zoom_submenu.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'zoom.png')))

    zoom_info_action = QAction(MSG[lang]['zoom_info'], aqt.mw)
    # Ctrl+Shift+0 doesn't work on NumPad
    zoom_info_action.setShortcut(QKeySequence(HOTKEY['zoom_info']))
    aqt.mw.connect(zoom_info_action, SIGNAL('triggered()'), zoom_info)

    zoom_images_action = QAction(MSG[lang]['zoom_images'], aqt.mw)
    # zoom_images_action.setShortcut(QKeySequence(HOTKEY['zoom_images']))
    zoom_images_action.setCheckable(True)
    zoom_images_action.setChecked(ZOOM_IMAGES)
    aqt.mw.connect(zoom_images_action, SIGNAL('triggered()'),
               lambda AKT=zoom_images_action: zoom_images(AKT))

    zoom_in_action = QAction(MSG[lang]['zoom_in'], aqt.mw)
    zoom_in_action.setShortcut(QKeySequence(HOTKEY['zoom_in']))
    zoom_in_action.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'zoom_in.png')))
    aqt.mw.connect(zoom_in_action, SIGNAL('triggered()'), zoom_in)

    zoom_out_action = QAction(MSG[lang]['zoom_out'], aqt.mw)
    zoom_out_action.setShortcut(QKeySequence(HOTKEY['zoom_out']))
    zoom_out_action.setIcon(
        QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'zoom_out.png')))
    aqt.mw.connect(zoom_out_action, SIGNAL('triggered()'), zoom_out)

    reset_zoom_action = QAction(
        MSG[lang]['zoom_reset'] +
        ' ( =' + str(deck_browser_standard_zoom) + ' =' +
        str(overview_standard_zoom) + ' =' +
        str(reviewer_standard_zoom) + ' )', aqt.mw)
    # Shift+0 does not work on NumPad
    reset_zoom_action.setShortcut(QKeySequence(HOTKEY['zoom_reset']))
    aqt.mw.connect(reset_zoom_action, SIGNAL('triggered()'), zoom_reset)

    reset_zoom_init_action = QAction(
        MSG[lang]['zoom_init'] +
        ' &1:1 100% ( =1.0 =1.0 =1.0 )', aqt.mw)
    reset_zoom_init_action.setShortcut(QKeySequence(HOTKEY['zoom_init']))
    aqt.mw.connect(reset_zoom_init_action, SIGNAL('triggered()'), zoom_init)

    if hasattr(aqt.mw, 'addon_view_menu'):
        aqt.mw.addon_view_menu.addMenu(aqt.mw.zoom_submenu)
        aqt.mw.zoom_submenu.addAction(zoom_info_action)
        aqt.mw.zoom_submenu.addAction(zoom_images_action)
        aqt.mw.zoom_submenu.addSeparator()
        aqt.mw.zoom_submenu.addAction(zoom_in_action)
        aqt.mw.zoom_submenu.addAction(zoom_out_action)
        aqt.mw.zoom_submenu.addSeparator()
        if deck_browser_standard_zoom != 1.0 or \
           overview_standard_zoom != 1.0 or \
           reviewer_standard_zoom != 1.0:
            aqt.mw.zoom_submenu.addAction(reset_zoom_action)
        aqt.mw.zoom_submenu.addAction(reset_zoom_init_action)

    def about_addon():
        """
        Show "About addon" message popup window.
        """
        aa_about_box = QMessageBox()
        aa_about_box.setText(
            __addon__ + "   " + __version__ + "\n" + __doc__)
        aa_width, aa_height = (1024, 768)
        # aa_width, aa_height = (1920, 1080)
        aa_left = (aa_width-480)/2
        aa_right = (aa_height-640)/2
        aa_about_box.setGeometry(aa_left, aa_right, 480, 640)
        aa_about_box.setWindowTitle(MSG[lang]['aa'] + __addon__)
        aa_about_box.exec_()

    about_addon_action = QAction(MSG[lang]['aa'] + __addon__, aqt.mw)
    aqt.mw.connect(about_addon_action, SIGNAL('triggered()'), about_addon)
    aqt.mw.zoom_submenu.addSeparator()
    aqt.mw.zoom_submenu.addAction(about_addon_action)

##


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
    anki.hooks.runHook('movedToState', state)

aqt.mw.moveToState = anki.hooks.wrap(aqt.mw.moveToState, run_move_to_state_hook)
anki.hooks.addHook('movedToState', current_reset_zoom)
original_mw_web_wheelEvent = aqt.mw.web.wheelEvent
aqt.mw.web.wheelEvent = handle_wheel_event

zoom_setup_menu()

##


def save_toolbarz_visible():
    aqt.mw.pm.profile['ctb_deck_browser_zoom'] = deck_browser_current_zoom
    aqt.mw.pm.profile['ctb_overview_zoom'] = overview_current_zoom
    aqt.mw.pm.profile['ctb_reviewer_zoom'] = reviewer_current_zoom
    aqt.mw.pm.profile['ctb_images_zoom'] = ZOOM_IMAGES


def load_toolbarz_visible():
    global deck_browser_current_zoom, overview_current_zoom,\
        reviewer_current_zoom, zoom_images_action, ZOOM_IMAGES

    try:
        key_value = aqt.mw.pm.profile['ctb_deck_browser_zoom']
        deck_browser_current_zoom = key_value
    except KeyError:
        pass
    #    deck_browser_current_zoom = deck_browser_standard_zoom

    try:
        key_value = aqt.mw.pm.profile['ctb_overview_zoom']
        overview_current_zoom = key_value
    except KeyError:
        pass
    #   overview_current_zoom = overview_standard_zoom

    try:
        key_value = aqt.mw.pm.profile['ctb_reviewer_zoom']
        reviewer_current_zoom = key_value
    except KeyError:
        pass
    #   reviewer_current_zoom = reviewer_standard_zoom

    try:
        key_value = aqt.mw.pm.profile['ctb_images_zoom']
        ZOOM_IMAGES = key_value
    except KeyError:
        pass

    zoom_images_action.setChecked(ZOOM_IMAGES)
    current_reset_zoom()

anki.hooks.addHook('unloadProfile', save_toolbarz_visible)
anki.hooks.addHook('profileLoaded', load_toolbarz_visible)

##


def openPreview(self):
    current_zoom = reviewer_current_zoom

    if ZOOM_IMAGES:
        # self._previewWindow.setZoomFactor(current_zoom)
        # AttributeError: 'QDialog' object has no attribute 'setZoomFactor'
        self._previewWeb.setZoomFactor(current_zoom)
    else:
        self._previewWeb.setTextSizeMultiplier(current_zoom)

aqt.browser.Browser._openPreview = anki.hooks.wrap(
    aqt.browser.Browser._openPreview, openPreview)


##

old_addons = (
    'Zoom.py',
)

old_addons2delete = ''
for old_addon in old_addons:
    if len(old_addon) > 0:
        old_filename = os.path.join(aqt.mw.pm.addonFolder(), old_addon)
        if os.path.exists(old_filename):
            old_addons2delete += old_addon[:-3] + ' \n'

if old_addons2delete != '':
    if lang == 'ru':
        aqt.utils.showText(
            'В каталоге\n\n ' + aqt.mw.pm.addonFolder() +
            '\n\nнайдены дополнения, которые уже включены в дополнение\n ' +
            os.path.basename(__file__) + '\n' +
            'и поэтому будут конфликтовать с ним.\n\n' +
            old_addons2delete +
            '\nПереименуйте (добавьте расширение .off) ' +
            '\n или удалите эти дополнения ' +
            '\n   и перезапустите Anki.')
    else:
        aqt.utils.showText(
            'There are some add-ons in the folder \n\n ' +
            aqt.mw.pm.addonFolder() + '\n\n' +
            old_addons2delete +
            '\n\nThey are already part of this addon,\n ' +
            os.path.basename(__file__) +
            '\n\nPlease, rename them (add .off extension to file)' +
            ' or delete\n and restart Anki.')
