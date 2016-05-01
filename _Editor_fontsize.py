# -*- mode: Python ; coding: utf-8 -*-
from __future__ import unicode_literals
import os
from operator import  itemgetter

FONT = 'Courier New' # "Calibri" # 'Arial'
FONTSIZE = 12

CtrlShiftX = "F4"

from aqt.qt import * 
import aqt.addons
import aqt.browser
import aqt.clayout
import aqt.editor
import aqt.utils
import PyQt4.QtGui
import PyQt4.QtCore
from BeautifulSoup import BeautifulSoup

font = PyQt4.QtGui.QFont()
font.setFamily(FONT)
font.setPointSize(FONTSIZE)

typeface = PyQt4.QtGui.QFont()
typeface.setPointSize(FONTSIZE)

#font.setWeight(62) # <=62 normal >=63 bold

"""
font.setBold(True)
font.setItalic(True)
font.setUnderline(True)
"""

# Cards... Style and Templates editing
######################################################################

def myReadCard(self):

    self.tab['tform'].front.setFont(font)
    self.tab['tform'].css.setFont(font)
    self.tab['tform'].back.setFont(font)

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
             lambda: openHelp("editor"))

    form.textEdit.setFont(font)
    form.textEdit.setPlainText(self.note.fields[self.currentField])

    form.textEdit.moveCursor(PyQt4.QtGui.QTextCursor.End)
    d.exec_()
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

import anki.hooks

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

    frm.text.setFont(font)
    frm.text.setPlainText(unicode(open(path).read(), "utf8"))

    d.connect(frm.buttonBox, PyQt4.QtCore.SIGNAL("accepted()"),
              lambda: self.onAcceptEdit(path, frm))
    d.exec_()

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

    text.setFont(font)
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

    self.form.searchEdit.lineEdit().setFont(typeface)

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
        #if self.activeCols[index.column()] not in (
        #    "question", "answer", "noteFld"):
        #    return
        f = QFont()
        row = index.row()
        c = self.getCard(index)
        t = c.template()
        f.setFamily(t.get("bfont", self.browser.mw.fontFamily))
        f.setPixelSize(t.get("bsize", self.browser.mw.fontHeight))
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
    for name, icon, cmd in tags:
        item = self.CallbackItem(
            root, name, lambda c=cmd: self.setFilter(c))
        item.setIcon(0, QIcon(":/icons/" + icon))
        item.setFont(0, typeface)
    return root

def _favTree(self, root):
    saved = self.col.conf.get('savedFilters', [])
    if not saved:
        # Don't add favourites to tree if none saved
        return
    root = self.CallbackItem(root, _("My Searches"), None)
    root.setExpanded(True)
    root.setIcon(0, QIcon(":/icons/emblem-favorite-dark.png"))
    root.setFont(0, typeface)
    for name, filt in sorted(saved.items()):
        item = self.CallbackItem(root, name, lambda s=filt: self.setFilter(s))
        item.setIcon(0, QIcon(":/icons/emblem-favorite-dark.png"))
        item.setFont(0, typeface)

def _decksTree(self, root):
    grps = self.col.sched.deckDueTree()
    def fillGroups(root, grps, head=""):
        for g in grps:
            item = self.CallbackItem(
                root, g[0],
                lambda g=g: self.setFilter("deck", head+g[0]),
                lambda g=g: self.mw.col.decks.collapseBrowser(g[1]))
            item.setIcon(0, QIcon(":/icons/deck16.png"))
            item.setFont(0, typeface)
            newhead = head + g[0]+"::"
            collapsed = self.mw.col.decks.get(g[1]).get('browserCollapsed', False)
            item.setExpanded(not collapsed)
            fillGroups(item, g[5], newhead)
    fillGroups(root, grps)

def _modelTree(self, root):
    for m in sorted(self.col.models.all(), key=itemgetter("name")):
        mitem = self.CallbackItem(
            root, m['name'], lambda m=m: self.setFilter("mid", str(m['id'])))
        mitem.setIcon(0, QIcon(":/icons/product_design.png"))
        mitem.setFont(0, typeface)

def _userTagTree(self, root):
    for t in sorted(self.col.tags.all()):
        if t.lower() == "marked" or t.lower() == "leech":
            continue
        item = self.CallbackItem(
            root, t, lambda t=t: self.setFilter("tag", t))
        item.setIcon(0, QIcon(":/icons/anki-tag.png"))
        item.setFont(0, typeface)

aqt.browser.Browser._systemTagTree = _systemTagTree
aqt.browser.Browser._favTree = _favTree
aqt.browser.Browser._decksTree = _decksTree
aqt.browser.Browser._modelTree = _modelTree
aqt.browser.Browser._userTagTree = _userTagTree
