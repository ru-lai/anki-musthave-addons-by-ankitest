# -*- mode: Python ; coding: utf-8 -*-
from __future__ import unicode_literals
import os

FONT = 'Courier New' # "Calibri" # 'Arial'
FONTSIZE = 12

CtrlShiftX = "F4"

import aqt.clayout
import aqt.editor
import aqt.addons
import aqt.utils
import PyQt4.QtGui
import PyQt4.QtCore
from BeautifulSoup import BeautifulSoup

font = PyQt4.QtGui.QFont()
font.setFamily(FONT)
font.setPointSize(FONTSIZE)

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

# Addons Edit...
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
