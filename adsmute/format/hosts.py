
"""Load servers from hosts format."""


def load(content):
    for line in content:
        # strip spaces
        line = line.strip()
        # remove multiple spaces
        line = ' '.join(line.split())
        # remove comments
        if len(line) > 0 and not line.startswith('#'):
            splits = line.split(' ')
            # remove initial address and localhost
            servers = filter(lambda x: x != 'localhost', splits[1:])
            for server in servers:
                yield server
