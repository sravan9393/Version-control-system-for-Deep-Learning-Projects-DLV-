#!/usr/bin/env python3

import argparse
from init import *
from add import *
from commit import *
from status import *

commands_usage = { 'init': 'Used for intializing DLV repository',
                   'add': 'Used for adding files to staging area',
                   'commit': 'tracking the files in the local repository',
                   'status': 'Gives the status of the files'}

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-q', '--quiet', help="Be quiet", action="store_true")
    parser.add_argument('-V', '--verbose', action='count', help="Increase level of verbosity")

    subparsers = parser.add_subparsers(title="dlv commands",
                                       description="Most commonly used DLV commands")

    for key in commands_usage:
        cmd_parser = subparsers.add_parser(key, description=key + " Description", help=commands_usage[key])
        function = 'handle_options_' + key
        globals()[function](cmd_parser)
      
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
