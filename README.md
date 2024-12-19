# Turkish-English dictionary for Kindle (.mobi) Readers

Turkish being an agglutinative language and Kindle capable of handling a dictionary, the idea is to compose one which resembles a _'usual'_ dictionary on its input side and contains enough inflected forms on the content side so that, once loaded into a Kindle reader, would recognize the most words possible and give some hint on the grammar background of the inflected form in question.

## Overview

The process of Kindle dictionary compilation:
* prepare (extend) some vocabulary listing, still in a human-editable form -> _input/dict_test_v2.tsv_
* create an interim XHTML format (theoretically) readable in both a Web browser AND for the .mobi generator -> e.g. _interim_output/dict_test_v2.html_
* with the use of a static _.opt_ header let _mobigen.exe_ do the magic -> _mobi/tstdict.mobi_

The single batch file _gen_dict.bat_ is meant to perform the entire compilation process.

Great introductions are available on how the interim XHTML and the .opt header (plus other optional inputs) should look like, e.g. [here (Jake McCrary)](https://jakemccrary.com/blog/2020/11/11/creating-a-custom-kindle-dictionary/), [here (Jürgen Schulze)](https://1manfactory.com/create-your-own-kindle-dictionary-for-every-language-for-free/) or [here](https://hanzihero.com/blog/custom-kindle-dictionary) and, of course, not forgetting about the [official documentation](https://kdp.amazon.com/en_US/help/topic/G2HXJS944GL88DNV). Hence the challenging part: how to create the content... 

## TSV Input
As recommended by [Jürgen Schulze](https://1manfactory.com/create-your-own-kindle-dictionary-for-every-language-for-free/) (and others), a TSV obtained from [dict.cc](https://www.dict.cc/) is a good starting point. Although some data cleansing is definitely needed, the general structure is quite user-friendly:

_original_ TAB _translation_ TAB _word_type_ [TAB _example_1_ [...[TAB _example_n_]]]

E.g.
```
bahis	bet	noun	bahse tutuşmak: to make a bet	bahsi açılmak: to open a discussion
```
In this case two examples are attched to the meaning. Of course _bahis_ means not just _bet_ but also _discussion_ which leads us to the problem of words with multiple meanings. Well, a certainly more elegant representation would be something like:
```
bahis	bet	noun	bahse tutuşmak: to make a bet
bahis	discussion	noun	bahsi açılmak: to open a discussion
```
Clearly, the first example goes with _bet_ and the second with _discussion_.
When distinguishing between the various meanings is not relevant:
```
bakma	look, watch, attendance	noun
```
We also have words acting (and being inflected...) in different types, like:
```
dahi	genius	noun
dahi	as well	conj
```

As a result, {_original_ , _translation_ , _word_type_} seems like a reasonable Primary Key.

Furthermore: whereas _translation_ and _example_1-n_ will only be shown to the user, _original_ is the dictionary headword that will be subject to heavy inflection treatment based on the content of _word_type_. Consequently,
* _word_type_ should take its value with a limited set: {_noun, verb, adj, adv, conj, part, prep, pron, posp, det_} standing for noun, verb, adjective, adverb, conjunction, particle, preposition, pronoun, postposition, determinant, respectively
* _original_ should be kept as clean as possible: no blanks, no punctuation marks, no capital letters

## Content Generation
### How Kindle Works
When pointing to a word in an ebook, the reader starts searching the word
* first in the _orth_ tags (attribute 'value')
* then in _orth > infl > iform_ tags (attribute 'value')

According to the documentation, a so-called _fuzzy_ search takes place unless explicitly forbidden by the attribute exact='yes' in _iform_.
E.g. _dış_ (external) and _diş_ (tooth) allegedly get mixed up by fuzzy search, but will be treated as separate words with exact='yes'. Tooth's inflected form _dişimden_ (~from my tooth) can be exempted from exact='yes' since other possible variations (_disimden, dısımden, dışımden_) have no meaning in Turkish, and hopefully our content generator will not  produce them either.

Not mentioned in the documentation however, Kindle generation breaks down (and the entries get entirely omitted) if a word appears more than once in the dictionary.
E.g. _karı_ (1: wife, non-inflected ; 2: snow in accusative) can appear only once in the generated XHTML. So if we venture to take both wife (_karı_) and snow (_kar_) into our dictionary with all their inflected forms, in theory at least three distinct sets must be created:
* inflected and uninflected forms solely of _kar_ that do not interfere with _karı_
  * e.g. _karı_ (snow in accusative) and _karın_ (snow in genitive) should be excluded
  * this will all point to an entry something like '_kar_: snow'
* inflected forms of _karı_ that do not interfere with _kar_
  * e.g. _karı_ (wife uninflected) and _karın_ (~your wife) should be excluded
  * this will all point to an entry something like '_karı_: wife'
* the intersection of the inflected forms of _karı_ and _kar_
  * exactly that is the place for _karı_ and _karın_
  * it will point to a mixed entry something like '1: _kar_: snow , 2: _karı_: wife'
And, belive it or not, _kara_ can mean black (as an adjective uninflected), land (as a noun uninflected) or even 'to the snow' (_kar_ +Dative)...

Moreover, Kindle can only handle 255 inflected forms under a given _orth_ tag. In case an entry has more inflected forms, some kind of partitioning must be applied.

### Entries and Meanings
Each _original_ read from the input TSV is considered as an Entry. An Entry may have different Meanings pertaining to different Word Types.
E.g.
```
bahis	bet	noun	bahse tutuşmak: to make a bet
bahis	discussion	noun	bahsi açılmak: to open a discussion
dahi	genius	noun
dahi	as well	conj
```
would yield two Entries (with 'orig' form _bahis_ and _dahi_, respectively) both having two Meanings.

Upon reading in the TSV input, only Entries and Meanings get generated. Inflected forms are only generated by _calci_.

### Calculating Inflections
An Entry may have different word types (like _kara_ being both a noun and an adjective), therefore may have subject to different grammar rules yielding a vast amount of inflected forms.

Generation of inflected forms is broken down by word types: prcnoun.processNoun(), prcverb.processVerb() etc.

Agglutination means a relatively short stem (e.g. _et_: make) may take on various appendices yielding not just long results (e.g. _edebileceğim_: I will be able to make) but also a lot of them, well above a thousand.

Keeping in mind that Kindle won't handle groups over 255 members anyway, it seems to be a good idea to keep track of the inflection (something like _edebileceğim_ = _et_ + Potential + Future + PossessiveSingular1) and later do a grouping based on the inflection paths.

By calling _Entry.calcInflections()_, the inflections get generated and grouped first by Word type, then by the grouping rule laid down in _constants.INFLECTION_GROUPS_.
```
{'infl': 'edebileceğim', 'src': 'Pot.Fut', 'wtype': 'verb'}
```

### Regrouping Inflections
Unfortunately a simple calculation of all potential inflections would yield e.g. _karın_ appearing under both _karı_ (wife) and _kar_ (snow). Words without any predefined processing will have no inflected forms at all (e.g. Phrases will always be relegated to this category).

The next step in the process is 
* to generate the widest possible set of distinct words to be handled (practically by pouring together all 'orig' forms and inflected forms from Entries)
* and then grouping them so that Kindle doesn't get confused
The Groups should also be "press-ready" that is, a designated headword, all meanings and examples must be available.

### XML Creation
Create an XML document from the set of Groups, according to the rules laid down in the documentation.
