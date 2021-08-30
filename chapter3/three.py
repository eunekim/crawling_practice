from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

# 페이지에서 발견된 내부 링크를 모두 목록으로 만듭니다.
def get_internal_link(bs, include_url):
    include_url = f'{urlparse(include_url).scheme}://{urlparse(include_url).netloc}'
    internal_link = []
    # /로 시작하는 링크를 모두 찾습니다.
    for link in bs.find_all('a', href=re.compile('^(/|.*' + include_url + ')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_link:
                if link.attrs['href'].startswith('/'):
                    internal_link.append(include_url + link.attrs['href'])
                else:
                    internal_link.append(link.attrs['href'])
    return internal_link


# 페이지에서 발견된 외부 링크를 모두 목록으로 만듭니다.
def get_external_links(bs, exclude_url):
    exclude_links = []
    # 현재 URl을 포함하지 않으면서 http나 www로 시작하는 링크를 모두 찾습니다.
    for link in bs.find_all('a', href=re.compile('^(http|www)((?!' + exclude_url + ').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in exclude_links:
                exclude_links.append(link.attrs['href'])
    return exclude_links


def get_random_external_link(starting_page):
    html = urlopen(starting_page)
    bs = BeautifulSoup(html.read(), 'html.parser')
    external_links = get_external_links(bs, urlparse(starting_page).netloc)
    if len(external_links) == 0:
        print('No external links, looking around the site for one')
        domain = f'{urlparse(starting_page).scheme}://{urlparse(starting_page).netloc}'
        internal_link = get_internal_link(bs, domain)
        return get_random_external_link(internal_link[random.randint(0, len(internal_link) - 1)])
    else:
        return external_links[random.randint(0, len(external_links) - 1)]


def follow_external_only(starting_site):
    external_link = get_random_external_link(starting_site)
    print('Random external link is: {}'.format(external_link))
    follow_external_only(external_link)

follow_external_only('http://oreilly.com')
