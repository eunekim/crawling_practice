"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def get_links(page_url):
    global pages
    html = urlopen('http://en.wikipedia.org{}'.format(page_url))
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.findAll('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # 새 페이지를 발견
                new_page = link.attrs['href']
                print(new_page)
                pages.add(new_page)
                get_links(new_page)

get_links('')

"""





from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def get_links(page_url):
    global pages
    html = urlopen('http://en.wikipedia.org'+page_url)
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').findAll('p')[0])
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('This is error')
    for link in bs.findAll('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                new_page = link.attrs['href']
                print('______________\n'+new_page)
                pages.add(new_page)
                get_links(new_page)

get_links('')


