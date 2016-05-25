""" Scrap-EO: The SEO auditing CLI tool

Copyright (C) 2016  Paul Morris

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import requests
import click
import sys

""" Local imports """
from scrapeo.core import ScrapEO

# Defaults
DEFAULT_META = 'description'

# Styled text
H1_STYLED = click.style('h1\'s', fg='green')
TITLE_STYLED = click.style('Title', fg='green')
META_STYLED = click.style('Meta', fg='green')
NEG_INDICATOR = click.style('[-]', fg='red')

@click.command()
@click.option('--title', '-t', is_flag='true',
        help='Tell scrapeo to print the title of the document.')
@click.option('--h1', is_flag='true',
        help='Tell scrapeo to print the text node for all h1\'s in the document')
@click.option('--allmeta', '-a', is_flag='true',
        help='Tell scrapeo to print the content from all meta tags')
@click.option('--meta', '-m',
        multiple=True,
        help='Search meta tags by name and print their content')
@click.argument('url')
def cli(title, h1, allmeta, meta, url):
    """ Scrape data from a document found at URL for SEO data analysis """

    # Rebuild URL if schema is not provided
    if not (url[:7] == 'http://' or url[:8] == 'https://'):
        url = 'http://%s' % url
        click.echo('Rebuilt url to %s...' % url)

    try:
        url = url.decode('utf-8')
        req = requests.get(url)

        # Raise an exception if request returns "bad" status
        req.raise_for_status()
        html = req.text
        scrapeo = ScrapEO(html)

        # Run without options provided (default behavior)
        if not any([title, allmeta, meta, h1]):
            click.echo('Title: %s' % scrapeo.scrape_title())
            try:
                scraped_meta = scrapeo.scrape_meta(DEFAULT_META)
                click.echo('%s' % META_STYLED)
                click.echo('  %s: %s' % (click.style(DEFAULT_META, fg='yellow'), scraped_meta[DEFAULT_META][0]))

            except IndexError:
                pass

            sys.exit(0)

        ### Flags ###

        # --title flag
        if title:
            click.echo('%s: %s' % (TITLE_STYLED, scrapeo.scrape_title()))

        # --h1 flag
        if h1:
            _h1s = scrapeo.scrape_h1s()
            count = 1
            click.echo(H1_STYLED)

            for _h1 in _h1s:
               click.echo('  %d) %s' % (count, _h1))
               count += 1

        if allmeta:
            scraped_meta = scrapeo.scrape_meta()
            click.echo('%s:' % META_STYLED)

            for name in scraped_meta.keys():
                for content in scraped_meta[name]:
                    styled_name = click.style('%s' % name, fg='yellow')
                    click.echo('  %s: %s' % (styled_name, content))

        ### Options w/ args ###

        # --meta option
        if meta:
            scraped_meta = scrapeo.scrape_meta(*meta)
            click.echo('%s:' % META_STYLED)
            for name in scraped_meta.keys():
                for content in scraped_meta[name]:
                    click.echo('  %s: %s' % (click.style(name, fg='yellow'), content))

    except requests.exceptions.RequestException, e:
        # "Bad" status codes, improper input
        if isinstance(e, requests.exceptions.ConnectionError):
            click.echo(click.style('CONNECION ERROR', bg='red'))
            click.echo('%s Possible DNS failure, the connection may have been refused by the host, or the host may be down' % NEG_INDICATOR)

        if isinstance(e, requests.exceptions.HTTPError):
            click.echo(click.style('HTTP ERROR', bg='red'))
            click.echo('%s The server returned an invalid response' % NEG_INDICATOR)

            for arg in e.args:
                click.echo(arg)

        if isinstance(e, requests.exceptions.Timeout):
            click.echo(click.style('TIMEOUT'), bg='red')
            click.echo('%s The request to %s timed out' % (NEG_INDICATOR, url))

        if isinstance(e, requests.exceptions.TooManyRedirects):
            click.echo(click.style('TOO MANY REDIRECTS', bg='red'))
            click.echo('%s Request exceeded the maximum number of redirects' % NEG_INDICATOR)
