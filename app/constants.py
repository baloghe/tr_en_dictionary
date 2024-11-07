import regex
regex.DEFAULT_VERSION = regex.VERSION1

WORDTYPE_MAP = {'verb': 'verb'
    ,'noun': 'noun'
    ,'phrase': 'phrase'
    ,'adj': 'adjective'
    ,'adv': 'adverb'
    ,'conj': 'conjuncture'
    ,'part': 'particle'
    ,'prep': 'preposition'
    ,'pron': 'pronoun'}

EXCEPTIONS = {
        'PLURAL':{
            'saat':'saatler'
        },
        'ALTERNATE': ['sap','at','kek','saç','saat','kat'],
        'ACCUSATIVE': {
             'saat':'saati'
            ,'gol':'golü'
            ,'kontrol':'kontrolü'
        },
        'DATIVE': {
             'saat':'saate'
        },
        'LOCATIVE': {
        },
        'ABLATIVE': {
        },
        'POSSESSIVE': {
             'su': ['suyum','suyun','suyu','suyumuz','suyunuz']
        },
        'GENITIVE': {
        },
        'PROGRESSIVE_STEM': {
			 'ye': 'yi'
			,'de': 'di'
			,'git': 'gid'
			,'et': 'ed'
			,'tat': 'tad'
        },
        'PROGRESSIVE': {
        },
        'FUTURE_STEM': {
			 'ye': 'yi'
			,'de': 'di'
			,'git': 'gid'
			,'et': 'ed'
			,'tat': 'tad'
        },
        'FUTURE': {
        }
    }

ALTERNATING_CONSONANTS = {'p':'b' , 't':'d' , 'k':'ğ' , 'ç':'c'}

rp_last_syl_low = regex.compile(r'.*?[aıou][\w--[aıoueiöü]]*$')
rp_last_syl_ai = regex.compile(r'.*?[aı][\w--[aıoueiöü]]*$')
rp_last_syl_ou = regex.compile(r'.*?[ou][\w--[aıoueiöü]]*$')
rp_last_syl_ei = regex.compile(r'.*?[ei][\w--[aıoueiöü]]*$')
rp_last_syl_oouu = regex.compile(r'.*?[öü][\w--[aıoueiöü]]*$')
rp_last_cons_hard = regex.compile(r'.*?[çfhkpsşt]$')
rp_ends_alter_cons = regex.compile(r'.*?[ptkç]$')
rp_ends_alter_cons_nk = regex.compile(r'.*?nk$')
rp_ends_vow = regex.compile(r'.*?[aıoueiöü]$')
rp_ends_cons = regex.compile(r'.*?[bcdgğjlmnrvyzfhsşpçtk]$')
rp_ends_uuii = regex.compile(r'.*?[uüıi]$')
rp_ends_aeoo = regex.compile(r'.*?[aeoö]$')

