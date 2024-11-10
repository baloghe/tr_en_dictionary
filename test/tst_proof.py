from bs4 import BeautifulSoup
import json
import requests

from proof.trydict import tryDict

#document.getElementsByTagName('textarea')[1].value
#text = 'Karımın teni kar gibi beyazdır. Üzerimize kara bir hava çöktü. Bunu kara ekle. Trajedi orada'

response = requests.get('https://www.gazetekadikoy.com.tr/edebiyat-hayatindan-hatirlamalar/sait-faik-abasiyanik-ipekli-mendil')
soup = BeautifulSoup(response.text, 'html.parser')
div = soup.find("div", {"class": "newspage_content"})
text = div.text

tryDict('interim_output/TR_EN_prod.json', text, 'interim_output/prf_tst_found', 'interim_output/prf_tst_notfound')
