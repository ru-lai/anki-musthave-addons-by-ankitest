# -*- mode: Python ; coding: utf-8 -*-
# ' Addons Install Tooltip
# https://ankiweb.net/shared/info/1738282325
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2017 Dmitry Mikheev, http://finpapa.ucoz.ru/index.html
import anki
import aqt
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Get language class
# Выбранный пользователем язык программной оболочки
lang = anki.lang.getLang()

install_tooltip = True  # False  #
install_hotkeys = True  # False  #
install_again = False  # True  #
install_menu = True  # False  #

if lang == "ru":
    show_install_again_text = u"Показывать Обзор и установка... &Снова"
    open_ankiweb_shared_text = u'Открыть сайт AnkiWeb с &дополнениями'
elif lang == "es":
    show_install_again_text = u"Ver el Examen y la instalación... de &Nuevo"
    open_ankiweb_shared_text = \
        u'Abrir el sitio de Anki&Web, con las complementos'
else:
    show_install_again_text = _(u"Show Browse and Install... &Again")
    open_ankiweb_shared_text = _(u"Open Anki&Web shared add-ons site")


# --------------------------
# anki-master\aqt\addons.py
#  Monkey Patching
#   showInfo -> tooltip
def _accept1(self):
    # go_AnkiWeb_addons()
    # This way starts after dialog window were closed, not before.

    QDialog.accept(self)
    # create downloader thread

    txt = self.form.code.text().split()
    for x in txt:
        ret = aqt.downloader.download(self.mw, x)
        if not ret:
            return
        data, fname = ret
        self.mw.addonManager.install(data, fname)
        self.mw.progress.finish()

    aqt.utils.tooltip(
        _("Download successful. Please restart Anki."),
        period=3000)

    if install_again:
        aqt.addons.AddonManager.onGetAddons(self.mw.addonManager)

if install_tooltip:
    aqt.addons.GetAddons.accept = _accept1

# hotkeys

if install_hotkeys:
    aqt.mw.form.actionDownloadSharedPlugin.setShortcut(
        QKeySequence('Ctrl+Shift+Insert'))


# menu
def go_AnkiWeb_addons():
    aqt.utils.openLink("https://ankiweb.net/shared/addons/")


def toggle_install_again():
    global install_again
    install_again = show_install_again_action.isChecked()

    aqt.addons.AddonManager.onGetAddons(aqt.mw.addonManager)

show_install_again_action = QAction(aqt.mw)
show_install_again_action.setText(show_install_again_text)
show_install_again_action.setCheckable(True)
show_install_again_action.setChecked(install_again)
aqt.mw.connect(show_install_again_action, SIGNAL("triggered()"),
               toggle_install_again)


def save_install_again():
    aqt.mw.pm.profile['addons_install_again'] = (
        show_install_again_action.isChecked())


def load_install_again():
    global install_again, show_install_again_action
    try:
        install_again = aqt.mw.pm.profile['addons_install_again']
    except KeyError:
        install_again = False
    show_install_again_action.setChecked(install_again)

if install_menu:
    anki.hooks.addHook("unloadProfile", save_install_again)
    anki.hooks.addHook("profileLoaded", load_install_again)

    aqt.mw.form.menuPlugins.insertAction(aqt.mw.form.actionOpenPluginFolder,
                                         show_install_again_action)

    open_ankiweb_shared_action = QAction(aqt.mw)
    open_ankiweb_shared_action.setText(open_ankiweb_shared_text)
    aqt.mw.connect(open_ankiweb_shared_action, SIGNAL("triggered()"),
                   go_AnkiWeb_addons)
    aqt.mw.form.menuPlugins.insertAction(aqt.mw.form.actionOpenPluginFolder,
                                         open_ankiweb_shared_action)

else:
    install_again = False

# menuPlugins
# designer/main.ui

# Browse & Install...
# <string>Browse &amp;&amp; Install...</string>
# actionDownloadSharedPlugin

# <string>&amp;Open Add-ons Folder...</string>
# actionOpenPluginFolder
