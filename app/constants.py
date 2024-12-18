import regex
regex.DEFAULT_VERSION = regex.VERSION1

ALPHABET2 = 'aAâÂbBcCçÇdDeEfFgGğĞhHiİıIîÎjJkKlLmMnNoOöÖpPqQrRsSşŞtTuUûÛüÜvVwWxXyYzZ'
ALPHABET = {'a':0,'A':0,'â':0,'Â':0,'b':1,'B':1,'c':2,'C':2,'ç':2,'Ç':2,'d':3,'D':3,'e':4,'E':4,'f':5,'F':5
            ,'g':6,'G':6,'ğ':6,'Ğ':6,'h':7,'H':7,'i':8,'İ':8,'ı':8,'I':8,'î':8,'Î':8,'j':9,'J':9,'k':10,'K':10
            ,'l':11,'L':11,'m':12,'M':12,'n':13,'N':13,'o':14,'O':14,'ö':15,'Ö':15,'p':16,'P':16,'q':17,'Q':17
            ,'r':18,'R':18,'s':19,'S':19,'ş':19,'Ş':19,'t':20,'T':20,'u':21,'U':21,'û':21,'Û':21,'ü':22,'Ü':22
            ,'v':23,'V':23,'w':24,'W':24,'x':25,'X':25,'y':26,'Y':26,'z':27,'Z':27}

WORDTYPE_MAP = {'verb': 'verb'
    ,'noun': 'noun'
    ,'phrase': 'phrase'
    ,'adj': 'adjective'
    ,'adv': 'adverb'
    ,'conj': 'conjunction'
    ,'part': 'particle'
    ,'prep': 'preposition'
    ,'pron': 'pronoun'
    ,'posp': 'postposition'
    ,'det': 'determinant'}

EXCEPTIONS = {
        'PLURAL':{
            'saat':'saatler',
            'hal':'haller'
        },
        'ALTERNATE': ['sap','at','kek','saç','saat','kat','adet','cesaret','fiyat','dikkat'],
        'ALTERNATE_POSS': ['kek','saç'],
        'ACCUSATIVE': {
             'saat':'saati'
            ,'gol':'golü'
            ,'kontrol':'kontrolü'
            ,'hal':'hali'
        },
        'DATIVE': {
             'saat':'saate'
        },
        'LOCATIVE': {
             'hal':'halde'
        },
        'ABLATIVE': {
             'hal':'halden'
        },
        'POSSESSIVE': {
             'su': ['suyum','suyun','suyu','suyumuz','suyunuz','suyu'],
             'akıl': ['aklım','aklın','aklı','aklımız','aklınız','aklı'],
             'ömür': ['ömrüm','ömrün','ömrü','ömrümüz','ömrünüz','ömrü'],
             'vakif': ['vakfım','vakfın','vakfı','vakfımız','vakfınız','vakfı'],
             'vakit': ['vaktim','vaktin','vakti','vaktimiz','vaktiniz','vakti'],
             'zihin': ['zihnim','zihnin','zihni','zihnimiz','zihniniz','zihni'],
             'isim': ['ismim','ismin','ismi','ismimiz','isminiz','ismi'],
             'karın': ['karnım','karnın','karnı','karnımız','karnınız','karnı'],
             'ağız': ['ağzım','ağzın','ağzı','ağzımız','ağzınız','ağzı'],
             'kahır': ['kahrım','kahrın','kahrı','kahrımız','kahrınız','kahrı'],
             'boyun': ['boynum','boynun','boynu','boynumuz','boynunuz','boynu'],
             'böğür': ['böğrüm','böğrün','böğrü','böğrümüz','böğrünüz','böğrü'],
             'evlat': ['evladım','evladın','evladı','evladımız','evladınız','evladı'],
             'göğüs': ['göğsüm','göğsün','göğsü','göğsümüz','göğsünüz','göğsü']
        },
        'GENITIVE': {
        },
        'GENERAL_STEM': {
             'ye': 'yi'
            ,'de': 'di'
            ,'git': 'gid'
            ,'et': 'ed'
            ,'tat': 'tad'
            ,'affet': 'affed'
            ,'seyret': 'seyred'
            ,'kaybet': 'kaybed'
            ,'zannet': 'zanned'
            ,'başet': 'başed'
            ,'hazzet': 'hazzed'
        },
        'CONTINUOUS': {
        },
        'FUTURE': {
        },
        'AORIST': {
             'al': 'alır'
            ,'bil': 'bilir'
            ,'bul': 'bulur'
            ,'dur': 'durur'
            ,'et': 'eder'
            ,'gel': 'gelir'
            ,'git': 'gider'
            ,'gör': 'görür'
            ,'kal': 'kalir'
            ,'ol': 'olur'
            ,'öl': 'ölür'
            ,'san': 'sanır'
            ,'tat': 'tader'
            ,'var': 'varır'
            ,'vur': 'vurur'
            ,'affet': 'affeder'
            ,'seyret': 'seyreder'
            ,'kaybet': 'kaybeder'
            ,'zannet': 'zanneder'
            ,'başet': 'başeder'
            ,'hazzet': 'hazzeder'
        }
    }

