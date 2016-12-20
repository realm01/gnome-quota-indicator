"""Helper functions."""

import subprocess as sp
import os
import yaml
from lib.exception_feedback import show_cmd_error


def getuid():
    """Same as os.getuid() but returns a str."""
    return str(os.getuid())


def load_config():
    try:
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

        if config.get('refresh') is None:
            config['refresh'] = {}

        if config['refresh'].get('quota_rate') is None:
            config['refresh']['quota_rate'] = 15 * 1000 * 60
        else:
            config['refresh']['quota_rate'] *= 1000 * 60

        if config['refresh'].get('fs_rate') is None:
            config['refresh']['fs_rate'] = 15 * 1000 * 60
        else:
            config['refresh']['fs_rate'] *= 1000 * 60

        if config['refresh'].get('warning') is None:
            config['refresh']['warning'] = 60 * 1000 * 60
        else:
            config['refresh']['warning'] *= 1000 * 60

        if config['refresh'].get('critical') is None:
            config['refresh']['critical'] = 30 * 1000 * 60
        else:
            config['refresh']['critical'] *= 1000 * 60

        return config
    except Exception as e:
        show_cmd_error('Failed to read configuration file', e)
        raise e

def sys_call(cmd):
    """Execute a system call and return utf-8 formated output."""
    try:
        proc = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
        out = proc.communicate()
        out = out[0].decode('utf-8')
        return out
    except Exception as e:
        show_cmd_error('Failed to execute shell command', e)
        raise e


def get_path(file):
    """Build absolute path for __file___ and append filename."""
    if file is None:
        file = ''

    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
