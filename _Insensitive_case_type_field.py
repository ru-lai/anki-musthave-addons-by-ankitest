# -*- mode: Python ; coding: utf-8 -*-
# • Insensitive case type field
# https://ankiweb.net/shared/info/1616934891
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 How to make Anki insensitive case when using {{type:field}}

 monkey patch
 Upper case, lower case and {{type:}}

 You can use it together with
 Multiple type fields on card
 https://ankiweb.net/shared/info/689574440

 Inspired by
 Select Buttons Automatically If Correct Answer, Wrong Answer or Nothing
 https://ankiweb.net/shared/info/2074758752
"""
from __future__ import division
from __future__ import unicode_literals
import os
import re
import unicodedata

from aqt import mw
from aqt.reviewer import Reviewer
import HTMLParser
from anki.utils import stripHTML
from anki.hooks import addHook, wrap, runHook
from aqt.utils import tooltip, showInfo

UPPER_CASE = False
# UPPER_CASE = True

EXACT_COMPARING = False
# EXACT_COMPARING = True

__addon__ = "'" + __name__.replace('_', ' ')
__version__ = "2.0.44a"

# from Ignore accents in browser search add-on
# https://ankiweb.net/shared/info/1924690148


def stripCombining(txt):
    """Return txt with all combining characters removed."""
    norm = unicodedata.normalize('NFKD', txt)
    return ''.join([c for c in norm if not unicodedata.combining(c)])


def maTypeAnsAnswerFilter(self, buf):
    # tell webview to call us back with the input content
    self.web.eval('_getTypedText();')
    if not self.typeCorrect:
        return buf
    origSize = len(buf)
    buf = buf.replace('<hr id=answer>', '')
    hadHR = len(buf) != origSize
    # munge correct value
    parser = HTMLParser.HTMLParser()
    cor = stripHTML(self.mw.col.media.strip(self.typeCorrect))
    # ensure we don't chomp multiple whitespace
    cor = cor.replace(' ', '&nbsp;')
    cor = parser.unescape(cor)
    cor = cor.replace(u'\xa0', ' ')
    given = self.typedAnswer

    if not EXACT_COMPARING:
        cor = stripCombining(cor)
        given = stripCombining(given)

    # compare with typed answer
    if EXACT_COMPARING:
        res = self.correct(given, cor, showBad=False)
    elif UPPER_CASE:
        res = self.correct(given.strip().upper(),
                           cor.strip().upper(), showBad=False)
    else:
        res = self.correct(given.strip().lower(),
                           cor.strip().lower(), showBad=False)
    # and update the type answer area

    def repl(match):
        # can't pass a string in directly, and can't use re.escape as it
        # escapes too much
        s = """
<span style="font-family: '%s'; font-size: %spx">%s</span>""" % (
            self.typeFont, self.typeSize, res)
        if hadHR:
            # a hack to ensure the q/a separator falls before the answer
            # comparison when user is using {{FrontSide}}
            s = '<hr id=answer>' + s
        return s
    return re.sub(self.typeAnsPat, repl, buf)


def myTypeAnsAnswerFilter(self, buf, i):
    if i >= len(self.typeCorrect):
        return re.sub(self.typeAnsPat, '', buf)
    # tell webview to call us back with the input content
    self.web.eval('_getTypedText(%d);' % i)
    if not self.typeCorrect:
        return buf
    origSize = len(buf)
    buf = buf.replace('<hr id=answer>', '')
    hadHR = len(buf) != origSize
    # munge correct value
    parser = HTMLParser.HTMLParser()
    cor = stripHTML(self.mw.col.media.strip(self.typeCorrect[i]))
    # ensure we don't chomp multiple whitespace
    cor = cor.replace(' ', '&nbsp;')
    cor = parser.unescape(cor)
    cor = cor.replace(u'\xa0', ' ')
    given = self.typedAnswer

    if not EXACT_COMPARING:
        cor = stripCombining(cor)
        given = stripCombining(given)

    # compare with typed answer
    if EXACT_COMPARING:
        res = self.correct(given, cor, showBad=False)
    elif UPPER_CASE:
        res = self.correct(given.strip().upper(),
                           cor.strip().upper(), showBad=False)
    else:
        res = self.correct(given.strip().lower(),
                           cor.strip().lower(), showBad=False)
    # and update the type answer area

    def repl(match):
        # can't pass a string in directly, and can't use re.escape as it
        # escapes too much
        s = """
