rem generate interim (HTML) dictionary
py -m app.run input/dictv2.tsv interim_output/TR_EN_prod.json interim_output/TR_EN_prod.html

cd mobi
mobigen dict.opf -unicode > log.txt 2>&1

cd ..