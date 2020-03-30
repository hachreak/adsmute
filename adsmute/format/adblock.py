# -*- coding: utf-8 -*-
#
# This file is part of adsmute.
# Copyright 2020 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>.

"""Load servers from adblock format.

||ads.example.com^$script,image,domain=example.com|~foo.example.info

This rule blocks http://ads.example.com/foo.gif only if the conditions are met.

@@||ads.example.com/notbanner^$~script

Exception rules are built the same as blocking rules, they define which
addresses should be allowed even if matching blocking rules exists.

*Note*: be carefull because it can include many host that you want to block
only partially.

See: https://adblockplus.org/filter-cheatsheet
"""

import re

from ..utils import HOSTNAME_REGEX


def load(content):
    extract = _extract_name()
    servers = []
    exceptions = []

    for line in content:
        # strip spaces
        line = line.strip()
        # check for new server
        if line.startswith('||'):
            line = line[2:]
            name = extract(line)
            if name:
                servers.append(name)
        # check for exceptions
        if line.startswith('@@||'):
            line = line[4:]
            name = extract(line)
            if name:
                exceptions.append(name)

    servers = set(servers) - set(exceptions)
    for s in servers:
        yield s


def _extract_name():
    search = re.compile(r'^{}'.format(HOSTNAME_REGEX))

    def f(line):
        res = search.match(line)
        if res:
            return line[res.start():res.end()]
    return f
