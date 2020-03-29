
"""Utils."""

import json
import requests


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
