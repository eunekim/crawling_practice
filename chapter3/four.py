from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

all_ext_link = set()
all_inter_link = set()

def get_all_external_link(site_url):
    html = urlopen(site_url)
    domain = f'{urlparse(site_url).scheme}://{urlparse(site_url).netloc}'

    bs = BeautifulSoup(html, 'html.parser')
    internal_links = get_internal_link(bs, domain)
    external_links = get_external_links(bs, domain)

    for link in external_links:
        if link not in all_ext_link:
            all_ext_link.add(link)
            print(link)

    for link in internal_links:
        if link not in all_inter_link:
            all_inter_link.add(link)
            get_all_external_link(link)


all_inter_link.add('http://oreilly.com')
get_all_external_link('http://oreilly.com')