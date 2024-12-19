from app.constants import alphaSort, ALPHABET, getCodedWord

words = ['deniz','kar','ceza','kara','sarı','karın','tercih','şerefe','tercih etmek','çakı', 'hala','hâlâ','hele','çocuk','soğuk']

print(words)
'''
from app.constants import ALPHABET
for w in words:
    print(w)
    for c in w:
        print(f"{c} :: index={ALPHABET.find(c)}")
'''
print(alphaSort(words))

w2 = [['kar','snow','noun'],['çakı','pocket knife','noun'],['çocuk','child','noun'],['ceza','punishment','noun']]
print(w2)
print(alphaSort(w2))

w3 = [['kar',4],['çakı',9],['çocuk',20],['ceza',40]]
print(w3)
print(alphaSort(w3))

w4 = ['dış','Diş']
for w in w4:
    print(f"{w} -> {getCodedWord(w)}")
