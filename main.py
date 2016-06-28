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
from scrapeo.utils import echo_meta, rebuild_url, handle_errors


""" Constants """
# Defaults
DEFAULT_META = 'description'
TRUNCATE_LENGTH = 100

# Styled text
H1_STYLED = click.style('h1\'s', fg='green')
TITLE_STYLED = click.style('Title', fg='green')
META_STYLED = click.style('Meta', fg='green')
ARTICLE_STYLED = click.style('Article', fg='yellow')
SECTION_STYLED = click.style('Sub-sections', fg='yellow')
CONTENT_STYLED = click.style('Content', fg='yellow')
HEADING_STYLED = click.style('Heading', fg='yellow')

@click.command()
@click.option('--title', '-t', is_flag='true',
        help='Tell scrapeo to print the title of the document')
@click.option('--h1', is_flag='true',
        help='Tell scrapeo to print the text node for all h1\'s in the document')
@click.option('--allmeta', '-a', is_flag='true',
        help='Tell scrapeo to print the content (if it exists) from all self-closing meta tags')
@click.option('--articles', '-r', is_flag='true',
        help='Tell scrapeo to print any articles on the page')
@click.option('--meta', '-m',
        multiple=True,
        help='Search meta tags by name and print their content')
@click.argument('url')
def cli(title, h1, allmeta, meta, articles, url):
    """ Scrape data from a document found at URL for SEO data analysis """

    # Rebuild URL if schema is not provided
    url = rebuild_url(url)

    try:
        req = requests.get(url)
        req.raise_for_status()    # Raise an exception if request returns "bad" status

    except requests.exceptions.RequestException, e:
        # "Bad" status codes, improper input
        handle_errors(e)

    else:
        html = req.text
        scrapeo = ScrapEO(html)

        # Run without options provided (default behavior)
        if not any([title, allmeta, meta, h1, articles]):
            scraped_meta = scrapeo.scrape_meta(DEFAULT_META)
            click.echo('%s: %s' % (TITLE_STYLED, scrapeo.scrape_title()))
            click.echo('%s' % META_STYLED)

            echo_meta(scraped_meta)
            sys.exit(0)

        """ Flags and Options """

        # --title flag
        if title:
            scraped_title = scrapeo.scrape_title()

            if not scraped_title:
                scraped_title = click.style('NO TITLE', bg='blue')

            click.echo('\n%s: %s' % (TITLE_STYLED, scraped_title))

        # --h1 flag
        if h1:
            _h1s = scrapeo.scrape_h1s()
            count = 1
            click.echo('\n%s' % H1_STYLED)

            for _h1 in _h1s:
               click.echo('  %d) %s' % (count, _h1))
               count += 1

        if allmeta or meta:

            # --allmeta flag
            if allmeta:
                scraped_meta = scrapeo.scrape_meta()

            # --meta option
            elif meta:
                scraped_meta = scrapeo.scrape_meta(*meta)

            click.echo('\n%s:' % META_STYLED)
            echo_meta(scraped_meta)

        # --articles option
        if articles:
            outline = scrapeo.outline()
            num_articles = click.style(str(len(outline)), fg='green')

            click.echo('\n%s article(s) found in the document' % num_articles)
            print_sectioning_content(outline)

def print_sectioning_content(outline, spacing=""):

    for section in outline:
        click.echo('\n%s%s: %s' % (spacing, click.style('Type', fg='yellow'), section['type']))

        try:
            click.echo('%s%s: %s' % (spacing, HEADING_STYLED, section['heading']))
        except KeyError:
            # No heading for this section
            click.echo('%s%s: NONE' % (spacing, HEADING_STYLED))

        for content in section['content']:
            click.echo('%s%s: %s' % (spacing, CONTENT_STYLED, content))

        if any(section['sections']):
            click.echo('%s%s:' % (spacing, SECTION_STYLED))
            indent = spacing + "  "
            print_sectioning_content(section['sections'], spacing=indent)
