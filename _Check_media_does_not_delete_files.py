# -*- coding: utf-8 -*-
# ~ Check media does not delete files
# https://ankiweb.net/shared/info/1051530260
# License: GNU GPL, version 3 or later
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# Check media... don't delete files into the basket,
#  just move them to an outside folder.
# If answer NO then
#  usual removal into the trash will be done.
"""
Copyright: Steve AW <steveawa@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
from __future__ import unicode_literals
import os
import datetime
import shutil

from anki.lang import _
from anki.hooks import wrap
from aqt.main import AnkiQt
from aqt.utils import askUser, tooltip, showWarning, openFolder

__author__ = 'Steve'

NOW = datetime.datetime.now().strftime('%y%m%d_%H%M%S')


def deleteUnused(self, unused, diag, _old):
    base_del_dir = self.pm._ensureExists(
        os.path.join(self.pm.profileFolder(), 'backups'))
    dest_del_dir = os.path.join(base_del_dir, 'deleted%s' % (NOW))
    mdir = self.col.media.dir()
    if not askUser(_('Move unused media files to the folder<br><i>%s</i>') %
                   (dest_del_dir)):
        return _old(self, unused, diag)
    else:
        if os.path.exists(dest_del_dir):
            showWarning('Folder already exists')
            return
        os.makedirs(dest_del_dir)
        for f in unused:
            source_path = os.path.join(mdir, f)
            target_path = os.path.join(dest_del_dir, f)
            shutil.move(source_path, target_path)
        tooltip(_('Media files were deleted into<br> %s') % (dest_del_dir))
        if askUser(_('<b>Open folder</b><br><i>%s</i>') % (dest_del_dir)):
            openFolder(dest_del_dir)
        diag.close()
        return True

AnkiQt.deleteUnused = wrap(AnkiQt.deleteUnused, deleteUnused, 'around')
