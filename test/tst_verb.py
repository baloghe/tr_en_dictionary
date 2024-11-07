from app.prcverb import processVerb

for w in ['yemek', 'gitmek', 'aramak', 'yürümek']:
    print(f"{w} -> {processVerb(w)}")
