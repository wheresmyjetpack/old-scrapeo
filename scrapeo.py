import urllib2
import requests
import sys
import click

from bs4 import BeautifulSoup


@click.command()
@click.option('--title', is_flag='true',
        help='Tell scrapeo to print the title of the document.'
        )
@click.option('--description', is_flag='true',
        help='Tell scrapeo to print the meta description of the document.'
        )
@click.argument('url')
def cli(title, description, url):
    """ Scrape data from a document found at URL for SEO data analysis """

    try:
        req = requests.get(url)

        # Raise an excpetion if request returns "bad" status
        req.raise_for_status()

        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        if title:
            _title = soup.title.text.encode('utf-8')
            _title_out = 'Title: %s' % _title
            click.echo(_title_out)

        if description:
            _description = soup.find('meta', { 'name': 'description' })
            _description_out = 'Description: %s' % _description['content'].encode('utf-8')
            click.echo(_description_out)

    except requests.exceptions.RequestException, e:
        for arg in e.args:
            print arg
