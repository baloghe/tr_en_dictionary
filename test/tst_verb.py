from app.prcverb import processVerb

for w in ['yemek', 'gitmek', 'aramak']:
    print(f"{w} -> {processVerb(w)}")
