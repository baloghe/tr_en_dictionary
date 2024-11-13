from app.prcverb import processVerb

#for w in ['yemek', 'gitmek', 'aramak', 'yürümek', 'almak']:
for w in ['aramak']:
    print(f"{w} -> {processVerb(w)}")
