
# todo change build so result is standalone executable

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

    # ----------------------- add the required, and optional command line parameters ----------------------
    # input file
    cli_parser.add_argument('inputfile',
                            type=argparse.FileType('r'),
                            help='input data filename')

    # version
    cli_parser.add_argument('-v', '--version',
                            help='Print version of this utility and exit',
                            action='version',
                            version=f'Version: {_version.__VERSION__}')

    # todo - need an option to show input file format

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

    # create the Chart instance to acccept the input data
    the_chart = Chart.Chart()

    # read in all the input data
    for (index, line) in enumerate(data_file):
        # get rid of trailing newlines
        line = line.strip()
        # print(f'Index: {index}, line contents [{line}]')

        # split the line into fields
        fields = re.split(pattern, line)
        # print(f'{fields}')

        # special line format: xlabel
        if fields[0].casefold() == 'xlabel':
            # redo the split, but just once, to strip off the special 'xlabel' delimiter and preserve the rest
            fields = re.split(pattern, line, maxsplit=1)
            the_chart.xlabel = fields[1]

        # special line format: ylabel
        elif fields[0].casefold() == 'ylabel':
            # redo the split, but just once, to strip off the special 'ylabel' delimiter and preserve the rest
            fields = re.split(pattern, line, maxsplit=1)
            the_chart.ylabel = fields[1]

        # special line format: title
        elif fields[0].casefold() == 'title':
            # redo the split, but just once, to strip off the special 'title' delimiter and preserve the rest
            fields = re.split(pattern, line, maxsplit=1)
            the_chart.title = fields[1]

        # line format 1:  x y
        elif len(fields) == 2:
            x = float(fields[0])
            y = float(fields[1])
            # print(f'x = {x}, y = {y}')

            the_chart.add_datapoint(x, y)

        # line format 2:  x y series_id
        elif len(fields) == 3:
            x = float(fields[0])
            y = float(fields[1])
            series_id = fields[2]
            print(f'x = {x}, y = {y}, series_id = {series_id}')

            the_chart.add_datapoint(x, y, series_id)

    # and finally, we get to the payoff
    # tell the chart to draw itself
    the_chart.draw()


def main() -> None:

    # process the command line input parameters
    process_command_line()

    # read all lines from the input file
    process_input_file()


if __name__ == '__main__':
    main()
