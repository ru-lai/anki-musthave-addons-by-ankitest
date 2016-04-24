# -*- mode: Python ; coding: utf-8 -*-
from __future__ import unicode_literals

FONT = 'Courier New' # "Calibri" # 'Arial'
FONTSIZE = 12

import aqt.clayout
import PyQt4.QtGui

def myReadCard(self):
    font = PyQt4.QtGui.QFont()
    font.setFamily(FONT)
    font.setPointSize(FONTSIZE)

    #font.setWeight(62) # <=62 normal >=63 bold

    """
    font.setBold(True)
    font.setItalic(True)
    font.setUnderline(True)
    """

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
