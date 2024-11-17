rem generate interim (HTML) dictionary
py -m app.run input/dict_test_v2.tsv interim_output/tstdict.json interim_output/tstdict.html
cd mobi
mobigen tstdict.opf -unicode