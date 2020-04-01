# -*- coding: utf-8 -*-
#
# This file is part of adsmute.
# Copyright 2020 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>.

"""Load servers from dircrypt format."""


def load(content):
    for line in content:
        # remove after comment char
        line = line.split('#')[0]
        # strip spaces
        line = line.strip()
        # remove multiple spaces
        line = ' '.join(line.split())
        # remove comments
        if len(line) > 0 and not \
                (line.startswith('#') or line.startswith('!')):
            server = line.split(' ')[0]
            # remove localhost
            if server != 'localhost':
                yield server
