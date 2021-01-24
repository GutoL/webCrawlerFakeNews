
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

    portuguese_links = []  # there are some links with spanish news, we remove them
    for l in links:
      if re.search("verificamos-", l) != None:
        portuguese_links.append(re.search("verificamos-", l).string)
    
    return portuguese_links

def scrape_search_for_links(page_index):
    links = find_links_from_search_page(site + search_query + '/page/' +
                                        str(page_index)+'/')
    return links

def get_data_from_json(json_data):
    json_data = json_data.replace('<script type="application/ld+json">','')
    json_data = json_data.replace('</script>','')
    # json_data = json_data.replace('”','"')
    
    date = re.search('"datePublished":(.*),', json_data).group(1)
    
    classification = re.search('"alternateName":(.*),', json_data).group(1).replace('"','')
    
    # # url: url
    # url = re.search('"url":(.*),', json_data).group(1)
    
    text = re.search('"claimReviewed":(.*),', json_data).group(1)

    # source: itemReviewed -> name
    source = re.findall('"name":(.*)\r', json_data)[1].replace(',','') # the first one is the name of site (Agência Lupa)
    
    return date, text, source, classification, json_data

def scrape_fake(link):
    print('> Scrapping', link)
    soup = get_soup(link)

    links = soup.findAll('img')
    image_link = links[6]['src'] # because the page has several images, and the 6° is related to the fake news

    contents = soup.find_all('script', type='application/ld+json')
    
    if len(contents) < 3:
        print("Error: JSON is not present in the page...")
        return [None]*6
    
    json_list = []

    for x in range(2,len(contents)): # because the first two scripts [0,1] are not related to fake news
        json_list.append(str(contents[x]))

    date_list = []
    text_list = []
    source_list = []
    json_data_list = []
    classification_list = []

    for x in range(len(json_list)):
        date, text, source, classification, json_data = get_data_from_json(json_list[x])
        
        date_list.append(date)
        text_list.append(text)
        source_list.append(source)
        classification_list.append(classification)
        json_data_list.append(json_data)

    image_link_list = [image_link] * len(date_list)
    link_list = [link] * len(date_list)
    
    return date_list, link_list, text_list, source_list, classification_list, json_data_list, image_link_list


    
    

site = "https://piaui.folha.uol.com.br/lupa/"
search_query = 'tag/verificamoscovid/'

if __name__ == "__main__":
    initial_page = 1
    final_page = -1 # -1 → to search in all pages
    print('Start scrapping', site, 'from page', initial_page, 'to', final_page)
    
    all_links = []
    search = True
    
    number_page = initial_page
    while search:
        if (number_page == final_page+1):
            break
        
        print('Scrapping page', number_page)
        links = scrape_search_for_links(number_page)

        if (len(links) > 10): # is a page with no fake news, stop!
            break
        else:
            print('> Found', len(links), 'links for page', number_page)
            all_links.extend(links)
        
        number_page += 1

    cont_links = len(all_links)
    print('> Found', cont_links, 'total')

    all_fakes = []
    
    fail = 0

    for link in all_links:
        date_list, link_list, text_list, source_list, classification_list, json_data_list, image_link_list = scrape_fake(link)
        
        if json_data_list is not None:
            for x in range(len(date_list)):
                all_fakes.append({
                    'date':date_list[x], 
                    'url':link_list[x],
                    'text': text_list[x],
                    'source':source_list[x],
                    'classification':classification_list[x],
                    'json':json_data_list[x],
                    'img':image_link_list[x]
                    })
        else:
            fail+=1

    print('Sucess:',len(all_links)-fail,'Fail:',fail,'Total:',len(all_links))
    
    
    df = pd.DataFrame(all_fakes)
    df.to_csv('data.csv',sep=';') #'''

