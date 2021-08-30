import requests
from bs4 import BeautifulSoup


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
        print("BODY:{}".format(self.body))


class Website:
    """
    웹사이트 구조에 관한 정보를 저장할 클래스
    """

    def __init__(self, name, url, title_tag, body_tag):
        self.name = name
        self.url = url
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
        """
        Beautiful 객체와 선택자를 받아 콘텐츠 문자열을 추출하는 함수
        주어진 선택자로 검색된 결과가 없다면 빈 문자열을 반환합니다.
        """

        selected_elems = page_obj.select(selector)
        if selected_elems is not None and len(selected_elems) > 0:
            return '\n'.join(
                [elem.get_text() for elem in selected_elems])
        return ''

    def parse(self, site, url):
        """
        url을 받아 빈 콘텐츠를 추출합니다
        """

        bs = self.get_page(url)
        if bs is not None:
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

clawler = Crawler()

site_date = [
    ['0\'Reilly Media', 'http://oreilly.com',
        'h1', 'section#product-description'],
    ['Reuters', 'http://reuters.com',
        'h1', 'div.StadardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu',
        'h1', 'div.post-body']
]
websites = []
urls = [
    'http://shop.oreilly.com/produst/0636920028154.do',
    'http://www.reuters.com/article/us-usa-epa-pruitt-idUSKBN19W2D0',
    'http://www.brookings.edu/blog/techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/'
]
for row in site_date:
    websites.append(Website(row[0], row[1], row[2], row[3]))

clawler.parse(websites[0], urls[0])
clawler.parse(websites[1], urls[1])
clawler.parse(websites[2], urls[2])
