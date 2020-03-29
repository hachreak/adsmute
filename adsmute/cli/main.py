
"""CLI main."""

import click
import os
import logging

from . import validation as val
from .. import utils


@click.group()
def cli():
    pass


@cli.command()
@click.argument('source', type=click.File(mode='r'),
                callback=val.load_source)
@click.argument('destination',
                type=click.Path(exists=True, dir_okay=True, writable=True))
def download(source, destination):
    source = list(source)
    with click.progressbar(source, length=len(source)) as bar:
        for x in utils.stream(utils.download, bar):
            name = os.path.join(destination, x['name'])
            if 'download' in x:
                with open(name, 'w') as f:
                    f.write('\n'.join(x['download']))
            if 'error' in x:
                logging.warning(
                    'Url {} return error!\nSee\n{}'.format(
                        x['url'], str(x['error'])
                    )
                )


@cli.command()
@click.argument('source', type=click.File(mode='r'),
                callback=val.load_source)
@click.argument('base_path',
                type=click.Path(exists=True, dir_okay=True, readable=True))
@click.argument('destination', type=click.File(mode='w'))
def servers(source, base_path, destination):
    source = {x['name']: x for x in source}
    process = utils.process()
    servers = []
    filenames = os.listdir(base_path)
    with click.progressbar(filenames, length=len(filenames)) as bar:
        for name in bar:
            if name in source:
                full_name = os.path.join(base_path, name)
                download = utils.load_file(full_name)
                servers.extend(process(source[name]['format'], download))
    destination.write('\n'.join(set(servers)))
