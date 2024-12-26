rem save codepage and set UTF-8
for /f "tokens=2 delims=:." %%G in ('chcp') Do set _codepage=%%G
chcp 65001
set PYTHONIOENCODING=utf-8

rem generate interim (HTML) dictionary
py -m app.run input/dictv2.tsv interim_output/TR_EN_prod.json interim_output/TR_EN_prod.html > interim_output/log.txt 2>&1

rem restore codepage
chcp %_codepage%

cd mobi
mobigen dict.opf -unicode > log.txt 2>&1

cd ..