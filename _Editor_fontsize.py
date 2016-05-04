# -*- mode: Python ; coding: utf-8 -*-
# • Editor fontsize
# https://ankiweb.net/shared/info/1931469441
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# 
# Increase Text Size for Card Types Editor and so on.
# 
# TODO: Some description should be here!!!
# 
# HTML Editor saves width and height on exit.
# Also do Addons Editor.
# 
# Decks, Note Types and Tags in Browser Tree could be collapsed too.
# 
# Expand/Collapse Whole Browser Tree
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
from __future__ import unicode_literals
import os
from operator import  itemgetter

CtrlShiftPlus  = "Ctrl+Shift++" # Expand   Them All
CtrlShiftMinus = "Ctrl+Shift+-" # Collapse Them All
CtrlAltShiftMinus = "Ctrl+Alt+Shift+-" # Collapse Them at All

CtrlShiftX = "F4" # You can make your own e.g. = "Ctrl+Alt+Shift+0"

BrowserColumns = True # if you want to enlarge ALL columns in browser
#BrowserColumns = False # to enlarge "Sort Field", "Question", "Answer" only

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

    #'Force custom font':  (None, 0),
    #'Force custom font':  ('Calibri', 14),
    'Force custom font':  ('Times New Roman', 16),

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

from aqt import mw
from aqt.qt import * 
import aqt.addons
import aqt.browser
import aqt.clayout
import aqt.editor
import aqt.fields
import anki.hooks
import aqt.utils
import PyQt4.QtGui
import PyQt4.QtCore
from BeautifulSoup import BeautifulSoup
from aqt.webview import AnkiWebView

#####################
# Get language class
# Выбранный пользователем язык программной оболочки
import anki.lang
lang = anki.lang.getLang()

def particularFont(fontKey, bold=False, italic=False, underline=False):
    font = PyQt4.QtGui.QFont()
    if fontKey in FONTS:
       if FONTS[fontKey][0] != None:
          font.setFamily(FONTS[fontKey][0])
       fontsize = int(FONTS[fontKey][1])
       if fontsize > 0:
          font.setPixelSize(fontsize)
          #font.setPointSize(fontsize)
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

# HTML editing
######################################################################

def myHtmlEdit(self):
    self.saveNow()
    d = PyQt4.QtGui.QDialog(self.widget)
    form = aqt.forms.edithtml.Ui_Dialog()
    form.setupUi(d)
    d.connect(form.buttonBox, PyQt4.QtCore.SIGNAL("helpRequested()"),
             lambda: aqt.utils.openHelp("editor"))
    aqt.utils.restoreGeom(d,'HTMLedit')

    form.textEdit.setFont(particularFont('HTML Editor'))
    form.textEdit.setPlainText(self.note.fields[self.currentField])

    form.textEdit.moveCursor(PyQt4.QtGui.QTextCursor.End)
    d.exec_()
    aqt.utils.saveGeom(d,'HTMLedit')
    html = form.textEdit.toPlainText()
    # filter html through beautifulsoup so we can strip out things
    # like a leading </div>
    html = unicode(BeautifulSoup(html))
    self.note.fields[self.currentField] = html
    self.loadNote()
    # focus field so it's saved
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)

aqt.editor.Editor.onHtmlEdit = myHtmlEdit

# F4 as well as Ctrl+Shift+X
######################################################################

def mySetupF4(self):
    f4 = PyQt4.QtGui.QShortcut(
         PyQt4.QtGui.QKeySequence(CtrlShiftX), self.parentWindow)
    f4.connect(f4, PyQt4.QtCore.SIGNAL("activated()"), self.onHtmlEdit)

aqt.editor.Editor.setupButtons = anki.hooks.wrap(aqt.editor.Editor.setupButtons, mySetupF4)

# Addons Edit...
######################################################################

