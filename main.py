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

@click.command()
@click.option('--title', '-t', is_flag='true',
        help='Tell scrapeo to print the title of the document.')
@click.option('--meta', '-m',
        help='Search meta tags by name and print their content')
@click.option('--h1', is_flag='true',
        help='Tell scrapeo to print the text node for all h1\'s in the document')
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
            click.echo('Meta description %s' % scrapeo.scrape_meta('description'))
            sys.exit(0)

        # Flags
        if title:
            click.echo('Title: %s' % (scrapeo.scrape_title()))

        if h1:
            _h1s = scrape_h1s()
            count = 1

            for _h1 in _h1s:
               click.echo('%d) %s' (count, _h1))
               count += 1

        # Options w/ args
        if meta:
            click.echo(scrapeo.scrape_meta(meta))

    except requests.exceptions.RequestException, e:
        # "Bad" status codes, improper input
        for arg in e.args:
            print arg
