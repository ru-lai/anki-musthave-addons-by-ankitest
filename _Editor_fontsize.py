# -*- mode: Python ; coding: utf-8 -*-
# • Editor fontsize
# https://ankiweb.net/shared/info/1931469441
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 Increase Text Size for Card Types Editor and so on.

 TODO: Some description should be here!!!

 HTML Editor saves width and height on exit.
 Also do Addons Editor.

 Decks, Note Types and Tags in Browser Tree could be collapsed too.

 Expand/Collapse Whole Browser Tree
"""
from __future__ import unicode_literals
from __future__ import division
import os
import sys
import datetime
from operator import itemgetter

import PyQt4.QtGui
import PyQt4.QtCore

from aqt import mw
from aqt.qt import *

import aqt.addons
import aqt.browser
import aqt.clayout
import aqt.deckconf
import aqt.editor
import aqt.fields
import aqt.models
import aqt.utils

import anki.hooks

from BeautifulSoup import BeautifulSoup

from anki.consts import *

from aqt.webview import AnkiWebView
from aqt.editor import Editor  # the editor when you click 'Add' in Anki
from aqt.utils import saveGeom, restoreGeom

#####################
# Get language class
# Выбранный пользователем язык программной оболочки
import anki.lang
lang = anki.lang.getLang()

MSG = {
    'en': {
        'later': _('later'),
        'not now': _('not now'),
        'Cards': _('&Cards'),
        'View': _('&View'),
        'Go': _('&Go'),
        'Edit': _('&Edit...'),
        'Edit Layout': _('Edi&t Layout...'),
        'Edit Fields': _('Edit &Fields...'),
        'Added': _('Added Yesterday'),
        'Studied': _('Studied Yesterday'),
        'Again': _('Again Yesterday'),
        'Buried': _('Buried'),
        'Rootage': _('Rootage'),
        'Studied cards': _('Studied cards'),
        'Search help': _('Search help'),
        'Save here': _('Save your searches here'),
        'ExpandThemAll': _('Expand Them All'),
        'CollapseThemAll': _('Collapse Them All'),
        'CollapseThemAtAll': _('Collapse Them at All'),
        },
    'ru': {
        'later': 'позже',
        'not now': 'не сейчас',
        'Cards': '&Карточки',
        'View': '&Вид',
        'Go': 'П&ереход',
        'Edit': 'Ре&дактирование...',
        'Edit Layout': '&Шаблоны карточек...',
        'Edit Fields': '&Список полей...',
        'Added': 'Добавленные вчера',
        'Studied': 'Просмотрено вчера',
        'Again': 'Не вспомненные вчера',
        'Buried': 'Отложенные',
        'Rootage': 'Коренные',
        'Studied cards': 'Оценки ответов',
        'Search help': 'Подсказки по поиску',
        'Save here': 'Сохранять здесь',
        'ExpandThemAll': 'Развернуть всё &дерево',
        'CollapseThemAll': 'Свернуть все &ветки',
        'CollapseThemAtAll': 'Свернуть вообще всё',
        },
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

#         ('Добавленные вчера' if lang == 'ru' else _('Added Yesterday'),
#         ('Просмотрено вчера' if lang == 'ru' else _('Studied Yesterday'),
#         ('Не вспомненные вчера' if lang == 'ru' else _('Again Yesterday'),
# 'Отложенные' if lang == 'ru' else _('Buried')
# 'Коренные' if lang == 'ru' else _('Rootage')
# 'Оценки ответов' if lang == 'ru' else _('Studied cards')
# 'Подсказки по поиску' if lang == 'ru' else _('Search help')
# 'Сохранять здесь' if lang == 'ru' else _('Save your searches here')
# 'Свернуть вообще всё' if lang ==
#       'ru' else _('Collapse Them at All')

# You can set up your own hotkeys here:
HOTKEY = {      # in Reviewer
    'ExpandThemAll': 'Ctrl+Shift++',
    'CollapseThemAll': 'Ctrl+Shift+-',
    'CollapseThemAtAll': 'Ctrl+Alt+Shift+-',
    'Edit_HTML': 'F4',         # Ctrl+Shift+X
    'Edit_Fields': 'F4',         # e
    'Edit_Cards': 'Shift+F4',   #
    'Edit_Fieldz': 'Ctrl+F4',    # Alt+F4 == Close Window
}

BrowserColumns = True  # if you want to enlarge ALL columns in browser
# BrowserColumns = False # to enlarge 'Sort Field', 'Question', 'Answer' only

FONTS = {
    # {{}} height of curly braces is near font's height in pixels
    #  (Why not exact? It's font dependant).

    # ('Arial', 11) is Anki's default setup. Or 12?

    # To change only fontsize use
    #  (None, 14),

    # To change only typeface use
    #  ('Calibri', 0),

    # To switch off both particular typeface and fontsize setup
    #  you need to comment it's line
    #   (just use # sharp at the very beginning)

    # 'Force custom font':  (None, 0),
    'Force custom font':  ('Calibri', 14),
    # 'Force custom font':  ('Times New Roman', 16),

    'Menu':    ('Comic Sans MS', 15),
    # 'Menu':    ('Comic Sans MS', 0),
    # 'Menu':    (None, 14),
    # 'Menu':    (None, 0),

    'Front Template':   ('Courier New', 16),
    'Styling':          ('Courier New', 16),
    'Back Template':    ('Courier New', 16),

    'HTML Editor':      ('Courier New', 18),

    'Add-ons Edit...':  ('Calibri', 16),
    'showText':         ('Calibri', 16),

    'Browser Search':       ('Verdana', 14),
    'Browser Columns':      ('Courier New', 16),

    'Browser sysTree':      ('Calibri', 18),
    'Browser favTree':      ('Calibri', 18),
    'Browser deckTree':     ('Calibri', 20),
    'Browser noteTree':     ('Calibri', 18),
    'Browser tagTree':      ('Calibri', 16),

    'Fields List':          ('Consolas', 18),
}

__addon__ = "'" + __name__.replace('_', ' ')
__version__ = "2.0.44a"

if __name__ == '__main__':
    print("This is _F4_Edit add-on for the Anki program " +
          "and it can't be run directly.")
    print('Please download Anki 2.0 from http://ankisrs.net/')
    sys.exit()
else:
    pass

if sys.version[0] == '2':  # Python 3 is utf8 only already.
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf8')

try:
    MUSTHAVE_COLOR_ICONS = os.path.join(mw.pm.addonFolder(), 'handbook')
except:
    MUSTHAVE_COLOR_ICONS = ''

##

editor_standard_zoom = 1.5


def changeEditorFontSize(self):
    return [(f['font'], f['size'] * editor_standard_zoom, f['rtl'])
            for f in self.note.model()['flds']]

aqt.editor.Editor.fonts = anki.hooks.wrap(
    aqt.editor.Editor.fonts, changeEditorFontSize)

##

old_addons = (
    '_Collapse_Them_All.py',
    '_F4_Edit.py',
)

old_addons2delete = ''
for old_addon in old_addons:
    if len(old_addon) > 0:
        old_filename = os.path.join(mw.pm.addonFolder(), old_addon)
        if os.path.exists(old_filename):
            old_addons2delete += old_addon[:-3] + ' \n'

if old_addons2delete != '':
    if lang == 'ru':
        aqt.utils.showText(
            'В каталоге\n\n ' + mw.pm.addonFolder() +
            '\n\nнайдены дополнения, которые уже включены в дополнение\n' +
            ' Editor fontsize  \n' +
            'и поэтому будут конфликтовать с ним.\n\n' +
            old_addons2delete +
            '\nУдалите эти дополнения и перезапустите Anki.')
    else:
        aqt.utils.showText(
            '<big>There are some add-ons in the folder <br>\n<br>\n' +
            ' &nbsp; ' + mw.pm.addonFolder() +
            '<pre>' + old_addons2delete + '</pre>' +
            'They are already part of<br>\n' +
            ' <b> &nbsp; Editor fontsize</b>' +
            ' addon.<br>\n' +
            'Please, delete them and restart Anki.</big>', type="html")
##


def particularFont(fontKey, bold=False, italic=False, underline=False):
    font = PyQt4.QtGui.QFont()
    if fontKey in FONTS:
        if FONTS[fontKey][0] is not None:
            font.setFamily(FONTS[fontKey][0])
        fontsize = int(FONTS[fontKey][1])
        if fontsize > 0:
            font.setPixelSize(fontsize)
            # font.setPointSize(fontsize)
        font.setBold(bold)
        font.setItalic(italic)
        font.setUnderline(underline)
    return font

# Force Custom Font
# https://ankiweb.net/shared/info/2103013902
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


def changeFont():
    f = QFontInfo(particularFont('Force custom font'))
    ws = QWebSettings.globalSettings()
    mw.fontHeight = f.pixelSize()
    mw.fontFamily = f.family()
    mw.fontHeightDelta = max(0, mw.fontHeight - 13)
    ws.setFontFamily(QWebSettings.StandardFont, mw.fontFamily)
    ws.setFontSize(QWebSettings.DefaultFontSize, mw.fontHeight)
    mw.reset()

changeFont()

# Cards... Style and Templates editing
######################################################################


def myReadCard(self):

    self.tab['tform'].front.setFont(particularFont('Front Template'))
    self.tab['tform'].css.setFont(particularFont('Styling'))
    self.tab['tform'].back.setFont(particularFont('Back Template'))

    t = self.card.template()
    self.redrawing = True
    self.tab['tform'].front.setPlainText(t['qfmt'])
    self.tab['tform'].css.setPlainText(self.model['css'])
    self.tab['tform'].back.setPlainText(t['afmt'])
    self.tab['tform'].front.setAcceptRichText(False)
    self.tab['tform'].css.setAcceptRichText(False)
    self.tab['tform'].back.setAcceptRichText(False)
    self.tab['tform'].front.setTabStopWidth(30)
    self.tab['tform'].css.setTabStopWidth(30)
    self.tab['tform'].back.setTabStopWidth(30)
    self.redrawing = False

aqt.clayout.CardLayout.readCard = myReadCard

#
##########################################################

F4_Edit_exists = os.path.exists(
    os.path.join(mw.pm.addonFolder(), '_F4_Edit.py'))


def go_edit_current():
    """Edit the current card when there is one."""
    try:
        mw.onEditCurrent()
    except AttributeError:
        pass


def go_edit_layout():
    """Edit the current card's note's layout if there is one."""
    try:
        ccard = mw.reviewer.card
        aqt.clayout.CardLayout(mw, ccard.note(), ord=ccard.ord)
    except AttributeError:
        return


def go_edit_fields():
    """Edit the current card's note's fields if there is one."""
    # try:
    # ccard = mw.reviewer.card
    aqt.editor.onFields(mw)
    # except AttributeError:
    # return

try:
    mw.addon_cards_menu
except AttributeError:
    mw.addon_cards_menu = QMenu(MSG[lang]['Cards'], mw.menuBar())
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(), mw.addon_cards_menu)

F4_edit_current_action = QAction(mw)
F4_edit_current_action.setText(MSG[lang]['Edit'])
F4_edit_current_action.setIcon(
    QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_current.png')))
F4_edit_current_action.setShortcut(QKeySequence(HOTKEY['Edit_Fields']))
F4_edit_current_action.setEnabled(False)

F4_edit_layout_action = QAction(mw)
F4_edit_layout_action.setText(MSG[lang]['Edit Layout'])
F4_edit_layout_action.setIcon(
    QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_layout.png')))
F4_edit_layout_action.setShortcut(QKeySequence(HOTKEY['Edit_Cards']))
F4_edit_layout_action.setEnabled(False)

F4_edit_fields_action = QAction(mw)
F4_edit_fields_action.setText(MSG[lang]['Edit Fields'])
F4_edit_fields_action.setIcon(
    QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_fields.png')))
F4_edit_fields_action.setShortcut(QKeySequence(HOTKEY['Edit_Fieldz']))
F4_edit_fields_action.setEnabled(False)


def swap_off():
    F4_edit_current_action.setEnabled(False)
    F4_edit_layout_action.setEnabled(False)
    F4_edit_fields_action.setEnabled(False)


def swap_on():
    F4_edit_current_action.setEnabled(True)
    F4_edit_layout_action.setEnabled(True)
    F4_edit_fields_action.setEnabled(True)


def onFields(self):
    from aqt.fields import FieldDialog
    FieldDialog(self, self.card.note(), parent=mw)

if not F4_Edit_exists:
    mw.connect(F4_edit_current_action, SIGNAL('triggered()'), go_edit_current)
    mw.connect(F4_edit_layout_action, SIGNAL('triggered()'), go_edit_layout)
    mw.connect(F4_edit_fields_action, SIGNAL(
        'triggered()'), lambda: onFields(mw.reviewer))

    mw.addon_cards_menu.addSeparator()
    mw.addon_cards_menu.addAction(F4_edit_current_action)
    mw.addon_cards_menu.addAction(F4_edit_layout_action)
    mw.addon_cards_menu.addAction(F4_edit_fields_action)
    mw.addon_cards_menu.addSeparator()

    mw.deckBrowser.show = anki.hooks.wrap(mw.deckBrowser.show, swap_off)
    mw.overview.show = anki.hooks.wrap(mw.overview.show, swap_off)
    mw.reviewer.show = anki.hooks.wrap(mw.reviewer.show, swap_on)

# HTML editing
######################################################################


def myHtmlEdit(self):
    self.saveNow()
    d = PyQt4.QtGui.QDialog(self.widget)
    form = aqt.forms.edithtml.Ui_Dialog()
    form.setupUi(d)
    d.connect(form.buttonBox, PyQt4.QtCore.SIGNAL('helpRequested()'),
              lambda: aqt.utils.openHelp('editor'))
    aqt.utils.restoreGeom(d, 'HTMLedit')

    form.textEdit.setFont(particularFont('HTML Editor'))
    form.textEdit.setPlainText(self.note.fields[self.currentField])

    form.textEdit.moveCursor(PyQt4.QtGui.QTextCursor.End)
    d.exec_()
    aqt.utils.saveGeom(d, 'HTMLedit')
    html = form.textEdit.toPlainText()
    # filter html through beautifulsoup so we can strip out things
    # like a leading </div>
    html = unicode(BeautifulSoup(html))
    self.note.fields[self.currentField] = html
    self.loadNote()
    # focus field so it's saved
    self.web.setFocus()
    self.web.eval('focusField(%d);' % self.currentField)

# F4 as well as Ctrl+Shift+X
######################################################################


def mySetupF4(self):
    f4 = PyQt4.QtGui.QShortcut(
        PyQt4.QtGui.QKeySequence(HOTKEY['Edit_HTML']), self.parentWindow)
    f4.connect(f4, PyQt4.QtCore.SIGNAL('activated()'), self.onHtmlEdit)

    s = QShortcut(QKeySequence(HOTKEY['Edit_Cards']), self.widget)
    s.connect(s, SIGNAL("activated()"), self.onCardLayout)

    ss = QShortcut(QKeySequence(HOTKEY['Edit_Fieldz']), self.widget)
    ss.connect(ss, SIGNAL("activated()"), self.onFields)

if not F4_Edit_exists:
    aqt.editor.Editor.onHtmlEdit = myHtmlEdit
    aqt.editor.Editor.setupButtons = anki.hooks.wrap(
        aqt.editor.Editor.setupButtons, mySetupF4)

# Addons Edit...
######################################################################


def myEdit(self, path):
    d = PyQt4.QtGui.QDialog(self.mw)
    frm = aqt.forms.editaddon.Ui_Dialog()
    frm.setupUi(d)
    d.setWindowTitle(os.path.basename(path))

    frm.text.setFont(particularFont('Add-ons Edit...'))
    frm.text.setPlainText(unicode(open(path).read(), 'utf8'))
    aqt.utils.restoreGeom(d, 'AddonEditor')

    d.connect(frm.buttonBox, PyQt4.QtCore.SIGNAL('accepted()'),
              lambda: self.onAcceptEdit(path, frm))
    d.exec_()
    aqt.utils.saveGeom(d, 'AddonEditor')

aqt.addons.AddonManager.onEdit = myEdit

# showText with title=,minWidth=,minHeight= key parameters
######################################################################


def showTextik(txt, parent=None, type='text', run=True, geomKey=None,
               minWidth=500, minHeight=400, title=''):
    if not parent:
        parent = aqt.mw.app.activeWindow() or aqt.mw
    diag = PyQt4.QtGui.QDialog(parent)
    diag.setWindowTitle('Anki ' + title)
    layout = PyQt4.QtGui.QVBoxLayout(diag)
    diag.setLayout(layout)

    text = PyQt4.QtGui.QTextEdit()
    text.setReadOnly(True)

    text.setFont(particularFont('showText'))
    if type == 'text':
        text.setPlainText(txt)
    else:
        text.setHtml(txt)

    layout.addWidget(text)
    box = PyQt4.QtGui.QDialogButtonBox(PyQt4.QtGui.QDialogButtonBox.Close)
    layout.addWidget(box)

    def onReject():
        if geomKey:
            aqt.utils.saveGeom(diag, geomKey)
        PyQt4.QtGui.QDialog.reject(diag)

    diag.connect(box, PyQt4.QtCore.SIGNAL('rejected()'), onReject)
    diag.setMinimumHeight(minHeight)
    diag.setMinimumWidth(minWidth)
    if geomKey:
        restoreGeom(diag, geomKey)
    if run:
        diag.exec_()
    else:
        return diag, box

aqt.utils.showText = showTextik

'''
    try:
      showText(yourText, type='HTML',
               minHeight=150, minWidth=450, title='• Your title')
    except TypeError:
      showText(yourText, type='HTML')
'''

# Is there a way to increase the size of text in the Search bar?
######################################################################


def onBrowserSearch(self, reset=True):
    'Careful: if reset is true, the current note is saved.'
    txt = unicode(self.form.searchEdit.lineEdit().text()).strip()
    prompt = _('<type here to search; hit enter to show current deck>')
    sh = self.mw.pm.profile['searchHistory']
    # update search history
    if txt in sh:
        sh.remove(txt)
    sh.insert(0, txt)
    sh = sh[:30]
    self.form.searchEdit.clear()
    self.form.searchEdit.addItems(sh)
    self.mw.pm.profile['searchHistory'] = sh

    self.form.searchEdit.lineEdit().setFont(
        particularFont('Browser Search', bold=True))

    if self.mw.state == 'review' and 'is:current' in txt:
        # search for current card, but set search to easily display whole
        # deck
        if reset:
            self.model.beginReset()
            self.model.focusedCard = self.mw.reviewer.card.id
        self.model.search('nid:%d' % self.mw.reviewer.card.nid, False)
        if reset:
            self.model.endReset()
        self.form.searchEdit.lineEdit().setText(prompt)
        self.form.searchEdit.lineEdit().selectAll()
        return
    elif 'is:current' in txt:
        self.form.searchEdit.lineEdit().setText(prompt)
        self.form.searchEdit.lineEdit().selectAll()
    elif txt == prompt:
        self.form.searchEdit.lineEdit().setText('deck:current ')
        txt = 'deck:current '

    self.model.search(txt, reset)
    if not self.model.cards:
        # no row change will fire
        self.onRowChanged(None, None)
    elif self.mw.state == 'review':
        self.focusCid(self.mw.reviewer.card.id)

aqt.browser.Browser.onSearch = onBrowserSearch

# There is a way to increase the size of an each column in the Browser
######################################################################


def allData(self, index, role):
    if not index.isValid():
        return
    if role == Qt.FontRole:
        if not BrowserColumns:
            if self.activeCols[index.column()] not in (
                    'question', 'answer', 'noteFld'):
                return
        f = particularFont('Browser Columns')  # QFont()
        row = index.row()
        c = self.getCard(index)
        t = c.template()
        # f.setFamily(t.get('bfont', self.browser.mw.fontFamily))
        # f.setPixelSize(t.get('bsize', self.browser.mw.fontHeight))
        return f
    elif role == Qt.TextAlignmentRole:
        align = Qt.AlignVCenter
        if (self.activeCols[index.column()] not in (
                'question', 'answer', 'template', 'deck', 'noteFld', 'note')):
            align |= Qt.AlignHCenter
        return align
    elif role == Qt.DisplayRole or role == Qt.EditRole:
        return self.columnData(index)  # ??? TODO !!!
    else:
        return

aqt.browser.DataModel.data = allData

# Filter tree
######################################################################


def onClick(limb):
    if limb.isExpanded():
        limb.setExpanded(False)
    else:
        limb.setExpanded(True)


def _systemTagTree(self, root):
    tags = (
        (_('Whole Collection'), 'ankibw', ''),
        (_('Current Deck'), 'deck16', 'deck:current'),

        (_('Added Today'), 'view-calendar-tasks.png', 'added:1'),
        (_('Studied Today'), 'view-calendar-tasks.png', 'rated:1'),
        (_('Again Today'), 'view-calendar-tasks.png', 'rated:1:1'),

        (MSG[lang]['Added'],
         'view-pim-calendar.png', 'added:2 -added:1'),
        (MSG[lang]['Studied'],
         'view-pim-calendar.png', 'rated:2 -rated:1'),
        (MSG[lang]['Again'],
         'view-pim-calendar.png', 'rated:2:1 -rated:1:1'),

        (_('New'), 'plus16.png', 'is:new'),
        (_('Learning'), 'stock_new_template_red.png', 'is:learn'),
        (_('Relearn'), 'stock_new_template_red.png', 'is:learn is:review'),
        (_('Review'), 'clock16.png', 'is:review'),
        (_('Due'), 'clock-icon.png', 'is:due'),
        (_('Marked'), 'rating.png', 'tag:marked'),  # star16.png
        (MSG[lang]['Buried'],
         'media-playback-pause.png', 'is:buried'),
        (_('Suspended'), 'media-playback-pause.png', 'is:suspended'),
        (_('Leech'), 'emblem-important.png', 'tag:leech'),
        )

    def onCollapse():
        mw.col.conf['_collapseRootage'] = limb.isExpanded()

    limb = self.CallbackItem(
        root, MSG[lang]['Rootage'],
        lambda: onClick(limb), oncollapse=onCollapse)

    if '_collapseRootage' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseRootage'])
    else:
        limb.setExpanded(True)

    limb.setIcon(0, QIcon(':/icons/anki'))
    limb.setFont(0, particularFont('Browser sysTree', italic=True))

    for name, icon, cmd in tags:
        item = self.CallbackItem(
            limb, name, lambda c=cmd: self.setFilter(c))
        item.setIcon(0, QIcon(':/icons/' + icon))
        item.setFont(0, particularFont('Browser sysTree'))

    # almost never used, group these under 'Status'
    tags = (
        (_('Today (1) Again '),
         'view-calendar-tasks.png', 'rated:1:1 '),
        (_('Today (2) Hard '), 'view-calendar-tasks.png', 'rated:1:2 '),
        (_('Today (3) Good '), 'view-calendar-tasks.png', 'rated:1:3 '),
        (_('Today (4) Easy '),
         'view-calendar-tasks.png', 'rated:1:4 '),

        (_('Rescheduled Today'), 'clock-icon.png',
         datetime.datetime.now().strftime('tag:re*%y-%m-%d*')),
        (_('Rescheduled Yesterday'), 'clock16.png',
         (datetime.datetime.now() - datetime.timedelta(days=1)
          ).strftime('tag:re*%y-%m-%d*')),

        (_('Yesterday (1) Again '),
         'view-pim-calendar.png', 'rated:2:1 -rated:1:1'),
        (_('Yesterday (2) Hard '),
         'view-pim-calendar.png', 'rated:2:2 -rated:1:2 '),
        (_('Yesterday (3) Good '),
         'view-pim-calendar.png', 'rated:2:3 -rated:1:3 '),
        (_('Yesterday (4) Easy '),
         'view-pim-calendar.png', 'rated:2:4 -rated:1:4 '),

        (_('Last week Added '), 'spreadsheet.png', 'added:7 '),
        (_('Last week Studied '), 'spreadsheet.png', 'rated:7 '),

        (_('Last week (1) Again '),
         'go-first.png', 'rated:7:1 '),
        (_('Last week (2) Hard '), 'go-previous.png', 'rated:7:2 '),
        (_('Last week (3) Good '), 'go-next.png', 'rated:7:3 '),
        (_('Last week (4) Easy '),
         'go-last.png', 'rated:7:4 '),

        )

    def onCollaps():
        mw.col.conf['_collapsPast'] = past.isExpanded()

    past = self.CallbackItem(
        root, MSG[lang]['Studied cards'],
        lambda: onClick(past), oncollapse=onCollaps)

    if '_collapsPast' in mw.col.conf:
        past.setExpanded(mw.col.conf['_collapsPast'])
    else:
        past.setExpanded(False)

    past.setIcon(0, QIcon(":/icons/view-pim-calendar.png"))
    past.setFont(0, particularFont('Browser sysTree', italic=True))

    for name, icon, cmd in tags:
        item = self.CallbackItem(
            past, name, lambda c=cmd: self.setFilter(c))
        item.setIcon(0, QIcon(":/icons/" + icon))
        item.setFont(0, particularFont('Browser sysTree'))

    # almost never used, group these under 'Status'
    tags = (
        (_('Notes with no tags'), 'deletetag.png', 'tag:none '),

        (_('Filtered decks only'), 'deck16.png', 'deck:filtered '),
        (_('Normal decks only'), 'deck16.png', '-deck:filtered '),

        (_('Card 1'), 'stock_group.png', 'card:"Card 1" '),
        (_('First card'), 'stock_group.png', 'card:1 '),

        (_('review cards, not including lapsed cards '),
         'stock_new_template_red.png', '-is:learn is:review '),
        (_('cards that are in learning for the first time '),
         'stock_new_template_red.png', 'is:learn -is:review '),

        (_('Young'), 'green.png', 'prop:ivl<21 '),
        (_('Mature'), 'green.png', 'prop:ivl>20 '),

        (_('cards due tomorrow '), 'clock16.png', 'prop:due=1 '),
        (_('cards due yesterday that haven’t been answered yet '),
         'clock-icon.png', 'prop:due=-1 '),
        (_('cards due that haven’t been answered yet '),
         'clock16.png', 'prop:due<0 '),

        (_('cards due today'), 'help-hint.png', 'prop:due>-1 prop:due<1 '),
        (_('cards due now'), 'help-hint.png', 'prop:due=0 '),

        (_('Just Due'), 'clock-icon.png', 'is:due prop:due>-7 '),
        (_('Over Due'), 'clock16.png', 'is:due prop:due<=-7 '),

        (_('cards harder than default '),
         'kbugbuster.png', 'prop:ease<2.5 '),
        (_('cards easier than default '),
         'games-solve.png', 'prop:ease>2.5 '),
        (_('cards that have moved into relearning more than 3 times '),
         'kpersonalizer.png', 'prop:lapses>3 '),

        )

    status = self.CallbackItem(
        root, MSG[lang]['Search help'],
        lambda: onClick(status))

    status.setExpanded(False)

    status.setIcon(0, QIcon(":/icons/help.png"))
    status.setFont(0, particularFont('Browser sysTree', italic=True))

    for name, icon, cmd in tags:
        item = self.CallbackItem(
            status, name, lambda c=cmd: self.setFilter(c))
        item.setIcon(0, QIcon(":/icons/" + icon))
        item.setFont(0, particularFont('Browser sysTree'))

    return root


def _favTree(self, root):
    saved = self.col.conf.get('savedFilters', [])
    # if not saved:
    #    # Don't add favourites to tree if none saved
    #    return

    def onCollapse():
        mw.col.conf['_collapseFavorites'] = limb.isExpanded()
    limb = self.CallbackItem(root, _('My Searches'),
                             lambda: onClick(limb), oncollapse=onCollapse)
    if '_collapseFavorites' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseFavorites'])
    else:
        limb.setExpanded(True)
    limb.setIcon(0, QIcon(':/icons/emblem-favorite.png'))
    limb.setFont(0, particularFont('Browser favTree', italic=True))

    if saved:
        for name, filt in sorted(saved.items()):
            item = self.CallbackItem(
                limb, name, lambda s=filt: self.setFilter(s))
            item.setIcon(0, QIcon(':/icons/emblem-favorite-dark.png'))
            item.setFont(0, particularFont('Browser favTree', italic=True))
    else:
        name = MSG[lang]['Save here']
        filt = ''
        item = self.CallbackItem(
            limb, name, lambda s=filt: self.setFilter(s))
        item.setIcon(0, QIcon(':/icons/emblem-favorite-dark.png'))
        item.setFont(0, particularFont('Browser favTree', italic=True))


def _decksTree(self, root):
    def onCollapse():
        mw.col.conf['_collapseDecks'] = limb.isExpanded()
    limb = self.CallbackItem(root, _('Decks'),  # lambda: root.collapseAll(),
                             lambda: onClick(limb), oncollapse=onCollapse)
    if '_collapseDecks' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseDecks'])
    else:
        limb.setExpanded(True)
    limb.setIcon(0, QIcon(':/icons/stock_group.png'))
    limb.setFont(0, particularFont('Browser deckTree', italic=True))

    def fillGroups(root, grps, head=''):
        for g in grps:
            item = self.CallbackItem(
                root, g[0],
                lambda g=g: self.setFilter('deck', head + g[0]),
                lambda g=g: self.mw.col.decks.collapseBrowser(g[1]))
            item.setIcon(0, QIcon(':/icons/deck16.png'))
            item.setFont(0, particularFont('Browser deckTree'))
            newhead = head + g[0] + '::'
            collapsed = self.mw.col.decks.get(
                g[1]).get('browserCollapsed', False)
            item.setExpanded(not collapsed)
            fillGroups(item, g[5], newhead)
    fillGroups(limb, self.col.sched.deckDueTree())


def _modelTree(self, root):
    def onCollapse():
        mw.col.conf['_collapseNoteTypes'] = limb.isExpanded()
    limb = self.CallbackItem(root, _('Note Types'),
                             lambda: onClick(limb), oncollapse=onCollapse)
    if '_collapseNoteTypes' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseNoteTypes'])
    else:
        limb.setExpanded(True)
    limb.setIcon(0, QIcon(':/icons/package_games_card.png'))
    limb.setFont(0, particularFont('Browser noteTree', italic=True))
    for m in sorted(self.col.models.all(), key=itemgetter('name')):
        mitem = self.CallbackItem(
            limb, m['name'], lambda m=m: self.setFilter('mid', str(m['id'])))
        mitem.setIcon(0, QIcon(':/icons/product_design.png'))
        mitem.setFont(0, particularFont('Browser noteTree'))

# thanks to Patrice Neff http://patrice.ch/
# https://github.com/pneff/anki-hierarchical-tags
# https://ankiweb.net/shared/info/1089921461

HIERARCHICAL_TAGS = True
# HIERARCHICAL_TAGS = False

# Separator used between hierarchies
SEPARATOR = '::'


def _userTagTree(self, root):
    def onCollapse():
        mw.col.conf['_collapseTags'] = limb.isExpanded()

    limb = self.CallbackItem(
        root, _('Tags'),
        lambda: onClick(limb), oncollapse=onCollapse)

    if '_collapseTags' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseTags'])
    else:
        limb.setExpanded(True)

    limb.setIcon(0, QIcon(':/icons/addtag.png'))
    limb.setFont(0, particularFont('Browser tagTree', italic=True))

    tags_tree = {}
    for t in sorted(self.col.tags.all()):
        if t.lower() == 'marked' or t.lower() == 'leech':
            continue

        if HIERARCHICAL_TAGS:
            components = t.split(SEPARATOR)
            enum = enumerate(components)
            emax = len(components) - 1
            for idx, c in enum:
                partial_tag = SEPARATOR.join(components[0:idx + 1])
                if not tags_tree.get(partial_tag):
                    if idx == 0:
                        parent = limb
                    else:
                        parent_tag = SEPARATOR.join(components[0:idx])
                        parent = tags_tree[parent_tag]

                    item = self.CallbackItem(
                        parent, c,
                        lambda ptg=partial_tag: self.setFilter(
                            '(tag:"' + ptg + '::*" or tag:"' + ptg + '")'))

                    item.setIcon(0, QIcon(':/icons/anki-tag.png'))
                    item.setFont(0, particularFont('Browser tagTree'))

                    tags_tree[partial_tag] = item
        else:
            item = self.CallbackItem(
                limb, t, lambda t=t: self.setFilter('tag', t))
            item.setIcon(0, QIcon(':/icons/anki-tag.png'))
            item.setFont(0, particularFont('Browser tagTree'))

aqt.browser.Browser._systemTagTree = _systemTagTree
aqt.browser.Browser._favTree = _favTree
aqt.browser.Browser._decksTree = _decksTree
aqt.browser.Browser._modelTree = _modelTree
aqt.browser.Browser._userTagTree = _userTagTree


def setupMenu(self):
    menu = self.form.menuJump  # .menuEdit
    menu.addSeparator()

    a = menu.addAction(MSG[lang]['ExpandThemAll'])
    a.setShortcut(QKeySequence(HOTKEY['ExpandThemAll']))
    self.connect(a, PyQt4.QtCore.SIGNAL('triggered()'),
                 lambda b=self: ExpandThemAll(b, True, False))

    a = menu.addAction(MSG[lang]['CollapseThemAll'])
    a.setShortcut(QKeySequence(HOTKEY['CollapseThemAll']))
    self.connect(a, PyQt4.QtCore.SIGNAL('triggered()'),
                 lambda b=self: ExpandThemAll(b, False, False))

    a = menu.addAction(MSG[lang]['CollapseThemAtAll'])
    a.setShortcut(QKeySequence(HOTKEY['CollapseThemAtAll']))
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


# Fields List dialog window
def FieldDialog__init__(self, mw, note, ord=0, parent=None):
    QDialog.__init__(self, parent or mw)  # , Qt.Window)
    self.mw = aqt.mw
    self.parent = parent or mw
    self.note = note
    self.col = self.mw.col
    self.mm = self.mw.col.models
    self.model = note.model()
    self.mw.checkpoint(_('Fields'))
    self.form = aqt.forms.fields.Ui_Dialog()
    self.form.setupUi(self)
    self.setWindowTitle(_('Fields for %s') % self.model['name'])
    self.form.buttonBox.button(QDialogButtonBox.Help).setAutoDefault(False)
    self.form.buttonBox.button(QDialogButtonBox.Close).setAutoDefault(False)
    self.currentIdx = None
    self.oldSortField = self.model['sortf']
    self.fillFields()
    self.setupSignals()

    self.form.fieldList.setCurrentRow(0)
    self.form.fieldList.setFont(particularFont('Fields List'))

    aqt.utils.restoreGeom(self, 'fields', adjustSize=True)
    self.exec_()

aqt.fields.FieldDialog.__init__ = FieldDialog__init__


def reject(self):
    self.saveField()
    if self.oldSortField != self.model['sortf']:
        self.mw.progress.start()
        self.mw.col.updateFieldCache(self.mm.nids(self.model))
        self.mw.progress.finish()
    self.mm.save(self.model)
    self.mw.reset()
    aqt.utils.saveGeom(self, 'fields')
    QDialog.reject(self)


def accept(self):
    aqt.utils.saveGeom(self, 'fields')
    self.reject()

aqt.fields.FieldDialog.reject = reject
aqt.fields.FieldDialog.accept = accept


# Models
def updateModelsList(self):
    row = self.form.modelsList.currentRow()
    if row == -1:
        row = 0
    self.models = self.col.models.all()
    self.models.sort(key=itemgetter("name"))
    self.form.modelsList.clear()
    for m in self.models:
        mUse = self.mm.useCount(m)
        mUse = ngettext("%d note", "%d notes", mUse) % mUse
        item = QListWidgetItem("%s [%s]" % (m['name'], mUse))
        self.form.modelsList.addItem(item)
    self.form.modelsList.setCurrentRow(row)
    self.form.modelsList.setFont(particularFont('Fields List'))

aqt.models.Models.updateModelsList = updateModelsList


# Preview Answer / Preview Next by click Enter
#  (by default goPrev byLeftArrow goNext byRight Arrow)
def _openPreview(self):
    c = self.connect
    self._previewState = 'question'
    self._previewWindow = PyQt4.QtGui.QDialog(None, Qt.Window)
    self._previewWindow.setWindowTitle(_('Preview'))
    c(self._previewWindow, SIGNAL('finished(int)'), self._onPreviewFinished)

    vbox = QVBoxLayout()
    vbox.setMargin(0)
    self._previewWeb = AnkiWebView()
    vbox.addWidget(self._previewWeb)
    bbox = QDialogButtonBox()

    self._previewReplay = bbox.addButton(
        _('Replay Audio'), QDialogButtonBox.ActionRole)
    self._previewReplay.setAutoDefault(False)
    self._previewReplay.setShortcut(PyQt4.QtGui.QKeySequence('R'))
    self._previewReplay.setToolTip(_('Shortcut key: %s' % 'R'))

    self._previewPrev = bbox.addButton(
        '<', PyQt4.QtGui.QDialogButtonBox.ActionRole)
    self._previewPrev.setAutoDefault(False)
    self._previewPrev.setShortcut(PyQt4.QtGui.QKeySequence('Left'))
    self._previewPrev.setToolTip(_('Shortcut key: ← Left arrow ⇐ '))

    self._previewNext = bbox.addButton(
        '>', PyQt4.QtGui.QDialogButtonBox.ActionRole)
    self._previewNext.setAutoDefault(True)
    self._previewNext.setShortcut(PyQt4.QtGui.QKeySequence('Right'))
    self._previewNext.setToolTip(
        _('Shortcut key: → Right arrow ⇒ or Enter ↵ '))  # &crarr;

    c(self._previewPrev, PyQt4.QtCore.SIGNAL('clicked()'),
      self._onPreviewPrev)
    c(self._previewNext, PyQt4.QtCore.SIGNAL('clicked()'),
      self._onPreviewNext)
    c(self._previewReplay, PyQt4.QtCore.SIGNAL('clicked()'),
      self._onReplayAudio)

    vbox.addWidget(bbox)
    self._previewWindow.setLayout(vbox)
    aqt.utils.restoreGeom(self._previewWindow, 'preview')
    self._previewWindow.show()
    self._renderPreview(True)

aqt.browser.Browser._openPreview = _openPreview

# Context menu
##########################################################################


def onHistory(self):
    m = QMenu(mw)  # self)
    # m.setFont(particularFont('Menu')) # !!!
    for nid, txt in self.history:
        a = m.addAction(_("Edit %s") % txt)
        a.connect(a, SIGNAL("triggered()"),
                  lambda nid=nid: self.editHistory(nid))
    anki.hooks.runHook("AddCards.onHistory", self, m)  # !!!
    m.exec_(self.historyButton.mapToGlobal(QPoint(0, 0)))

aqt.addcards.AddCards.onHistory = onHistory


def onHeaderContext(self, pos):
    gpos = self.form.tableView.mapToGlobal(pos)
    m = QMenu(mw)  # )
    # m.setFont(particularFont('Menu')) # !!!
    for type, name in self.columns:
        a = m.addAction(name)
        a.setCheckable(True)
        a.setChecked(type in self.model.activeCols)
        a.connect(a, SIGNAL("toggled(bool)"),
                  lambda b, t=type: self.toggleField(t))
    m.exec_(gpos)

aqt.browser.Browser.onHeaderContext = onHeaderContext


def _contextMenuEvent(self, evt):
    # self) # self.mw) # !!! AttributeError: 'EditorWebView' object has no
    # attribute 'mw'
    m = QMenu(mw)
    # m.setFont(particularFont('Menu')) # !!!
    a = m.addAction(_("Cut"))
    a.connect(a, SIGNAL("triggered()"), self.onCut)
    a = m.addAction(_("Copy"))
    a.connect(a, SIGNAL("triggered()"), self.onCopy)
    a = m.addAction(_("Paste"))
    a.connect(a, SIGNAL("triggered()"), self.onPaste)
    anki.hooks.runHook("EditorWebView.contextMenuEvent", self, m)
    m.popup(QCursor.pos())

aqt.editor.EditorWebView.contextMenuEvent = _contextMenuEvent


def contextMenuEvent_(self, evt):
    if not self._canFocus:
        return
    m = QMenu(mw)  # self)
    # m.setFont(particularFont('Menu')) # !!!
    a = m.addAction(_("Copy"))
    a.connect(a, SIGNAL("triggered()"),
              lambda: self.triggerPageAction(QWebPage.Copy))
    anki.hooks.runHook("AnkiWebView.contextMenuEvent", self, m)
    m.popup(QCursor.pos())

aqt.webview.AnkiWebView.contextMenuEvent = contextMenuEvent_

# Menu, title bar & status
##########################################################################

mainMenu = mw.menuBar()
mainMenu.setFont(particularFont('Menu'))

try:
    appStyle = """
QMenu { font-family:%s; font-size:%spx; selection-background-color: #ffaa00;
selection-color: black; background-color: #999; border-style: solid;
border: 0px solid #EBEBEB; border-radius: 0; color: #EBEBEB;
padding: 0px 0px 0px 0px; }
QMenu:on  {padding-top: 0px; padding-left: 0px; background-color: #7A7A7A;
selection-background-color: #ffaa00; color: #fff; border-radius: 0;}
QMenu QAbstractItemView  { border: 0px solid black; background-color: #7A7A7A;
color: #EBEBEB; border-radius: 0; }
QMenu:hover { border: 0px solid #ffa02f; }
QMenu::disabled { color: #ccc; }
QMenu::drop-down  { border-radius: 0px; background-color: #7A7A7A;
color: #EBEBEB; }""" %\
        (FONTS['Menu'][0], FONTS['Menu'][1])
    mainMenu.setStyleSheet(appStyle)
    mw.setStyleSheet(mw.styleSheet() + appStyle)
except KeyError:
    pass


def setupBrowserMenu(self):
    self.menuBar().setFont(particularFont('Menu'))
    self.menuBar().setStyleSheet(appStyle)

anki.hooks.addHook('browser.setupMenus', setupBrowserMenu)