def myEdit(self, path):
    d = PyQt4.QtGui.QDialog(self.mw)
    frm = aqt.forms.editaddon.Ui_Dialog()
    frm.setupUi(d)
    d.setWindowTitle(os.path.basename(path))

    frm.text.setFont(particularFont('Add-ons Edit...'))
    frm.text.setPlainText(unicode(open(path).read(), "utf8"))
    aqt.utils.restoreGeom(d,'AddonEditor')

    d.connect(frm.buttonBox, PyQt4.QtCore.SIGNAL("accepted()"),
              lambda: self.onAcceptEdit(path, frm))
    d.exec_()
    aqt.utils.saveGeom(d,'AddonEditor')

aqt.addons.AddonManager.onEdit = myEdit

# showText with title=,minWidth=,minHeight= key parameters
######################################################################

def showTextik(txt, parent=None, type="text", run=True, geomKey=None, \
    minWidth=500, minHeight=400, title=''):
    if not parent:
        parent = aqt.mw.app.activeWindow() or aqt.mw
    diag = PyQt4.QtGui.QDialog(parent)
    diag.setWindowTitle("Anki " + title)
    layout = PyQt4.QtGui.QVBoxLayout(diag)
    diag.setLayout(layout)

    text = PyQt4.QtGui.QTextEdit()
    text.setReadOnly(True)

    text.setFont(particularFont('showText'))
    if type == "text":
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

    diag.connect(box, PyQt4.QtCore.SIGNAL("rejected()"), onReject)
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
      showText(yourText, type="HTML", minHeight=150, minWidth=450, title="• Your title")
    except TypeError:
      showText(yourText, type="HTML")
