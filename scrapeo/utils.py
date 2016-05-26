import click

def opts_provided(*args):
    return any(args)

def format_meta_out(scraped_meta):
    meta_out = []
    for name in scraped_meta.keys():
        for content in scraped_meta[name]:
            meta_out.append('  %s: %s' % (click.style(name, fg='yellow'), content))

    return meta_out
