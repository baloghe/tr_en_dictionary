import regex
regex.DEFAULT_VERSION = regex.VERSION1

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
        'ALTERNATE': ['sap','at','kek','saç','saat','kat','adet'],
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
             'su': ['suyum','suyun','suyu','suyumuz','suyunuz'],
             'akıl': ['aklım','aklın','aklı','aklımız','aklınız'],
             'ömür': ['ömrüm','ömrün','ömrü','ömrümüz','ömrünüz'],
             'vakit': ['vaktim','vaktin','vakti','vaktimiz','vaktiniz'],
             'zihin': ['zihnim','zihnin','zihni','zihnimiz','zihniniz']
        },
        'GENITIVE': {
        },
        'CONTINUOUS_STEM': {
             'ye': 'yi'
            ,'de': 'di'
            ,'git': 'gid'
            ,'et': 'ed'
            ,'tat': 'tad'
        },
        'CONTINUOUS': {
        },
        'FUTURE_STEM': {
             'ye': 'yi'
            ,'de': 'di'
            ,'git': 'gid'
            ,'et': 'ed'
            ,'tat': 'tad'
        },
        'FUTURE': {
        },
        'AORIST': {
             'al': 'alır'
            ,'bil': 'bilir'
            ,'bul': 'bulur'
            ,'dur': 'durur'
            ,'gel': 'gelir'
            ,'gör': 'görür'
            ,'kal': 'kalir'
            ,'ol': 'olur'
            ,'öl': 'ölür'
            ,'san': 'sanır'
            ,'var': 'varır'
            ,'vur': 'vurur'
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
    "verb": ['Aor','Cont','Ind','Nec','Can','Fut','Neg','Pot','Pt','OTH']
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
    "Neg": "Negative"
}

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

def getInflectionGroups(infl, type):
    ks = ['OTH']
    if type and type in INFLECTION_GROUPS:
        ks = INFLECTION_GROUPS[type]
    ret = {}
    for k in ks:
        ret[k] = {"head":"","infl":[]}
    for a in infl:
        parents = getParents(a['src'])
        slot = getSlot(parents, ks)
        ret[slot]["infl"].append(a)
        if len(ret[slot]["head"])==0 or len(ret[slot]["head"]) >= len(a['infl']):
            ret[slot]["head"] = a['infl']
    return ret
