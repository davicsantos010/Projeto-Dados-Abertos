import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys
sys.setrecursionlimit(10000)

input_csv_path = 'Portais.csv'
output_csv_path = 'output4.csv'

df = pd.read_csv(input_csv_path)
all_sublinks = []
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def get_sublinks(link):
    sublinks = []
    pagina = requests.get(link, verify=False, headers=headers)
    site = BeautifulSoup(pagina.text, 'html.parser')
    print(link)
    indiceBarra = link.find('/', link.find('/', link.find('/') + 1) + 1)
    main_link = link[:indiceBarra]
    conteudo = site.find_all('div', attrs={'class': ['dataset-content', 'item', 'card-body', 'node-title', 'col-md-10 col-lg-11 col-xs-10 search-result search-result-dataset', 'col-xs-12']})
    sublinks.extend([main_link + i.find('a').get('href') for i in conteudo])
    next_url = next_page(site)
    if next_url is not None:
        sublinks.extend(get_sublinks(main_link + next_url))

    return sublinks

def next_page(soup):
    prox = soup.find('a', string=['»','Próximos itens »', 'Next', 'próximo ›'])
    if prox:
        link_prox = prox.get('href')
        return link_prox
    else:
        return None

for index, row in df.iterrows():
    link = row['links'] 
    
    all_sublinks.extend(get_sublinks(link))
    

df_all_sublinks = pd.DataFrame({'sublinks': all_sublinks})

df_all_sublinks.to_csv(output_csv_path, index=False)