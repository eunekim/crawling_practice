import requests
from bs4 import BeautifulSoup


class Content:
    """
    글/페이지 전체에 사용할 기반 클래스
    """

    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):
        """
        출력 결과를 원하는 대로 바꿀 수 있는 함수
        """
        print('New article found for topic: {}'.format(self.topic))
        print("URL:{}".format(self.url))
        print("TITLE:{}".format(self.title))
        print("BODY:{}".format(self.body))


class Website:
    """
    웹사이트 구조에 관한 정보를 저장할 클래스
    """

    def __init__(self, name, url, search_url, result_listing, result_url, absolute_url,
        title_tag, body_tag):
        self.name = name
        self.url = url
        self.search_url = search_url
        self.result_listing = result_listing
        self.result_url = result_url
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag


class Crawler:
    def get_page(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safe_get(self, page_obj, selector):
        child_obj = page_obj.select(selector)
        if child_obj is not None and len(child_obj) > 0:
            return child_obj[0].get_text()
        return ''

    def search(self, topic, site):
        """
        주어진 검색어로 주엊니 웹사이트를 검색해 결과 페이지를 모두 기록합니다.
        """
        bs = self.get_page(site.search_url + topic)
        search_results = bs.select(site.result_listing)
        for result in search_results:
            url = result.select(site.result_url)[0].attrs['href']
            # 상대 url인지 절대 url인지 확인합니다.
            if site.absolute_url:
                bs = self.get_page(url)
            else:
                bs = self.get_page(site.url + url)
            if bs is None:
                print('Something was with that page or URL. Skipping!')
                return
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(topic, url, title, body)
                content.print()

clawler = Crawler()

site_date = [
    ['0\'Reilly Media',
        'http://oreilly.com',
        'http://ssearch.oreilly.com/?q=',
        'article.product-result',
        'p.title a',
        True,
        'h1',
        'section#product-description' ],
    ['Reuters', 'http://reuters.com',
        'http://www.reuters.com/search/news?blob=',
        'div.search-result-content',
        'h3.search-result-title a',
        False,
        'h1',
        'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu',
        'http://www.brookings.edu/search/?s=',
        'div.list-content article',
        'h4.title a',
        True,
        'h1',
        'div.post-body']
]
sites = []

for row in site_date:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

topics = ['python', 'data science']
for topic in topics:
    print('GETTING INFO ABOUT: ' + topic)
    for target_site in sites:
        clawler.search(topic, target_site)