from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import re
import json

driver = webdriver.Firefox()

driver.get('https://pikabu.ru/community/manul/new')


def pars_main(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = [title.get('href') for title in soup.find_all('a', class_='story__title-link')]
    return urls


def pars_post(url):
    res_post = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36'})
    soup_post = BeautifulSoup(res_post.text, 'lxml')
    title = soup_post.find_all('h1', class_='story__title')[0]
    body = soup_post.find_all('div', class_='story__content-inner')[0]
    des_post = body.find_all('div', class_='story-block story-block_type_text')
    r = ''
    for des in des_post:
        r += des.text
    return title.text + r


SCROLL_PAUSE_TIME = 5

all_urls = []

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
count = [a.text for a in soup.find_all('div', class_='community__information')][0].rstrip().lstrip().split()[0]
print(count)

while True:
    html = driver.page_source
    urls = pars_main(html)
    i = 0
    for url in urls:
        if url not in all_urls:
            all_urls.append(url)
            print(i, url)
            i += 1
    print('------------------------------')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    if all_urls[-1] == 'https://pikabu.ru/story/odin_manul_9202402':
        break

to_json = {}

for i in range(len(all_urls)):
    u = all_urls[len(all_urls) - 1 - i]
    parsed = pars_post(u)
    x = re.findall("[0-9]+", parsed)
    print(i, u)
    print(x)
    to_json[i + 1] = {'url': u, 'numbers': x}

print(to_json)

with open('temp.json', 'w') as f:
    json.dump(to_json, f, indent=2)
