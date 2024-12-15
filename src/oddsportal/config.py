import tomllib

def parse_config(path = 'config.toml'):
    with open(path, 'rb') as f:
        result = tomllib.load(f)
    return result
