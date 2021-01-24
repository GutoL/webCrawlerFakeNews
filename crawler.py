
#https://piaui.folha.uol.com.br/lupa/tag/verificamoscovid/page/1/

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from multiprocessing import Pool


def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')

def find_links_from_search_page(url):
    # https://stackoverflow.com/questions/32126358/how-do-i-get-the-value-of-a-soup-select
    selector = 'h2.bloco-title > a' # piaui lupa
    soup = get_soup(url)
    links = [a['href'] for a in soup.select(selector)]
    return links

def scrape_search_for_links(page_index):
    print('Scrapping page', page_index)
    links = find_links_from_search_page(site + search_query + '/page/' +
                                        str(page_index))
    print('> Found', len(links), 'links for page', page_index)
    return links

def scrape_fake(link):
    print('> Scrapping', link)
    soup = get_soup(link)

    contents = soup.find_all('script', type='application/ld+json')
    
    if len(contents) < 3:
        print("Error: JSON is not present in the page...")
        return [None]*6

    json_data = str(contents[2]) # because there are 3 scripts per post, and the last one has all information of fake news
    
    date, text, source, json_data = get_data_from_json(json_data)

    links = soup.findAll('img')
    image_link = links[6]['src'] # because the page has several images, and the 6° is related to the fake news
    
    return date, link, text, source, json_data, image_link

def get_data_from_json(json_data):
    json_data = json_data.replace('<script type="application/ld+json">','')
    json_data = json_data.replace('</script>','')
    # json_data = json_data.replace('”','"')
    
    # date: datePublished
    date = re.search('"datePublished":(.*),', json_data).group(1)
    
    # # url: url
    # url = re.search('"url":(.*),', json_data).group(1)
    
    # text: "claimReviewed"
    text = re.search('"claimReviewed":(.*),', json_data).group(1)

    # source: itemReviewed -> name
    source = re.findall('"name":(.*)\r', json_data)[1].replace(',','') # the first one is the name of site (Agência Lupa)
    
    return date, text, source, json_data
    
    

site = "https://piaui.folha.uol.com.br/lupa/"
search_query = '/tag/verificamoscovid/'

if __name__ == "__main__":
    initial_page = 1
    final_page = 1
    print('Start scrapping', site, 'from page', initial_page, 'to', final_page)
    
    all_links = []
    for number_page in range(initial_page, final_page+1):
        all_links.extend(scrape_search_for_links(number_page))
    cont_links = len(all_links)
    print('> Found', cont_links, 'total')

    all_fakes = []
    
    fail = 0

    for link in all_links:
        date, url, text, source, json_data, image_link = scrape_fake(link)
        
        if json_data is not None:
            all_fakes.append({
                'date':date, 
                'url':url,
                'text': text,
                'source':source,
                'json':json_data,
                'img':image_link
                })
        else:
            fail+=1

    print('Sucess:',len(all_links)-fail,'Fail:',fail,'Total:',len(all_links))
    rows = []
    
    for fake in all_fakes:
        rows.append({
            'date':fake['date'], 
            'url':fake['url'],
            'text': fake['text'],
            'source':fake['source'],
            'json':fake['json'],
            'img':fake['img']
         }) 
    
    df = pd.DataFrame(rows)
    df.to_csv('data.csv',sep=';')

