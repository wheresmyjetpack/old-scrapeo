import requests
from bs4 import BeautifulSoup

class ScrapEO(object):

    def __init__(self, html):
        self.soup = BeautifulSoup(html)

    def scrape_title(self):
        try:
            return self.soup.title.text.encode('utf-8').strip()

        except AttributeError:
            click.echo('Document contains no title tag')

    def scrape_meta(self, *names):
        # Returns a dictionary of all meta with attribute name == name
        meta_all = {}

        for name in names:
            meta_from_soup = self.soup.find_all('meta', { 'name': name })
            meta_all[name] = [ ele['content'].encode('utf-8').strip() for ele in meta_from_soup ]

        return meta_all

    def scrape_h1s(self):
        h1s = self.soup.find_all('h1')
        h1s_all = []
        count = 1

        for h1 in h1s:
            h1s_all.append('%s.) %s' % (count, h1.text.encode('utf-8').strip()))
            count += 1