'''

# Is there a way to increase the size of text in the Search bar?
######################################################################

def onBrowserSearch(self, reset=True):
    "Careful: if reset is true, the current note is saved."
    txt = unicode(self.form.searchEdit.lineEdit().text()).strip()
    prompt = _("<type here to search; hit enter to show current deck>")
    sh = self.mw.pm.profile['searchHistory']
    # update search history
    if txt in sh:
        sh.remove(txt)
    sh.insert(0, txt)
    sh = sh[:30]
    self.form.searchEdit.clear()
    self.form.searchEdit.addItems(sh)
    self.mw.pm.profile['searchHistory'] = sh

    self.form.searchEdit.lineEdit().setFont(particularFont('Browser Search',bold=True))

    if self.mw.state == "review" and "is:current" in txt:
        # search for current card, but set search to easily display whole
        # deck
        if reset:
            self.model.beginReset()
            self.model.focusedCard = self.mw.reviewer.card.id
        self.model.search("nid:%d"%self.mw.reviewer.card.nid, False)
        if reset:
            self.model.endReset()
        self.form.searchEdit.lineEdit().setText(prompt)
        self.form.searchEdit.lineEdit().selectAll()
        return
    elif "is:current" in txt:
        self.form.searchEdit.lineEdit().setText(prompt)
        self.form.searchEdit.lineEdit().selectAll()
    elif txt == prompt:
        self.form.searchEdit.lineEdit().setText("deck:current ")
        txt = "deck:current "

    self.model.search(txt, reset)
    if not self.model.cards:
        # no row change will fire
        self.onRowChanged(None, None)
    elif self.mw.state == "review":
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
            "question", "answer", "noteFld"):
            return
        f = particularFont('Browser Columns') #QFont()
        row = index.row()
        c = self.getCard(index)
        t = c.template()
        #f.setFamily(t.get("bfont", self.browser.mw.fontFamily))
        #f.setPixelSize(t.get("bsize", self.browser.mw.fontHeight))
        return f
    elif role == Qt.TextAlignmentRole:
        align = Qt.AlignVCenter
        if self.activeCols[index.column()] not in ("question", "answer",
           "template", "deck", "noteFld", "note"):
            align |= Qt.AlignHCenter
        return align
    elif role == Qt.DisplayRole or role == Qt.EditRole:
        return self.columnData(index)
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
        (_("Whole Collection"), "ankibw", ""),
        (_("Current Deck"), "deck16", "deck:current"),
        (_("Added Today"), "view-pim-calendar.png", "added:1"),
        (_("Studied Today"), "view-pim-calendar.png", "rated:1"),
        (_("Again Today"), "view-pim-calendar.png", "rated:1:1"),
        (_("New"), "plus16.png", "is:new"),
        (_("Learning"), "stock_new_template_red.png", "is:learn"),
        (_("Review"), "clock16.png", "is:review"),
        (_("Due"), "clock16.png", "is:due"),
        (_("Marked"), "star16.png", "tag:marked"),
        (_("Suspended"), "media-playback-pause.png", "is:suspended"),
        (_("Leech"), "emblem-important.png", "tag:leech"))
    def onCollapse():
        mw.col.conf['_collapseRootage'] = limb.isExpanded()
    limb = self.CallbackItem(root, "Коренные" if lang=='ru' else _("Rootage"), \
                             lambda: onClick(limb), oncollapse=onCollapse)
    if '_collapseRootage' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseRootage'])
    else:
        limb.setExpanded(True)
    limb.setIcon(0, QIcon(":/icons/ankibw"))
    limb.setFont(0, particularFont('Browser sysTree',italic=True))
    for name, icon, cmd in tags:
        item = self.CallbackItem(
            limb, name, lambda c=cmd: self.setFilter(c))
        item.setIcon(0, QIcon(":/icons/" + icon))
        item.setFont(0, particularFont('Browser sysTree'))
    return root

def _favTree(self, root):
    saved = self.col.conf.get('savedFilters', [])
    if not saved:
        # Don't add favourites to tree if none saved
        return
    def onCollapse():
        mw.col.conf['_collapseFavorites'] = limb.isExpanded()
    limb = self.CallbackItem(root, _("My Searches"), \
                             lambda: onClick(limb), oncollapse=onCollapse)
    if '_collapseFavorites' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseFavorites'])
    else:
        limb.setExpanded(True)
    limb.setIcon(0, QIcon(":/icons/emblem-favorite-dark.png"))
    limb.setFont(0, particularFont('Browser favTree',italic=True))
    for name, filt in sorted(saved.items()):
        item = self.CallbackItem(limb, name, lambda s=filt: self.setFilter(s))
        item.setIcon(0, QIcon(":/icons/emblem-favorite-dark.png"))
        item.setFont(0, particularFont('Browser favTree',italic=True))

def _decksTree(self, root):
    def onCollapse():
        mw.col.conf['_collapseDecks'] = limb.isExpanded()
    limb = self.CallbackItem(root, _("Decks"), #lambda: root.collapseAll(),
                             lambda: onClick(limb), oncollapse=onCollapse)
    if '_collapseDecks' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseDecks'])
    else:
        limb.setExpanded(True)
    limb.setIcon(0, QIcon(":/icons/deck16.png"))
    limb.setFont(0, particularFont('Browser deckTree',italic=True))
    def fillGroups(root, grps, head=""):
        for g in grps:
            item = self.CallbackItem(
                root, g[0],
                lambda g=g: self.setFilter("deck", head+g[0]),
                lambda g=g: self.mw.col.decks.collapseBrowser(g[1]))
            item.setIcon(0, QIcon(":/icons/deck16.png"))
            item.setFont(0, particularFont('Browser deckTree'))
            newhead = head + g[0]+"::"
            collapsed = self.mw.col.decks.get(g[1]).get('browserCollapsed', False)
            item.setExpanded(not collapsed)
            fillGroups(item, g[5], newhead)
    fillGroups(limb, self.col.sched.deckDueTree())

def _modelTree(self, root):
    def onCollapse():
        mw.col.conf['_collapseNoteTypes'] = limb.isExpanded()
    limb = self.CallbackItem(root, _("Note Types"), \
                             lambda: onClick(limb), oncollapse=onCollapse)
    if '_collapseNoteTypes' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseNoteTypes'])
    else:
        limb.setExpanded(True)
    limb.setIcon(0, QIcon(":/icons/product_design.png"))
    limb.setFont(0, particularFont('Browser noteTree',italic=True))
    for m in sorted(self.col.models.all(), key=itemgetter("name")):
        mitem = self.CallbackItem(
            limb, m['name'], lambda m=m: self.setFilter("mid", str(m['id'])))
        mitem.setIcon(0, QIcon(":/icons/product_design.png"))
        mitem.setFont(0, particularFont('Browser noteTree'))

# thanks to Patrice Neff http://patrice.ch/
# https://github.com/pneff/anki-hierarchical-tags
# https://ankiweb.net/shared/info/1089921461

HIERARCHICAL_TAGS = True
#HIERARCHICAL_TAGS = False

# Separator used between hierarchies
SEPARATOR = '::'

def _userTagTree(self, root):
    def onCollapse():
        mw.col.conf['_collapseTags'] = limb.isExpanded()
    limb = self.CallbackItem(root, _("Tags"), \
                             lambda: onClick(limb), oncollapse=onCollapse)
    if '_collapseTags' in mw.col.conf:
        limb.setExpanded(mw.col.conf['_collapseTags'])
    else:
        limb.setExpanded(True)
    limb.setIcon(0, QIcon(":/icons/anki-tag.png"))
    limb.setFont(0, particularFont('Browser tagTree',italic=True))
    tags_tree = {}
    for t in sorted(self.col.tags.all()):
      if t.lower() == "marked" or t.lower() == "leech":
         continue

      if HIERARCHICAL_TAGS:
        components = t.split(SEPARATOR)
        enum = enumerate(components)
        emax = len(components)-1
        for idx, c in enum:
            partial_tag = SEPARATOR.join(components[0:idx + 1])
            if not tags_tree.get(partial_tag):
                if idx == 0:
                    parent = limb
                else:
                    parent_tag = SEPARATOR.join(components[0:idx])
                    parent = tags_tree[parent_tag]
                if emax == idx:
                    item = self.CallbackItem(parent, c,
                        lambda ptg=partial_tag: self.setFilter("tag", ptg))
                else:
                    item = self.CallbackItem(parent, c,
                        lambda ptg=partial_tag: self.setFilter("tag", ptg + '::*'))

                item.setIcon(0, QIcon(":/icons/anki-tag.png"))
                item.setFont(0, particularFont('Browser tagTree'))

                tags_tree[partial_tag] = item
      else:
        item = self.CallbackItem(
            limb, t, lambda t=t: self.setFilter("tag", t))
        item.setIcon(0, QIcon(":/icons/anki-tag.png"))
        item.setFont(0, particularFont('Browser tagTree'))

aqt.browser.Browser._systemTagTree = _systemTagTree
aqt.browser.Browser._favTree = _favTree
aqt.browser.Browser._decksTree = _decksTree
aqt.browser.Browser._modelTree = _modelTree
aqt.browser.Browser._userTagTree = _userTagTree

def setupMenu(self):
    menu = self.form.menuJump #.menuEdit
    menu.addSeparator()

    a = menu.addAction('Развернуть всё дерево' if lang=='ru' else _('Expand Them All'))
    a.setShortcut(QKeySequence(CtrlShiftPlus))
    self.connect(a, PyQt4.QtCore.SIGNAL("triggered()"), lambda b=self: ExpandThemAll(b, True, False))

    a = menu.addAction('Свернуть все ветки' if lang=='ru' else _('Collapse Them All'))
    a.setShortcut(QKeySequence(CtrlShiftMinus))
    self.connect(a, PyQt4.QtCore.SIGNAL("triggered()"), lambda b=self: ExpandThemAll(b, False, False))

    a = menu.addAction('Свернуть вообще всё' if lang=='ru' else _('Collapse Them at All'))
    a.setShortcut(QKeySequence(CtrlAltShiftMinus))
    self.connect(a, PyQt4.QtCore.SIGNAL("triggered()"), lambda b=self: ExpandThemAll(b, False, True))

    menu.addSeparator()

def ExpandThemAll(self, action, atAll):
    if action:
        self.form.tree.expandAll()
    elif atAll:
        self.form.tree.collapseAll()
    else:
        self.form.tree.collapseAll()
        self.form.tree.expandToDepth(0)

anki.hooks.addHook("browser.setupMenus", setupMenu)

# Fields List dialog window
##########################################################################

def FieldDialog__init__(self, mw, note, ord=0, parent=None):
        QDialog.__init__(self, parent or mw) #, Qt.Window)
        self.mw = aqt.mw
        self.parent = parent or mw
        self.note = note
        self.col = self.mw.col
        self.mm = self.mw.col.models
        self.model = note.model()
        self.mw.checkpoint(_("Fields"))
        self.form = aqt.forms.fields.Ui_Dialog()
        self.form.setupUi(self)
        self.setWindowTitle(_("Fields for %s") % self.model['name'])
        self.form.buttonBox.button(QDialogButtonBox.Help).setAutoDefault(False)
        self.form.buttonBox.button(QDialogButtonBox.Close).setAutoDefault(False)
        self.currentIdx = None
        self.oldSortField = self.model['sortf']
        self.fillFields()
        self.setupSignals()

        self.form.fieldList.setCurrentRow(0)
        self.form.fieldList.setFont(particularFont('Fields List'))

        self.exec_()

aqt.fields.FieldDialog.__init__ = FieldDialog__init__

# Preview Answer / Preview Next by click Enter
#  (by default goPrev byLeftArrow goNext byRight Arrow)
#######################################################

def _openPreview(self):
    c = self.connect
    self._previewState = "question"
    self._previewWindow = PyQt4.QtGui.QDialog(None, Qt.Window)
    self._previewWindow.setWindowTitle(_("Preview"))
    c(self._previewWindow, SIGNAL("finished(int)"), self._onPreviewFinished)

    vbox = QVBoxLayout()
    vbox.setMargin(0)
    self._previewWeb = AnkiWebView()
    vbox.addWidget(self._previewWeb)
    bbox = QDialogButtonBox()

    self._previewReplay = bbox.addButton(_("Replay Audio"), QDialogButtonBox.ActionRole)
    self._previewReplay.setAutoDefault(False)
    self._previewReplay.setShortcut(PyQt4.QtGui.QKeySequence("R"))
    self._previewReplay.setToolTip(_("Shortcut key: %s" % "R"))

    self._previewPrev = bbox.addButton("<", PyQt4.QtGui.QDialogButtonBox.ActionRole)
    self._previewPrev.setAutoDefault(False)
    self._previewPrev.setShortcut(PyQt4.QtGui.QKeySequence("Left"))
    self._previewPrev.setToolTip(_("Shortcut key: ← Left arrow ⇐ "))

    self._previewNext = bbox.addButton(">", PyQt4.QtGui.QDialogButtonBox.ActionRole)
    self._previewNext.setAutoDefault(True)
    self._previewNext.setShortcut(PyQt4.QtGui.QKeySequence("Right"))
    self._previewNext.setToolTip(_("Shortcut key: → Right arrow ⇒ or Enter ↵ ")) # &crarr;

    c(self._previewPrev, PyQt4.QtCore.SIGNAL("clicked()"), self._onPreviewPrev)
    c(self._previewNext, PyQt4.QtCore.SIGNAL("clicked()"), self._onPreviewNext)
    c(self._previewReplay, PyQt4.QtCore.SIGNAL("clicked()"), self._onReplayAudio)

    vbox.addWidget(bbox)
    self._previewWindow.setLayout(vbox)
    aqt.utils.restoreGeom(self._previewWindow, "preview")
    self._previewWindow.show()
    self._renderPreview(True)

aqt.browser.Browser._openPreview = _openPreview
