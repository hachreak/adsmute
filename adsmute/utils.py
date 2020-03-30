# -*- coding: utf-8 -*-
#
# This file is part of adsmute.
# Copyright 2020 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>.

"""Utils."""

import json
import requests
import importlib


def load_source(filename):
    source = json.load(filename)
    return filter(lambda x: x.get('enabled', False), source['sources'])


def stream(fun, stream):
    """Apply fun to a stream."""
    for value in stream:
        yield fun(value)


def download(x):
    """Download file."""
    try:
        req = requests.get(x['url'])
        if req.status_code == 200:
            x['download'] = req.text.split('\n')
    except requests.exceptions.ConnectionError as e:
        x['error'] = e
    return x


def load_file(name):
    content = []
    with open(name, 'r') as f:
        for line in f:
            content.append(line)
    return content


def count_lines(filename):
    """Count file lines."""
    return sum(1 for i in open(filename, 'rb'))


def process():
    """Chose best processing function depending on text format."""
    modules = {}

    def _get_modules(format_name):
        if format_name not in modules:
            module = 'adsmute.format.{}'.format(format_name)
            module = importlib.import_module(module)
            modules[format_name] = module
        return modules[format_name]

    def f(format_name, download):
        return list(_get_modules(format_name).load(download))
    return f
