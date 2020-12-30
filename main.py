import requests
from bs4 import BeautifulSoup
import lxml
import TOCKENS


def take_away():
    for i in TOCKENS.URL_MOD:
        url = TOCKENS.URL_STAT + '/ip/' + i
        r = requests.get(url, headers = TOCKENS.HEADER)
        soup = BeautifulSoup(r.content,'lxml')
        for i in soup.find_all('div', {'class' :'company-item'}):
            for x in i.find_all('a'):
                yield x.get('href')

        
if __name__ == "__main__":
    while True:
        print(take_away())
        print('___________________________________________________')