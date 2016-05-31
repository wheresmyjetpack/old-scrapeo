import requests
import re
from collections import defaultdict
from bs4 import BeautifulSoup

class ScrapEO(object):

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def scrape_title(self):
        try:
            return self.soup.title.text.encode('utf-8').strip()

        except AttributeError:
            return

    def scrape_meta(self, *names):
        # Returns a dictionary containing the attributes and
        # content of each self-closing meta tag in the 
        # document
        meta = defaultdict(list)

        if not any(names):
            # Get every self closing meta tag from the soup
            meta_from_soup = self.soup.find_all('meta')
            for ele in meta_from_soup:

                try:
                    if ele.isSelfClosing:
                        meta[ele['name'].encode('utf-8')].append(ele['content'].encode('utf-8').strip())

                except KeyError:
                    # Meta tag does not possess "name" attr
                    pass

        else:
            for name in names:
                meta_from_soup = self.soup.find_all('meta', { 'name': name })
                meta[name.encode('utf-8')] = [ele['content'].encode('utf-8').strip() for ele in meta_from_soup]

        return meta

    def scrape_h1s(self):
        # Returns a list of all h1's in the document
        return [h1.text.encode('utf-8').strip() for h1 in self.soup.find_all('h1')]

    def scrape_articles(self):
        # Returns a list of articles
        # Each article is a dictionary which may contain
        # 'heading' and 'content' keys
        articles = []

        for article in self.soup.find_all('article'):
            article_data = {}

            # The first h tag in the article is the
            # article heading
            article_data['heading'] = article.find(re.compile('h[1-6]')).text.encode('utf-8')
            article_data['sections'] = []

            for section in article.find_all('section'):
                section_data = {}
                try:
                    # The first h tag in the section is the 
                    # section heading
                    section_data['heading'] = section.find(re.compile('h[1-6]')).text.encode('utf-8')

                except AttributeError:
                    # Section does not contain a heading
                    # Do not create a 'heading' key so we can raise
                    # another AttributeError later when accessing
                    # values in the articles list
                    pass

                section_data['content'] = [paragraph.text.encode('utf-8') for paragraph in section.find_all('p')]
                article_data['sections'].append(section_data)

            articles.append(article_data)

        return articles