<span style="font-family: '%s'; font-size: %spx">%s</span>""" % (
            self.typeFont, self.typeSize, res)
        if hadHR:
            # a hack to ensure the q/a separator falls before the answer
            # comparison when user is using {{FrontSide}}
            s = '<hr id=answer>' + s
        return s
    buf = re.sub(self.typeAnsPat, repl, buf, 1)
    return self.typeAnsAnswerFilter(buf, i + 1)

if os.path.exists(os.path.join(mw.pm.addonFolder(),
                  'Multiple_type_fields_on_card.py')):
    Reviewer.typeAnsAnswerFilter = myTypeAnsAnswerFilter
else:
    Reviewer.typeAnsAnswerFilter = maTypeAnsAnswerFilter

##################################################################
# Select_Buttons_Automatically_If_Correct_Answer_Wrong_Answer_or_Nothing.py
# https://ankiweb.net/shared/info/2074758752
# Select Buttons Automatically If Correct Answer, Wrong Answer or Nothing


def maybe_skip_question(self):
    self.typedAnswers = []

Reviewer._showQuestion = wrap(Reviewer._showQuestion, maybe_skip_question)


def maLinkHandler(self, url):

    if ':' in url:
        (cmd, arg) = url.split(':', 1)
    else:
        cmd = url
        arg = ''

    if cmd == 'study':
        my_studyDeck(self, arg)
    elif url.startswith('typeans:'):
        self.typedAnswers.append(unicode(arg))

Reviewer._linkHandler = wrap(Reviewer._linkHandler, maLinkHandler)


def JustDoIt(parm):
    try:
        arg = stripHTML(mw.col.media.strip(unicode(parm)))
        arg = parm.replace(' ', '&nbsp;')
    except UnicodeDecodeError:
        arg = ''
    # ensure we don't chomp multiple whitespace
    arg = HTMLParser.HTMLParser().unescape(arg)
    return arg  # unicode(arg.replace(u'\xa0', ' ')) #arg


def myDefaultEase(self, _old):
    # if self.mw.reviewer.state == 'question':
    #    return _old(self)
    # tooltip(self.mw.reviewer.state)
    # it's always called on answer side, but three times

    given = ''
    if hasattr(self, 'typedAnswer'):
        if hasattr(self, 'typeCorrect'):
            if self.typeCorrect:  # not None
                if hasattr(self, 'typedAnswers'):

                    self.typedAnswer = JustDoIt(
                        unicode(self.typedAnswer))
                    if not len(self.typedAnswers):
                        gvn = [self.typedAnswer]
                    else:
                        for i in range(len(self.typedAnswers)):
                            self.typedAnswers[i] = JustDoIt(
                                unicode(self.typedAnswers[i]))
                        gvn = self.typedAnswers

                    if not type(self.typeCorrect) is list:
                        self.typeCorrect = JustDoIt(
                            unicode(self.typeCorrect))
                        cor = [self.typeCorrect]
                        # in native Anki it is a string
                    else:
                        for i in range(len(self.typeCorrect)):
                            # <div>Indiana</div>
                            # It happens very often
                            # after unexpected pushing Enter key.
                            self.typeCorrect[i] = JustDoIt(
                                stripHTML(unicode(self.typeCorrect[i])))
                        cor = self.typeCorrect
                        # with Multiple_type_fields_on_card.py it becomes
                        # a list of strings

                    if (len(gvn) == 0):
                        res = False
                    else:
                        if (len(gvn) > 1 and len(gvn) != len(cor)):
                            res = False
                            # something went wrong
                        else:
                            res = True
                            for i in range(0, len(cor)):

                                if EXACT_COMPARING:
                                    pass
                                elif UPPER_CASE:
                                    gvn[i] = gvn[i].strip().upper()
                                    cor[i] = cor[i].strip().upper()
                                else:
                                    gvn[i] = gvn[i].strip().lower()
                                    cor[i] = cor[i].strip().lower()

                                if not EXACT_COMPARING:
                                    cor[i] = stripCombining(cor[i])
                                    gvn[i] = stripCombining(gvn[i])

                                if (gvn[i] != '' and gvn[i] != cor[i]):
                                    res = False
                                if (gvn[i] != ''):
                                    given += gvn[i]

                    retv = self.mw.col.sched.answerButtons(self.card)
                    if res or given == '':
                        if retv == 4:
                            retv = 3
                        else:
                            retv = 2
                    else:
                        if retv == 4:
                            retv = 2
                        else:
                            retv = 1

                else:
                    # tooltip ('No typedAnswers')
                    retv = _old(self)
            else:
                    # tooltip ('typeCorrect is None')
                retv = _old(self)
        else:
            # tooltip ('No typeCorrect')
            retv = _old(self)
    else:
        # tooltip ('No typedAnswer')
        retv = _old(self)

    return retv

Reviewer._defaultEase = wrap(Reviewer._defaultEase, myDefaultEase, 'around')
