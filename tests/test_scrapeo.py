#!/usr/bin/env python
import unittest
import os
from scrapeo.core import ScrapEO

class TestScrapEO(unittest.TestCase):

    def setUp(self):
        tests_dir = os.path.dirname(os.path.realpath(__file__))
        document_fixture = '%s/fixtures/document.html' % tests_dir
        self.scrapeo = ScrapEO(open(document_fixture))

    def tearDown(self):
        pass

    def test_scrape_title(self):
        self.assertEqual(
                self.scrapeo.scrape_title(), 'The title')

    def test_scrape_content_from_meta_tag_with_the_name_attribute(self):
        self.assertEqual(self.scrapeo.scrape_meta('description')['description'][0], 'The meta description')

    def test_scrape_content_from_meta_tag_with_the_property_attribute(self):
        self.assertEqual(self.scrapeo.scrape_meta('viewport')['viewport'][0], 'The meta viewport')

if __name__ == '__main__':
    unittest.main()
