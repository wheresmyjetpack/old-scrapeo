import requests
import re
import sys
from collections import defaultdict
from bs4 import BeautifulSoup

class ScrapEO(object):

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def scrape_title(self):
        try:
            return self.soup.title.text.encode('utf-8').strip()

        except AttributeError:
            # No title tag present in the document
            return None

    def scrape_meta(self, *search_terms):
        # Returns a dictionary containing the name attribute and
        # content of each self-closing meta tag in the document
        meta = defaultdict(list)

        if any(search_terms):
            # Search for meta tags by name
            for term in search_terms:
                meta_from_soup = self.soup.find_all('meta', {'name': term})
                meta_from_soup = meta_from_soup if meta_from_soup else self.soup.find_all('meta', {'property': term})

                meta[term] = [tag['content'].encode('utf-8').strip() for tag in meta_from_soup]

        else:
            # or get every meta tag from the soup
            # Gathers meta tags if they contain either
            # the name, property or http-equiv attributes
            meta_from_soup = self.soup.find_all('meta')

            for tag in meta_from_soup:

                try:
                    content = tag['content'].encode('utf-8').strip()

                except KeyError, e:
                    if e.args[0] == 'content':
                        # Meta tag doesn't contain the content attribute,
                        # we don't care about it. Skip this iteration
                        continue

                    else:
                        # We've encounterd an unknown error
                        # Print it and exit
                        print e
                        sys.exit(1)

                try:
                    # Assume we're looking for the "name" attribute
                    search_attr = tag['name']

                except KeyError:
                    try:
                        # Assume we're looking for the property attribute next
                        search_attr = tag['property']

                    except KeyError:
                        # Finally assume we're looking for the "http-equiv" attribute
                        try:
                            search_attr = tag['http-equiv']
                            content = '%s  (http-equiv)' % content

                        except KeyError:
                            # None of the above three attributes, we don't care about it
                            continue

                meta[search_attr.encode('utf-8')].append(content)

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
