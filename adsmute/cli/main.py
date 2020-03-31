# -*- coding: utf-8 -*-
#
# This file is part of adsmute.
# Copyright 2020 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>.

"""CLI main."""

import re
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
    """Download blacklist files."""
    source = list(source)
    with click.progressbar(source, length=len(source)) as bar:
        for x in utils.stream(utils.download, bar):
            name = os.path.join(destination, x['name'])
            if 'download' in x:
                with open(name, 'w') as f:
                    f.write('\n'.join(x['download']).encode('utf8'))
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
    """Extract server names from blacklist files."""
    servers = []
    source = {x['name']: x for x in source}
    process = utils.process()
    check = re.compile(r'^{}$'.format(utils.HOSTNAME_REGEX))
    # for each blacklist file
    filenames = os.listdir(base_path)
    with click.progressbar(filenames, length=len(filenames)) as bar:
        for name in bar:
            # only if contained in config file
            if name in source.keys():
                # load file
                full_name = os.path.join(base_path, name)
                download = utils.load_file(full_name)
                # append processed list
                servers.extend(process(source[name]['format'], download))
    # filter out not valid hostnames
    servers = filter(check.match, set(servers))
    # save results
    destination.write('\n'.join(servers))


@cli.command()
@click.argument('source', type=click.File(mode='r'))
@click.argument('destination', type=click.File(mode='w'))
def dnsmasq(source, destination):
    """Convert server names into dnsmasq configuration."""
    rules = [
        '# Generated by adsmute.',
        '#',
        '# See https://github.com/hachreak/adsmute',
        '#',
    ]
    count = utils.count_lines(source.name)
    with click.progressbar(source, length=count) as bar:
        for server in bar:
            rules.append('address=/{}/127.0.0.1'.format(server.strip()))
    destination.write('\n'.join(rules))
