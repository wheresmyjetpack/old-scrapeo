import click

def opts_provided(*args):
    return any(args)

def get_title():
    click.echo('Title: %s' % (scrapeo.scrape_title()))

def get_h1s():
    _h1s = scrapeo.scrape_h1s()
    count = 1

    for _h1 in _h1s:
       click.echo('%d) %s' (count, _h1))
       count += 1

def get_meta(meta):
    for name in meta:
        for meta_content in scrapeo.scrape_meta(name)[name]:
            click.echo('Meta %s: %s' % (name, meta_content))
