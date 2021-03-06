import os

import yaml

from .logger import Logger

class Generator(object):
    def __init__(self, base_directory):
        self._log = Logger()
        self._setup_context(base_directory)

    def _setup_context(self, base_directory):
        path = os.path.abspath(os.path.realpath(
            os.path.expanduser(base_directory)))
        if not os.path.exists(path):
            raise DispatchError('Nonexistent base directory')
        self._path = path

    def generate(self, types):
        log = self._log
        lines = []
        for type in types:
            try:
                self._log.info('Generating types for %s' % type['src'])
                if 'description' in type.keys():
                    lines.append('\n## %s' % type['description'])
                else:
                    lines.append('\n##')
                lines.extend(self._generate(type))
            except KeyError as e:
                raise DispatchError('Type %s is issing key %s' % (type, e))
            except Exception as e:
                self._log.error('Error processing %s' % e)
        return lines

    def _generate(self, type):
        path = os.path.join(self._path, type['src'])
        lines = []
        with open(path) as fin:
            data = yaml.safe_load(fin)
        if data:
            longest = max(map(len, data))
            for ext in data:
                lines.append(('%s' % ext).ljust(longest + 2) + '%s' % type['colour'])
        return lines

class DispatchError(Exception):
    pass
