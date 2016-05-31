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
from scrapeo.utils import format_meta_out, rebuild_url, handle_errors


""" Constants """
# Defaults
DEFAULT_META = 'description'

# Styled text
H1_STYLED = click.style('h1\'s', fg='green')
TITLE_STYLED = click.style('Title', fg='green')
META_STYLED = click.style('Meta', fg='green')
ARTICLE_STYLED = click.style('Article', fg='yellow')
SECTION_STYLED = click.style('Section', fg='yellow')
CONTENT_STYLED = click.style('Content', fg='yellow')

# Misc.
TRUNCATE_LENGTH = 100

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

        # Raise an exception if request returns "bad" status
        req.raise_for_status()
        html = req.text
        scrapeo = ScrapEO(html)

        # Run without options provided (default behavior)
        if not any([title, allmeta, meta, h1, articles]):
            scraped_meta = scrapeo.scrape_meta(DEFAULT_META)
            click.echo('%s: %s' % (TITLE_STYLED, scrapeo.scrape_title()))
            click.echo('%s' % META_STYLED)

            for i in format_meta_out(scraped_meta):
                click.echo(i)

            sys.exit(0)

        """ Flags and Options """

        # --title flag
        if title:
            click.echo('\n%s: %s' % (TITLE_STYLED, scrapeo.scrape_title()))

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

            for i in format_meta_out(scraped_meta):
                click.echo(i)

        # --articles option
        if articles:
            scraped_articles = scrapeo.scrape_articles()
            click.echo('\n%s article(s) found in the document' % click.style(str(len(scraped_articles)), fg='green'))

            for article in scraped_articles:
                click.echo('  %s: %s' % (ARTICLE_STYLED, click.style(article['heading'], fg='green')))

                for section in article['sections']:
                    try:
                        click.echo('    %s: %s' % (SECTION_STYLED, click.style(section['heading'], fg='green')))
                    except KeyError:
                        click.echo('    %s: %s' % (SECTION_STYLED, click.style('NO HEADING', bg='blue')))

                    # Display the first 24 characters from the first
                    # paragraph in the content
                    truncated_content = '%s...' % section['content'][0][:TRUNCATE_LENGTH]
                    click.echo('      %s: %s' % (CONTENT_STYLED, truncated_content))

    except requests.exceptions.RequestException, e:
        # "Bad" status codes, improper input
        handle_errors(e)
