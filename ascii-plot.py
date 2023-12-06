
import re
import textwrap
import argparse


import _version
import Chart

# command line arguments stored here
args = argparse.Namespace()


def process_command_line() -> None:
    """
    parse the command line
    """

    # ----------------------- set up the argument parser ----------------------
    def formatter(prog): return argparse.RawTextHelpFormatter(prog, max_help_position=52)
    cli_parser = argparse.ArgumentParser(
                                         # formatter_class=argparse.RawTextHelpFormatter,
                                         formatter_class=formatter,
                                         # formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent(f'''
                                            Command line tool to provide a quick plotting tool, using ascii characters,
                                            for data visualization.
                                            '''))

    # ----------------------- add the required, and optional input parameters ----------------------
    # input file
    cli_parser.add_argument('inputfile',
                            type=argparse.FileType('r'),
                            help='input data filename')

    # version
    cli_parser.add_argument('-v', '--version',
                            help='Print version of this utility and exit',
                            action='version',
                            version=f'Version: {_version.__VERSION__}')

    # ----------------------- parse the command line ----------------------
    global args
    args = cli_parser.parse_args()


def process_input_file() -> None:
    """
    process the input file
    note the file is already open, from the command line parsing process
    """

    data_file = args.inputfile
    # split the line using space, tabs, newlines, comma, colons, semicolons
    pattern = r'[ \s,:;]+'
    compiled_pattern = re.compile(pattern)

    # create the Chart instance to acccept the input data
    the_chart = Chart.Chart()

    for (index, line) in enumerate(data_file):
        # get rid of trailing newlines
        line = line.strip()
        # print(f'Index: {index}, line contents [{line}]')

        # split the line into fields
        fields = re.split(pattern, line)
        # print(f'{fields}')

        # line format 1:  x y
        if len(fields) == 2:
            x = float(fields[0])
            y = float(fields[1])
            # print(f'x = {x}, y = {y}')

            the_chart.add_datapoint(x, y)

        # line format 2:  x y series_id
        if len(fields) == 3:
            x = float(fields[0])
            y = float(fields[1])
            series_id = fields[2]
            print(f'x = {x}, y = {y}, series_id = {series_id}')

            the_chart.add_datapoint(x, y, series_id)


    the_chart.draw()


def main():

    process_command_line()
    process_input_file()


if __name__ == '__main__':
    main()
