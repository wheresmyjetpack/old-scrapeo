from click import style, echo
import requests.exceptions


NEG_INDICATOR = style('[-]', fg='red')


def opts_provided(*args):
    # No longer in use, redundant
    return any(args)

def format_meta_out(scraped_meta):
    # Return a list of strings each containing the value of the scraped
    # meta tags' name and content attributes
    meta_out = []

    for name, name_content in scraped_meta.iteritems():
        for content in name_content:
            meta_out.append('  %s: %s' % (style(name, fg='yellow'), content))

    return meta_out

def rebuild_url(url):
    if not (url[:7] == 'http://' or url[:8] == 'https://'):
        url = 'http://%s' % url
        echo('Rebuilt url to %s...\n' % style(url, fg="yellow"))

    return url.decode('utf-8')

def handle_errors(e):
    if isinstance(e, requests.exceptions.ConnectionError):
        echo(style('CONNECION ERROR', bg='red'))
        echo('%s Possible DNS failure, the connection may have been refused by the host, or the host may be down' % NEG_INDICATOR)

    if isinstance(e, requests.exceptions.HTTPError):
        echo(style('HTTP ERROR', bg='red'))
        echo('%s The server returned either a "bad" status code or an invalid response' % NEG_INDICATOR)

        for arg in e.args:
            echo(arg)

    if isinstance(e, requests.exceptions.Timeout):
        echo(style('TIMEOUT'), bg='red')
        echo('%s The request to %s timed out' % (NEG_INDICATOR, url))

    if isinstance(e, requests.exceptions.TooManyRedirects):
        echo(style('TOO MANY REDIRECTS', bg='red'))
        echo('%s Request exceeded the maximum number of redirects' % NEG_INDICATOR)
