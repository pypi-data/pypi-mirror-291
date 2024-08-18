import platform


def parse_platform():
    system = platform.system()
    architecture = platform.machine()
    system_mapping = {'Linux': 'linux', 'Darwin': 'osx', 'Windows': 'win'}
    if system == 'Windows':
        architecture = 'x64' if architecture == 'AMD64' else 'x86'
    elif system == 'Darwin':
        architecture = 'x64' if architecture == 'x86_64' else 'arm64'
    elif system == 'Linux':
        architecture = 'x64' if architecture == 'x86_64' else 'arm'
    return system_mapping[system], architecture


def parse_log_level(log: str):
    for level in ('info', 'warn'):
        if log.startswith(level):
            return False
    if log.startswith('['):
        level = log.split(' ')[3]
        return level.lstrip('[').rstrip(']:')