ALTERNATING_CONSONANTS = {'p':'b' , 't':'d' , 'k':'ğ' , 'ç':'c'}
ALTERNATING_CONSONANTS_POSS = {'p':'b' , 'k':'ğ' , 'ç':'c'}

rp_last_syl_low = regex.compile(r'.*?[aıou][\w--[aıoueiöü]]*$')
rp_last_syl_ai = regex.compile(r'.*?[aı][\w--[aıoueiöü]]*$')
rp_last_syl_ou = regex.compile(r'.*?[ou][\w--[aıoueiöü]]*$')
rp_last_syl_ei = regex.compile(r'.*?[ei][\w--[aıoueiöü]]*$')
rp_last_syl_oouu = regex.compile(r'.*?[öü][\w--[aıoueiöü]]*$')
rp_last_cons_hard = regex.compile(r'.*?[çfhkpsşt]$')
rp_ends_alter_cons = regex.compile(r'.*?[ptkç]$')
rp_ends_alter_cons_nk = regex.compile(r'.*?nk$')
rp_ends_alter_cons_poss = regex.compile(r'.*?[pkç]$')
rp_ends_vow = regex.compile(r'.*?[aıoueiöü]$')
rp_ends_cons = regex.compile(r'.*?[bcdgğjlmnrvyzfhsşpçtk]$')
rp_ends_uuii = regex.compile(r'.*?[uüıi]$')
rp_ends_aeoo = regex.compile(r'.*?[aeoö]$')
rp_all_vows = regex.compile(r'[aeoöuüıi]')

INFLECTION_GROUPS = {
    "noun": ['Ind','Pl.Ind','Pl.Poss.Ind','Pl.Poss','Pl','Poss.Ind','Poss','OTH'],
    "verb": ['Aor','Cont','Ind','Nec','Can.Neg.Ing','Can','Fut','Ing','Neg.Fut','Neg.Ing','Neg.Pt','Neg','Pot','Pt','OTH'],
    "adj" : ['Ind','OTH']
}

INFLECTION_DESC = {
    "Acc": "Accusative",
    "Ind": "Indirect",
    "Pl": "Plural",
    "Poss": "Possessive",
    "Dat": "Dative",
    "Loc": "Locative",
    "Abl": "Ablative",
    "Gen": "Genitive",
    "Ki": "Ki",
    "With": "With",
    "Pt": "Past",
    "Pred": "Predicative",
    "LocPers": "Locative personal",
    "Cont": "Continuous",
    "Fut": "Future",
    "Ind": "Indirect",
    "Aor": "Aorist",
    "Ing": "By doing",
    "Prog": "Progressive",
    "Imp": "Imperative",
    "Opt": "Optative",
    "Nec": "Necessitative",
    "Obl": "Obligation",
    "Can": "Can",
    "Pot": "Potential",
    "Neg": "Negative",
    "Ing": "VerbIng",
    "Unless": "Unless",
    "As": "As",
    "When": "When"
}

def _alphaLookup(c):
    if type(c) is str:
        if c in ALPHABET:
            return ALPHABET[c]
        else:
            return -1
    elif type(c) in [int, float]:
        return c
    else:
        return -1

def alphaSort(a):
    # works both
    return sorted(a, key=lambda word: [_alphaLookup(c) for c in ''.join(map(str,word))])

def getSrc(word, actSrc):
    if word['src']:
        return word['src'] + '.' + actSrc
    else:
        return actSrc

def getMx(stem, rexArr):
    ret = {}
    for k in rexArr:
        if regex.match(rexArr[k],stem):
            ret[k]=True
        else:
            ret[k]=False
    return ret

def getParents(src):
    s = src.split('.')
    ret = []
    for i in s:
        if ret:
            ret.append(ret[len(ret)-1] + '.' + i)
        else:
            ret.append(i)
    return ret

def getSlot(parents, keys):
    ret = ''
    for k in keys:
        for p in parents:
            if not ret and k==p:
                ret = k
            #print(f"p={p} - k={k} - ret={ret}")
    if not ret:
        ret = 'OTH'
    return ret

def getInflectionGroups(infl, type, orig):
    ks = ['OTH']
    if type and type in INFLECTION_GROUPS:
        ks = INFLECTION_GROUPS[type]
    ret = {}
    for k in ks:
        ret[k] = {"head":"","infl":[]}
    for a in infl:
        if 'src' not in a:
            print(a)
        parents = getParents(a['src'])
        slot = getSlot(parents, ks)
        ret[slot]["infl"].append(a)
        if len(ret[slot]["head"])==0 or len(ret[slot]["head"]) >= len(a['infl']):
            ret[slot]["head"] = a['infl']
    if 'OTH' in ks:
        ret['OTH']["head"] = orig

    return ret
