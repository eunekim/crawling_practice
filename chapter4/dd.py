import requests
from bs4 import BeautifulSoup
import re

class Website:

    def __init__(self, name, url, target_pattern, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.target_pattern = target_pattern
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag

class Content:
    """
    글/페이지 전체에 사용할 기반 클래스
    """

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body


    def print(self):
        """
        출력 결과를 원하는 대로 바꿀 수 있는 함수
        """
        print("URL:{}".format(self.url))
        print("TITLE:{}".format(self.title))
        print("BODY:\n{}".format(self.body))

class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []

    def get_page(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safe_get(self, page_obj, selector):
        selected_elems = page_obj.select(selector)
        if selected_elems is not None and len(selected_elems) > 0:
            return '\n'.join([elem.get_text() for elem in selected_elems])
        return ''

    def parse(self, url):
        bs = self.get_page(url)
        if bs is not None:
            title = self.safe_get(bs, self.site.title_tag)
            body = self.safe_get(bs, self.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

    def crawl(self):
        """
        사이트 홈페이지에서 페이지를 가져옵니다.
        """
        bs = self.get_page(self.site.url)
        target_pages = bs.findAll('a', href=re.compile(self.site.target_pattern))
        for target_page in target_pages:
            target_page = target_page.attrs['href']
            if target_page not in self.visited:
                self.visited.append(target_page)
                if not self.site.absolute_url:
                    target_page = '{}{}'.format(self.site.url, target_page)
                self.parse(target_page)

reuters = Website('Reuters',
                  'https://www.reuters.com',
                  '^(/article/)',
                  False,
                  'h1',
                  'div.StandardArticleBody_body')

crawler = Crawler(reuters)
crawler.crawl()