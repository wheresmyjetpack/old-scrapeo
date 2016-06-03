import requests
import re
import sys
from collections import defaultdict
from bs4 import BeautifulSoup

class ScrapEO(object):

    def __init__(self, html):
        # ScrapEO uses BeautifulSoup to parse the HTML passed to it
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
        meta_from_soup = self.soup.find_all('meta')

        # Search for meta tags by attribute value...
        if any(search_terms):
            for term in search_terms:

                # Add the value of the "contents" attribute if one of the tag's attribute
                # values is the search term provided
                meta[term] = [tag['content'].encode('utf-8').strip() for tag in meta_from_soup if term in tag.attrs.values()]

        # ...or get every meta tag from the soup
        else:
            # Gathers meta tags if they contain either
            # the name, property or http-equiv attributes
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
                    search_attr = self.__get_search_attr(tag)

                except UnboundLocalError, e:
                    print e[0]
                    # Tag does not have the name, property, or http-equiv
                    # attribute, we don't are about it. Skip itteration
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


    """ Private methods """

    def __get_search_attr(self, tag):

        if tag.has_attr('name'):
            # Assume we're looking for the "name" attribute
            search_attr = tag['name']

        elif tag.has_attr('property'):
            # Assume we're looking for the property attribute next
            search_attr = tag['property']

        elif tag.has_attr('http-equiv'):
            # Finally assume we're looking for the "http-equiv" attribute
            search_attr = tag['http-equiv']

        else:
            # None of the above three attributes, we don't care about it
            # Used to raise ValueError later since search_attr has
            # not been defined
            pass

        return search_attr
