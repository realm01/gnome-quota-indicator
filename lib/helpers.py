"""Helper functions."""

import subprocess as sp
import os
import yaml


def load_config():
    """"Load configuration format it and return it."""
    with open(get_path('../app.conf')) as file:
        config = yaml.load(file)

    use_etc_exports = config.get('use_etc_exports')
    if config.get('fs') is None or not isinstance(config.get('fs'), list):
        config['fs'] = []

    if use_etc_exports is not None and use_etc_exports is True:
        try:
            with open('/etc/exports') as efile:
                line = efile.readline()
                while line:
                    if line.strip()[0] == '#':
                        line = efile.readline()
                        continue

                    config['fs'].append(line.strip().split()[0])
                    line = efile.readline()
        except:
            print('/etc/exports not found.')

    return config


def sys_call(cmd):
    """Execute a system call and return utf-8 formated output."""
    proc = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
    out = proc.communicate()
    out = out[0].decode('utf-8')

    return out


def get_path(file):
    """Build absolute path for __file___ and append filename."""
    if file is None:
        file = ''

    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
