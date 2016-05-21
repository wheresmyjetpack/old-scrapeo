import requests
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

        # Unique the list of names
        names = set(names)
        meta = {}

        for name in names:
            meta_from_soup = self.soup.find_all('meta', { 'name': name })
            meta[name] = [ele['content'].encode('utf-8').strip() for ele in meta_from_soup]

        return meta

    def scrape_h1s(self):
        return [h1.text.encode('utf-8').strip() for h1 in self.soup.find_all('h1')]
