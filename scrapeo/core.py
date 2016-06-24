import requests
import re
import sys
from collections import defaultdict
from bs4 import BeautifulSoup, NavigableString

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
        # Returns a dictionary containing the name|property|http-equiv
        # attribute and content of each meta tag in the document
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
                    # print e[0]
                    # Tag does not have the name, property, or http-equiv
                    # attribute, we don't are about it. Skip iteration
                    continue

                meta[search_attr.encode('utf-8')].append(content)

        return meta

    def scrape_h1s(self):
        # Returns a list of all h1's in the document
        return [h1.text.encode('utf-8').strip() for h1 in self.soup.find_all('h1')]

    def scrape_articles(self):
        # TODO This really should be more of a document
        # outline generator, since it's becoming clear
        # that this method will handle more than just specifically
        # articles

        # Returns a list of articles
        # Each article is a dictionary which may contain
        # 'heading' and 'content' keys
        articles = []

        for article in self.soup.find_all('article'):
            article_data = {}

            # The first h tag in the article is the
            # article heading
            article_data['heading'] = article.find(re.compile('h[1-6]')).text.encode('utf-8').strip()
            article_data['sections'] = []

            for section in article.find_all('section'):
                section_data = {}
                try:
                    # The first h tag in the section is the 
                    # section heading
                    section_data['heading'] = section.find(re.compile('h[1-6]')).text.encode('utf-8').strip()

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

    def outline(self, root=None):
        document_outline = []
        top_level_sections = []
        section_types = ['article', 'section']
        sections = self.soup.body.find_all(section_types)

        for s in sections:
            section_parents = [p.name for p in s.parents]
            # Are any parents of the section in our section_types list?
            if not any(set(section_parents).intersection(section_types)):
                top_level_sections.append(s)

        # Then for each of the child sections, get the heading and content (if any)
        for sect in top_level_sections:
            child_sections = sect.find_all(section_types)
            child_sections = [child for child in child_sections if ]
            for child in child_sections:
                outlined_child = {}
                outlined_child['type'] = child.name
                outlined_child['heading'] = child.find(re.compile('h[1-6]'))
                outlined_child['content'] = [paragraph for paragraph in child.find_all('p', recursive=False)]

            # Then we want to see if there are sub-sections, and if so, recurse
            if any(child.find_all(['article', 'section'], recursive=False)):
                outlined_child['sections'] = self.outline(root=child)

            document_outline.append(outlined_child)

            document_outline.extend(self.outline(root=next_node))

        else:
            pass

        return document_outline


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

    def __get_sibling_from(self, node):
        if not isinstance(node, NavigableString):
            if not node.next_sibling:
                self.__get_sibling_from(node.parent)
            else:
                return node.next_sibling
        else:
            return self.__get_sibling_from(node.next_sibling)
