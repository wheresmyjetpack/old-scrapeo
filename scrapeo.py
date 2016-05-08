
import urllib2
import requests
import sys
import click

from bs4 import BeautifulSoup


@click.command()
@click.option('--url')
def cli(url):
    """ Scrap data from webpages that are useful for SEO purposes """
    try:
        req = requests.get(url)

        # Raise an excpetion if request returns "bad" status
        req.raise_for_status()

        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        click.echo(soup.title)

    except requests.exceptions.RequestException, e:
        for arg in e.args:
            print arg
