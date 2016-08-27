"""
jtools

Usage:
  jtools hello
  jtools left_join --pkey=<col> <file>...
  jtools -h | --help
  jtools --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  jtools left_join --pkey=id file1 file2

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.ibm.com/Davin-Shearer/JsonTools
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    # Dynamically match the command the user is trying to run with a command class
    for k, v in options.iteritems():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            command = [command[1] for command in getmembers(module, isclass) if command[0] != 'Base'][0]
            command = command(options)
            command.run()
