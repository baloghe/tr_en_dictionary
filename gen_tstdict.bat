rem save codepage and set UTF-8
for /f "tokens=2 delims=:." %%G in ('chcp') Do set _codepage=%%G
chcp 65001
set PYTHONIOENCODING=utf-8

rem generate interim (HTML) dictionary
py -m app.run input/dict_test_v2.tsv interim_output/tstdict.json interim_output/tstdict.html > interim_output/tstlog.txt 2>&1

rem restore codepage
chcp %_codepage%

cd mobi
mobigen tstdict.opf -unicode > tstlog.txt 2>&1
cd ..