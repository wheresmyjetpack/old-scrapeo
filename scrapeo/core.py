import requests
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
        # Returns a dictionary of all meta with attribute name == name
        meta = defaultdict(list)

        if not any(names):
            # Get every self closing meta tag from the soup
            meta_from_soup = self.soup.find_all('meta')
            for ele in meta_from_soup:

                try:
                    if ele.isSelfClosing:
                        meta[ele['name']].append(ele['content'].encode('utf-8').strip())

                except KeyError:
                    # Meta tag does not possess "name" attr
                    pass

        else:
            for name in names:
                meta_from_soup = self.soup.find_all('meta', { 'name': name })
                meta[name] = [ele['content'].encode('utf-8').strip() for ele in meta_from_soup]

        return meta

    def scrape_h1s(self):
        return [h1.text.encode('utf-8').strip() for h1 in self.soup.find_all('h1')]
