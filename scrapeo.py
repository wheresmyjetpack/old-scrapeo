import requests
import click

from bs4 import BeautifulSoup


@click.command()
@click.option('--title', is_flag='true',
        help='Tell scrapeo to print the title of the document.'
        )
@click.option('--meta', default='description',
        help='Tell scrapeo to print content from meta tags in the document.'
        )
@click.option('--h1', is_flag='true',
        help='Tell scrapeo to print the text node for all h1\'s in the document'
        )
@click.argument('url')
def cli(title, meta, h1, url):
    """ Scrape data from a document found at URL for SEO data analysis """

    try:
        req = requests.get(url)

        # Raise an excpetion if request returns "bad" status
        req.raise_for_status()

        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # Flags
        if title:
            try:
                _title = soup.title.text.encode('utf-8')
                _title_out = 'Title: %s' % _title
                click.echo(_title_out)
            except AttributeError:
                click.echo('Document contains no title tag')

        if meta:
            _meta = soup.find('meta', { 'name': meta })

            try:
                _meta_out = 'Meta %s: %s' % (meta, _meta['content'].encode('utf-8'))
                click.echo(_meta_out)
            except TypeError:
                click.echo('Document contains no meta tag with name %s' % meta)

        if h1:
            _h1s = soup.find_all('h1')
            click.echo('h1\'s:')
            for _h1 in _h1s:
                click.echo(_h1.text.encode('utf-8').strip())

    except requests.exceptions.RequestException, e:
        for arg in e.args:
            print arg
