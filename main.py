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
from scrapeo.utils import opts_provided

DEFAULT_META = 'description'

@click.command()
@click.option('--title', '-t', is_flag='true',
        help='Tell scrapeo to print the title of the document.')
@click.option('--h1', is_flag='true',
        help='Tell scrapeo to print the text node for all h1\'s in the document')
@click.option('--meta', '-m',
        multiple=True,
        help='Search meta tags by name and print their content')
@click.argument('url')
def cli(title, h1, meta, url):
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
        scrapeo = ScrapEO(html)

        # Run without options provided (default behavior)
        if not opts_provided(title, meta, h1):
            click.echo('Title: %s' % scrapeo.scrape_title())
            try:
                click.echo('Meta %s: %s' % (DEFAULT_META, scrapeo.scrape_meta(DEFAULT_META)[DEFAULT_META][0]))

            except IndexError:
                click.echo('Meta %s: %s' % (DEFAULT_META, 'None'))

            sys.exit(0)

        ### Flags ###

        # --title flag
        if title:
            click.echo('Title: %s' % (scrapeo.scrape_title()))

        # --h1 flag
        if h1:
            _h1s = scrapeo.scrape_h1s()
            count = 1

            for _h1 in _h1s:
               click.echo('%d) %s' (count, _h1))
               count += 1

        ### Options w/ args ###

        # --meta option
        if meta:
            for name in meta:
                for meta_content in scrapeo.scrape_meta(name)[name]:
                    click.echo('Meta %s: %s' % (name, meta_content))

    except requests.exceptions.RequestException, e:
        # "Bad" status codes, improper input
        if isinstance(e, requests.exceptions.ConnectionError):
            click.echo('CONNECION ERROR')
            click.echo('[-] Possible DNS failure, the connection may have been refused by the host, or the host may be down')

        if isinstance(e, requests.exceptions.HTTPError):
            click.echo('HTTP ERROR')
            click.echo('[-] The server returned an invalid response')

            for arg in e.args:
                click.echo(arg)

        if isinstance(e, requests.exceptions.Timeout):
            click.echo('TIMEOUT')
            click.echo('[-] The request to %s timed out' % url)

        if isinstance(e, requests.exceptions.TooManyRedirects):
            click.echo('TOO MANY REDIRECTS')
            click.echo('[-] Request exceeded the maximum number of redirects')

        #for arg in e.args:
            #print arg
