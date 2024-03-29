#출처: https://cromboltz.tistory.com/7 [생각 책장]
#출처: https://inspiringpeople.github.io/data%20analysis/wrapper_wikipedia/

#beautiful soup https://wikidocs.net/85739
import wikipediaapi

import csv

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests

import datetime

wiki = wikipediaapi.Wikipedia(
    language='ko',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

def find_date(keyword):
    url = "https://ko.wikipedia.org/w/index.php?title="+keyword+"&action=history"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        ex_id_divs = soup.find('a', {'class': 'mw-changeslist-date'}).get_text()
        date_time_str = ex_id_divs[:ex_id_divs.find('(')-1]
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y년 %m월 %d일')
    else :
        date_time_obj = None

    return date_time_obj

def get_wiki_page_return_info(keyword):
    page_py = wiki.page(keyword)
    id = 0
    url = ""
    text = ""
    length = 0
    if page_py.exists():
        id = page_py.pageid
        url = page_py.fullurl
        text = page_py.text
        length = len(text)
    return id, url, text, length

def main_process(keyword):
    id, url, text, length = get_wiki_page_return_info(keyword)
    date = None
    if length > 0:
        date = find_date(keyword)
    #return [id, url, keyword, text[:10], length, date] 기록용
    return [0, id, url, keyword, text[:10]]

#print(main_process('과학적 방법'))          test용


f = open('good_article.csv', 'w', newline='')
wr = csv.writer(f)
#wr.writerow(['id', 'url', 'keyword', 'text', 'length', 'date'])    기록용
wr.writerow(['id', 'revid', 'url', 'title', 'text'])
with open('good_article', 'r') as f:
    i = 20
    for line in f:
        text = line[:-1]
        print(i)
        if wiki.page(text).exists():
            process_list = main_process(text)
            process_list[0] = i
            wr.writerow(process_list)
        else:
            print(text + " failed")
        i += 1
        

