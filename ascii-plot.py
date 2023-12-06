
import sys
import argparse
import textwrap


import _version

# command line arguments stored here
args = argparse.Namespace()


def main():

    # *********************************************************************************************************
    # parse the command line
    def formatter(prog): return argparse.RawTextHelpFormatter(prog, max_help_position=52)
    cli_parser = argparse.ArgumentParser(
                                         # formatter_class=argparse.RawTextHelpFormatter,
                                         formatter_class=formatter,
                                         # formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent(f'''
                                            Command line tool to provide a quick plotting tool, using ascii characters,
                                            for data visualization.
                                            '''))


    # version
    cli_parser.add_argument('-v', '--version',
                            help='flag: Print version of this utility and exit',
                            action='store_true')

    # parse the command line
    global args
    args = cli_parser.parse_args()


    # process vbump version command
    if args.version:
        print(f'{_version.__VERSION__}')
        sys.exit(0)



if __name__ == '__main__':
    main()
