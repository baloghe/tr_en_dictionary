import regex
regex.DEFAULT_VERSION = regex.VERSION1

MOBI_MAX_INFLECTIONS = 255

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
        'ALTERNATE': ['süt','sap','et','at','kek','saç','suç','saat','kat','adet','cesaret','fiyat','dikkat','ip','ameliyat','anket','cinayet','ceket'
                     ,'akrobat','aparat','avukat','baharat','bürokrat','cemaat','cennet','cemiyet','cehalet','ciddiyet'
                     ,'cinsiyet','davet','dehşet','demet','devlet','diyet','ebediyet','edebiyat','ehliyet','emanet','emniyet','etiket'
                     ,'eyalet','eziyet','faaliyet','fazilet','felaket','ganimet','gayret','gurbet','hareket','hakaret','hakimiyet'
                     ,'hasret','hassasiyet','hayalet','hayret','hazret','heybet','heyet','hiddet','hikmet','hizmet','hükumet','hükümet'
                     ,'hürmet','cumhuriyet','hürriyet','hüviyet','ibadet','ibret','icraat','ihanet','ikamet','illet','internet','inşaat','isabet'
                     ,'iskelet','istikamet','işaret','jilet','kabiliyet','kamyonet','kanaat','kaset','kastanyet','kasvet','klarnet'
                     ,'kriket','kravat','kudret','kuvvet','kümbet','küvet','kısmet','kıyafet','kıyamet','kıymet','lanet','lezzet'
                     ,'lânet','mahiyet','maliyet','manşet','marifet','market','mazeret','mecburiyet','medeniyet','medet','memleket'
                     ,'memnuniyet','meşruiyet','meşrutiyet','millet','milliyet','misket','motosiklet','muhabbet','muhalefet'
                     ,'mukavemet','muvaffakiyet','müddet','mülkiyet','münasebet','müracaat','nefret','net','nezaket','nimet','nispet'
                     ,'niyet','nöbet','paket','poşet','rahmet','rağbet','rekabet','rivayet','rüşvet','saadet','samimiyet','sefalet'
                     ,'sefaret','sepet','servet','set','siyaset','sohbet','suret','surat','sünnet','sürat','ticaret','trompet'
                     ,'tuvalet','ücret','vahşet','vasiyet','vaziyet','vekalet','vilayet','zahmet','zanaat','zihniyet','ziyafet'
                     ,'çiklet','ümmet','şahsiyet','şiddet','şikayet','şikâyet','şöhret'
                     ,'azat','cellat','cellât','diplomat','format','fırsat','hakikat','harekat','harekât','hayat','ihracat'
                     ,'iktisat','iltifat','imalat','inat','inşaat','irtibat','ispat','istihbarat','istirahat','ithalat'
                     ,'itikat','kabahat','karbonhidrat','karbondioksit','menfaat','mevduat','mevzuat','muhaberat','mutabakat'
                     ,'mülakat','müracaat','nasihat','olimpiyat','rahat','ruhsat','saltanat','sanat','seyahat','stat','surat'
                     ,'sıfat','tabiat','tahribat','talimat','tarikat','tatbikat','tazminat','teminat','teribat','tezat','teşkilat'
                     ,'vaat','vefat','yat','zat','ziraat','çat','üstat','şefkat','şeriat','şubat','maç'
                     ,'kart','özet','şerbet','sırt','tüvist','yanıt','yapıt','zevk','çark','bulut','hap','asfalt','jip','dost'],
        'ALTERNATE_POSS': ['kek','saç','ip','suç','hap','jip'],
        'ACCUSATIVE': {
             'saat':'saati'
            ,'gol':'golü'
            ,'kontrol':'kontrolü'
            ,'hal':'hali'
            ,'menfaat':'menfaati'
            ,'ziraat':'ziraati'
            ,'şefkat':'şefkati'
            ,'dikkat':'dikkati'
            ,'resim':'resmi'
            ,'rol':'rolü'
            ,'şekil':'şekli'
            ,'sır':'sırrı'
            ,'sual':'suali'
            ,'tavır':'tavrı'
            ,'vakıf':'vakfı'
            ,'alın':'alnı'
        },
        'DATIVE': {
             'saat':'saate'
            ,'hal':'hale'
            ,'cemaat':'cemaate'
            ,'kanaat':'kanaate'
            ,'hakikat':'hakikate'
            ,'menfaat':'menfaate'
            ,'şefkat':'şefkate'
            ,'dikkat':'dikkate'
            ,'resim':'resme'
            ,'rol':'role'
            ,'şekil':'şekle'
            ,'sır':'sırra'
            ,'sual':'suale'
            ,'tavır':'tavra'
            ,'vakıf':'vakfa'
            ,'alın':'alna'
        },
        'LOCATIVE': {
             'hal':'halde'
            ,'dikkat':'dikkatte'
            ,'rol':'rolde'
            ,'saat':'saatte'
            ,'sual':'sualde'
        },
        'ABLATIVE': {
             'hal':'halden'
            ,'dikkat':'dikkatten'
            ,'rol':'rolden'
            ,'saat':'saatten'
            ,'sual':'sualden'
        },
        'POSSESSIVE': {
             'su': ['suyum','suyun','suyu','suyumuz','suyunuz','suyu'],
             'akıl': ['aklım','aklın','aklı','aklımız','aklınız','aklı'],
             'ömür': ['ömrüm','ömrün','ömrü','ömrümüz','ömrünüz','ömrü'],
             'vakıf': ['vakfım','vakfın','vakfı','vakfımız','vakfınız','vakfı'],
             'vakit': ['vaktim','vaktin','vakti','vaktimiz','vaktiniz','vakti'],
             'zihin': ['zihnim','zihnin','zihni','zihnimiz','zihniniz','zihni'],
             'isim': ['ismim','ismin','ismi','ismimiz','isminiz','ismi'],
             'karın': ['karnım','karnın','karnı','karnımız','karnınız','karnı'],
             'ağız': ['ağzım','ağzın','ağzı','ağzımız','ağzınız','ağzı'],
             'kahır': ['kahrım','kahrın','kahrı','kahrımız','kahrınız','kahrı'],
             'boyun': ['boynum','boynun','boynu','boynumuz','boynunuz','boynu'],
             'böğür': ['böğrüm','böğrün','böğrü','böğrümüz','böğrünüz','böğrü'],
             'evlat': ['evladım','evladın','evladı','evladımız','evladınız','evladı'],
             'göğüs': ['göğsüm','göğsün','göğsü','göğsümüz','göğsünüz','göğsü'],
             'hacim': ['hacmim','hacmin','hacmi','hacmimiz','hacminiz','hacmi'],
             'hak': ['hakkım','hakkın','hakkı','hakkımız','hakkınız','hakkı'],
             'hal': ['halim','halin','hali','halimiz','haliniz','hali'],
             'halk': ['halkım','halkın','halkı','halkımız','halkınız','halkı'],
             'keşif': ['keşfim','keşfin','keşfi','keşfimiz','keşfiniz','keşfi'],
             'keyif': ['keyfim','keyfin','keyfi','keyfimiz','keyfiniz','keyfi'],
             'beyin': ['beynim','beynin','beyni','beynimiz','beyniz','beyni'],
             'menfaat': ['menfaatim','menfaatin','menfaati','menfaatimiz','menfaatiniz','menfaati'],
             'saat': ['saatim','saatin','saati','saatimiz','saatiniz','saati'],
             'dikkat': ['dikkatim','dikkatin','dikkati','dikkatimiz','dikkatiniz','dikkati'],
             'oğul': ['oğlum','oğlun','oğlu','oğlumuz','oğlunuz','oğlu'],
             'resim': ['resmim','resmin','resmi','resmimiz','resminiz','resmi'],
             'rol': ['rolüm','rolün','rolü','rolümüz','rolünüz','rolü'],
             'şahıs': ['şahsım','şahsın','şahsı','şahsımız','şahsınız','şahsı'],
             'şekil': ['şeklim','şeklin','şekli','şeklimiz','şekliniz','şekli'],
             'sır': ['sırrım','sırrın','sırrı','sırrımız','sırrınız','sırrı'],
             'sual': ['sualim','sualin','suali','sualimiz','sualiniz','suali'],
             'tavır': ['tavrım','tavrın','tavrı','tavrımız','tavrınız','tavrı'],
             'burun': ['burnum','burnun','burnu','burnumuz','burnunuz','burnu'],
             'alın': ['alnım','alnın','alnı','valnımız','alnınız','alnı'],
             'fikir': ['fikrim','fikrin','fikri','fikrimiz','fikriniz','fikri'],
             'devir': ['devrim','devrin','devri','devrimiz','devriniz','devri'],
             'hat': ['hattım','hattın','hattı','hattımız','hattınız','hattın']
        },
        'GENITIVE': {
        },
        'WITH': {
             'dikkat':'dikkatle'
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
            ,'hisset': 'hissed'
            ,'keşfet': 'keşfed'
            ,'gevşet': 'gevşed'
            ,'sabret': 'sabred'
            ,'küfret': 'küfred'
            ,'arzet': 'arzed'
            ,'atfet': 'atfed'
            ,'bahset': 'bahsed'
            ,'devret': 'devred'
            ,'emret': 'emred'
            ,'farket': 'farked'
            ,'fethet': 'fethed'
            ,'genişlet': 'genişled'
            ,'gözet': 'gözed'
            ,'hafiflet': 'hafifled'
            ,'hallet': 'halled'
            ,'hapset': 'hapsed'
            ,'höpürdet': 'höpürded'
            ,'hükmet': 'hükmed'
            ,'ilerlet': 'ilerled'
            ,'ilet': 'iled'
            ,'inlet': 'inled'
            ,'kastet': 'kasted'
            ,'katlet': 'katled'
            ,'kaydet': 'kayded'
            ,'kirlet': 'kirled'
            ,'mahvet': 'mahved'
            ,'methet': 'methed'
            ,'naklet': 'nakled'
            ,'reddet': 'redded'
            ,'resmet': 'resmed'
            ,'sarfet': 'sarfed'
            ,'terket': 'terked'
            ,'tüket': 'tüked'
            ,'yönet': 'yöned'
            ,'zikret': 'zikred'
            ,'öğret': 'öğred'
            ,'üret': 'üred'
            ,'şükret': 'şükred'
            ,'titret': 'titred'
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
            ,'kal': 'kalır'
            ,'ol': 'olur'
            ,'öl': 'ölür'
            ,'san': 'sanır'
            ,'tat': 'tader'
            ,'var': 'varır'
            ,'ver': 'verir'
            ,'vur': 'vurur'
            ,'affet': 'affeder'
            ,'seyret': 'seyreder'
            ,'kaybet': 'kaybeder'
            ,'zannet': 'zanneder'
            ,'başet': 'başeder'
            ,'hazzet': 'hazzeder'
            ,'hisset': 'hisseder'
            ,'keşfet': 'keşfeder'
            ,'gevşet': 'gevşeder'
            ,'sabret': 'sabreder'
            ,'küfret': 'küfreder'
            ,'arzet': 'arzeder'
            ,'atfet': 'atfeder'
            ,'bahset': 'bahseder'
            ,'devret': 'devreder'
            ,'emret': 'emreder'
            ,'farket': 'farkeder'
            ,'fethet': 'fetheder'
            ,'genişlet': 'genişleder'
            ,'gözet': 'gözeder'
            ,'hafiflet': 'hafifleder'
            ,'hallet': 'halleder'
            ,'hapset': 'hapseder'
            ,'höpürdet': 'höpürdeder'
            ,'hükmet': 'hükmeder'
            ,'ilerlet': 'ilerleder'
            ,'ilet': 'ileder'
            ,'inlet': 'inleder'
            ,'kastet': 'kasteder'
            ,'katlet': 'katleder'
            ,'kaydet': 'kaydeder'
            ,'kirlet': 'kirleder'
            ,'mahvet': 'mahveder'
            ,'methet': 'metheder'
            ,'naklet': 'nakleder'
            ,'reddet': 'reddeder'
            ,'resmet': 'resmeder'
            ,'sarfet': 'sarfeder'
            ,'terket': 'terkeder'
            ,'tüket': 'tükeder'
            ,'yönet': 'yöneder'
            ,'zikret': 'zikreder'
            ,'öğret': 'öğreder'
            ,'üret': 'üreder'
            ,'şükret': 'şükreder'
            ,'titret': 'titreder'
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
    "noun": ['Pl','Poss','OTH'],
    "verb": ['Can.Neg.Ing','Can','Fut.Poss','Fut','Ing','Neg.Fut.Poss','Neg.Fut','Neg.Ing','Neg.Pt','Neg.Poss','Neg','Pt','Poss','Pl','Pot.Fut','OTH'],
    "adj" : ['OTH']
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

def getCodedWord(s):
    return '.'.join([str(_alphaLookup(c)) for c in s])

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
