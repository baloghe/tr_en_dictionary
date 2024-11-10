from app.prcverb import processVerb

for w in ['yemek', 'gitmek', 'aramak', 'yürümek', 'almak']:
    print(f"{w} -> {processVerb(w)}")
