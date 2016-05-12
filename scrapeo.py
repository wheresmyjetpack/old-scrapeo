import requests
import click
import sys

from bs4 import BeautifulSoup

def opts_provided(*args):
    return any(args)

def scrape_title(soup):
    try:
        _title = soup.title.text.encode('utf-8').strip()
        _title_out = 'Title: %s' % _title
        click.echo(_title_out)

    except AttributeError:
        click.echo('Document contains no title tag')

def scrape_meta(soup, name):
    _meta = soup.find_all('meta', { 'name': name })

    if any(_meta):
        for i in _meta:
            _meta_out = 'Meta %s: %s' % (name, i['content'].encode('utf-8').strip())
            click.echo(_meta_out)

    else:
        click.echo('Document contains no meta tags by the name "%s"' % name)

def scrape_h1s(soup):
    _h1s = soup.find_all('h1')
    click.echo('h1\'s:')
    count = 1

    for _h1 in _h1s:
        click.echo('%s.) %s' % (count, _h1.text.encode('utf-8').strip()))
        count += 1

@click.command()
@click.option('--title', '-t', is_flag='true',
        help='Tell scrapeo to print the title of the document.')
@click.option('--meta', '-m',
        help='Search meta tags by name and print their content')
@click.option('--h1', is_flag='true',
        help='Tell scrapeo to print the text node for all h1\'s in the document')
@click.argument('url')
def cli(title, meta, h1, url):
    """ Scrape data from a document found at URL for SEO data analysis """

    # Rebuild URL if schema is not provided
    if not (url[:7] == 'http://' or url[:8] == 'https://'):
        url = 'http://%s' % url
        click.echo('Rebuilt url to %s...' % url)

    try:
        req = requests.get(url)

        # Raise an exception if request returns "bad" status
        req.raise_for_status()
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # Run without options provided (default behavior)
        if not opts_provided(title, meta, h1):
            scrape_title(soup)
            scrape_meta(soup, 'description')
            sys.exit(0)

        # Flags
        if title:
            scrape_title(soup)

        if h1:
            scrape_h1s(soup)

        # Options w/ args
        if meta:
            scrape_meta(soup, meta)

    except requests.exceptions.RequestException, e:
        # "Bad" status codes, improper input
        for arg in e.args:
            print arg
