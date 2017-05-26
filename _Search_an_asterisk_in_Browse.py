# -*- coding: utf-8 -*-
# Do not replace an asterisk
# Anki 2.0 Monkey Patch 
# to let users search for \* and % 
# (precisely for asterisk and percent sign)
import anki.find
import re
import sre_constants

from anki.utils import ids2str, splitFields, joinFields, intTime, fieldChecksum, stripHTMLMedia
from anki.consts import *


def _findText(self, val, args):
    val = val.replace("%", "\%")

    tmp = val.split('\\\\')
    for (i, item) in enumerate(tmp):
        temp = item.split('\*')
        for (j, jtem) in enumerate(temp):
            temp[j] = jtem.replace('*', '%')
        tmp[i] = '*'.join(temp)   
    val = '\\\\'.join(tmp)   

    args.append("%"+val+"%")
    args.append("%"+val+"%")
    return "(n.sfld like ? escape '\\' or n.flds like ? escape '\\')"

anki.find.Finder._findText = _findText


def _findTag(self, (val, args)):
    if val == "none":
        return 'n.tags = ""'

    val = val.replace("%", "\%")

    tmp = val.split('\\\\')
    for (i, item) in enumerate(tmp):
        temp = item.split('\*')
        for (j, jtem) in enumerate(temp):
            temp[j] = jtem.replace('*', '%')
        tmp[i] = '*'.join(temp)   
    val = '\\\\'.join(tmp)   

    if not val.startswith("%"):
        val = "% " + val
    if not val.endswith("%"):
        val += " %"

    args.append(val)
    return "n.tags like ? escape '\\'"

anki.find.Finder._findTag = _findTag


def _findField(self, field, val):
    field = field.lower()

    val = val.replace("%", "\%")

    tmp = val.split('\\\\')
    for (i, item) in enumerate(tmp):
        temp = item.split('\*')
        for (j, jtem) in enumerate(temp):
            temp[j] = jtem.replace('*', '%')
        tmp[i] = '*'.join(temp)   
    val = '\\\\'.join(tmp)   

    # find models that have that field
    mods = {}
    for m in self.col.models.all():
        for f in m['flds']:
            if f['name'].lower() == field:
                mods[str(m['id'])] = (m, f['ord'])
    if not mods:
        # nothing has that field
        return
    # gather nids
    regex = re.escape(val).replace("\\_", ".").replace("\\%", ".*")

    nids = []
    for (id,mid,flds) in self.col.db.execute("""
select id, mid, flds from notes
where mid in %s and flds like ? escape '\\'""" % (
                     ids2str(mods.keys())),
                     "%"+val+"%"):
        flds = splitFields(flds)
        ord = mods[str(mid)][1]
        strg = flds[ord]
        try:
            if re.search("(?si)^"+regex+"$", strg):
                nids.append(id)
        except sre_constants.error:
            return
    if not nids:
        return "0"
    return "n.id in %s" % ids2str(nids)

anki.find.Finder._findField = _findField
