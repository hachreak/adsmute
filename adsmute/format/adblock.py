
"""Load servers from adblock format.

||ads.example.com^$script,image,domain=example.com|~foo.example.info

This rule blocks http://ads.example.com/foo.gif only if the conditions are met.

@@||ads.example.com/notbanner^$~script

Exception rules are built the same as blocking rules, they define which
addresses should be allowed even if matching blocking rules exists.

See: https://adblockplus.org/filter-cheatsheet
"""

import re


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
    pattern = '^[0-9a-zA-Z]+[\.0-9a-zA-Z]+'

    def f(line):
        res = re.match(pattern, line)
        if res:
            return line[res.start():res.end()]
    return f
