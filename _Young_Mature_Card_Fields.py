import copy
import time
from anki.collection import _Collection
from anki.utils import fmtTimeSpan
from anki.hooks import wrap

def timefn(tm):
    str = ""
    if tm >= 60:
        str = fmtTimeSpan((tm/60)*60, short=True, point=-1, unit=1)
    if tm%60 != 0 or not str:
        str += fmtTimeSpan(tm%60, point=2 if not str else -1, short=True)
    return str

    
#oldRenderQA = _Collection._renderQA
def _renderQA(self,data,_old,qfmt=None,afmt=None):
    origFieldMap = self.models.fieldMap
    model = self.models.get(data[2])
    if data[0] is None:
        card = None
    elif data[0] == 1:
        card = None
    else:
        try:
            card = self.getCard(data[0])
        except:
            card = None
    def tmpFieldMap(m):
        "Mapping of field name -> (ord, field)."
        d = dict((f['name'], (f['ord'], f)) for f in m['flds'])
        newFields = ['info:Ord','info:Did','info:Due','info:Id','info:Ivl','info:Queue','info:Reviews','info:Lapses','info:FirstReview','info:LastReview','info:TimeAvg','info:TimeTotal','info:Young','info:Mature','info:CardType','info:Nid','info:Mod','info:Usn','info:Factor']
        for i,f in enumerate(newFields):
            d[f] = (len(m['flds'])+i,0)
        return d
    self.models.fieldMap = tmpFieldMap
    origdata = copy.copy(data)
    data[6] += "\x1f"
    additionalFields = [str(data[4])]
    if card is not None:
        additionalFields += map(str,[card.did,card.due,card.id,card.ivl,card.queue,card.reps,card.lapses])
        (first,last,cnt, total) = self.db.first(
                "select min(id), max(id), count(), sum(time)/1000 from revlog where cid = :id",
                id=card.id)
        if cnt:
            additionalFields.append(time.strftime("%Y-%m-%d", time.localtime(first/1000)))
            additionalFields.append(time.strftime("%Y-%m-%d", time.localtime(last/1000)))
            additionalFields.append(timefn(total/float(cnt)))
            additionalFields.append(timefn(total))
        else:
            additionalFields += [""] * 4
        if card.type == 2 and card.ivl < 21:
            additionalFields += [_("Young")]
        else:
            additionalFields += [""]
        if card.type == 2 and card.ivl > 20:
            additionalFields += [_("Mature")]
        else:
            additionalFields += [""]
        additionalFields += [str(card.type)]
        additionalFields += [str(card.nid)]
        #additionalFields += [str(card.mod)]
        additionalFields.append(time.strftime("%Y-%m-%d", time.localtime(card.mod)))
        additionalFields += [str(card.usn)]
        additionalFields += [str(card.factor)]
    else:
        additionalFields += [""] * 18
    data[6] += "\x1f".join(additionalFields)
    #result = oldRenderQA(self,data,qfmt,afmt)
    result = _old(self,data,qfmt,afmt)
    data = origdata
    self.models.fieldMap = origFieldMap
    return result
    
#def previewCards(self, note, _old, type=0):
def previewCards(self, note, type=0):
    existingTemplates = {c.template()[u'name'] : c for c in note.cards()}
    if type == 0:
        cms = self.findTemplates(note)
    elif type == 1:
        cms = [c.template().name() for c in note.cards()]
    else:
        cms = note.model()['tmpls']
    if not cms:
        return []
    cards = []
    for template in cms:
        if template[u'name'] in existingTemplates:
            card = existingTemplates[template[u'name']]
        else:
            card = self._newCard(note, template, 1, flush=False)
        cards.append(card)
    return cards

#_Collection._renderQA = _renderQA
_Collection._renderQA = wrap(_Collection._renderQA, _renderQA, "around")

_Collection.previewCards = previewCards
#_Collection.previewCards = wrap(_Collection.previewCards, previewCards, "around")