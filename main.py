import requests
import pandas
from bs4 import BeautifulSoup
import lxml
import TOCKENS
import sys, os




Main_Data_Frame = {
    'Name':[],
    'INN':[],
    'NIP':[]
}


def proxy():
    with open('proxy.txt','r') as f:
        print("Reading proxies...")
        proxies = [i.strip() for i in f]
        print("Proxies are ready")
        return(proxies)



def take_away(proxy_l):
    global Main_Data_Frame
    row = 0
    for letter in TOCKENS.URL_MOD:
        for page in range(1,5):
            for pr in proxy_l:
                url = TOCKENS.URL_STAT + 'ip/' + letter + '/' + str(page) 
                print('Taking url' + url)
                try:
                    r = requests.get(url, headers = TOCKENS.HEADER, proxies = dict.fromkeys(['http','https'],pr))
                except Exception:
                    continue
                if r.status_code == 404 or r.status_code != 200:
                    print(str(r.status_code)+ "Bad proxy")
                    continue
                else:
                    print("Good Proxy")
                    soup = BeautifulSoup(r.content,'lxml')
                    for i in soup.find_all('div', {'class' :'company-item'}):
                        if i.find('span', {'class' : 'warning-text'}):
                            break
                        else:
                            for x in i.find_all('a'):
                                Main_Data_Frame['Name'].append(str(x.text).strip())
                                #xyxl.cell(row + 1, 1 ).value = str(x.text).strip()
                            for z in i.find_all('dd')[0:1]:
                                if (row + 1) % 2 == 1:
                                    Main_Data_Frame['INN'].append(str(z.text).strip())
                                    row+=1
                                    #xyxl.cell(row + 1 , 2).value = str(z.text).strip()
                                else:
                                    Main_Data_Frame['NIP'].append(str(z.text).strip())
                                    row+=1
                                    #xyxl.cell(row + 1 , 3).value = str(z.text).strip()
                    break
                    
                        
            



if __name__ == "__main__":
    #while True:
    try:
        print(take_away(proxy()))
    except KeyboardInterrupt:
        print(Main_Data_Frame)
        df = pandas.DataFrame.from_dict(Main_Data_Frame, orient='index')
        df = df.transpose()
        df.to_excel('pyth.xlsx')
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    print('___________________________________________________')