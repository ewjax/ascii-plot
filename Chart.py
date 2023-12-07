import copy
import math


#
# set up the values for the screen locations of the outer grid.  The
# values to be set up correspond to the following diagram, where the
# (0,0) screen origin is in the upper left corner
# 
#    **************************************************************
#    *                         |                                  *
#    *                      plotOffset.y                          *
#    *                         |                                  *
#    *                         |                                  *
#    *                  *************************************     *
#    * plotOffset.x     *   |                               *     *
#    *------------------*   |                               *     *
#    *                  *   |                               *     *
#    *                  *   |                               *     *
#    *                  *   |                               *     *
#    *                  * plotRange.y                       *     *
#    *                  *   |                               *     *
#    *                  *   |                               *     *
#    *                  *   |                               *     *
#    *                  *   |                               *     *
#    *                  *---|-------plotRange.x-------------*     *
#    *                  *   |                               *     *
#    *                  *************************************     *
#    *                                                            *
#    *                                                            *
#    **************************************************************
#


class Series:

    # type declaration
    point_list: list[tuple]

    def __init__(self):
        # create empty list of points
        self.point_list = list()


class Chart:
    """
    Basic data structure

    Chart has many Series, each of which has many tuples of (x, y) raw data points
    """

    # type declaration
    series_dict: dict[str, Series]

    def __init__(self):

        # create the dictionary of series, with key = series_id, val = Series object
        # best to make the keys a single character, rather than a full string, since they are also
        # used to plot that particular series
        self.series_dict = {}

        # the plotting range will be 115 columns wide, and 74 rows tall
        self.plot_range = (115, 74)

        # the plotting surface will be offset 11 columns from the left, and 3 rows from the top
        self.plot_offset = (11, 3)

        num_cols = self.plot_range[0] + self.plot_offset[0] + 5
        num_rows = self.plot_range[1] + self.plot_offset[1] + 5

        # the array of lines where we will 'draw' the plotted data
        self.lines = []

        # create a blank line
        blank_line = ''
        # blank_char = '.'
        blank_char = ' '
        for i in range(num_cols):
            blank_line += blank_char

        # create a list of blank lines
        for i in range(num_rows):
            self.lines.append(copy.copy(blank_line))

        # create a pair of points to use for scaling, to hold the maxima and minima of all Series
        self.max_raw = (0, 0)
        self.min_raw = (0, 0)

        # labels
        self.title = 'This is the Chart Title'
        self.xlabel = 'This is the X-Axis Label'
        self.ylabel = 'This is the Y-Axis Label'

    def add_datapoint(self, x: float, y: float, series_id: str = '1') -> None:
        """
        Add a datapoint to the indicated Series

        :param x: x value
        :param y: y value
        :param series_id: best to make the series_id values a single character, rather than a full string, since they are also
        used to plot that particular series
        """
        # if there is not already a series with the passed series_id, create a new one
        if series_id not in self.series_dict.keys():
            self.series_dict[series_id] = Series()

        # get the desired Series, and add the datapoint to it
        point = (x, y)
        s = self.series_dict[series_id]
        s.point_list.append(point)

    def draw(self) -> None:
        """
        The main drawing routine, which calls each of the sub-pieces in turn
        """
        # find_bounds(), determine the X and Y maxima and minima for all series, for use in scaling
        self.find_bounds()

        # draw_axes()
        self.draw_axes()

        # draw each series
        self.draw_series()

        # print them to the screen
        for ll in self.lines:
            print(ll)

    def find_bounds(self) -> None:
        """
        Walk the list of Series and then each list of datapoints, to find
        the raw values maxima and minima, for use in scaling the raw data
        onto the plotting surface
        """
        # start with the 0-th point in the 0-th graph
        series_id_list = list(self.series_dict.keys())
        if len(series_id_list) > 0:
            series = self.series_dict[series_id_list[0]]
            if len(series.point_list) > 0:
                self.max_raw = series.point_list[0]
                self.min_raw = series.point_list[0]

        # walk the dict of Series
        for series_id in series_id_list:
            series = self.series_dict[series_id]
            # print(series.point_list)

            # walk the list of datapoints
            for point in series.point_list:
                x = point[0]
                y = point[1]

                # preserve the maximum and minimum x and y values
                if x > self.max_raw[0]:
                    self.max_raw = (x, self.max_raw[1])
                if y > self.max_raw[1]:
                    self.max_raw = (self.max_raw[0], y)

                if x < self.min_raw[0]:
                    self.min_raw = (x, self.min_raw[1])
                if y < self.min_raw[1]:
                    self.min_raw = (self.min_raw[0], y)

        # print(self.max_raw, self.min_raw)

    def transform(self, raw_x: float, raw_y: float) -> tuple:
        """
        Transform a raw (x, y) floating point data pair into the (row, col) integer screen positions

        :param raw_x:
        :param raw_y:
        :return: a tuble with the transformed (x, y) data
        """
        transform_x = round(self.plot_offset[0] +
                            self.plot_range[0] * (raw_x - self.min_raw[0]) /
                            (self.max_raw[0] - self.min_raw[0])
                            )

        transform_y = round(self.plot_offset[1] +
                            self.plot_range[1] * (1.0 - (raw_y - self.min_raw[1]) /
                            (self.max_raw[1] - self.min_raw[1]))
                            )

        return transform_x, transform_y

    def draw_string(self, x: int, y: int, the_string: str) -> None:
        """
        Draw a character at position (x, y)
        x and y values are assumed to already be transformed to screen coordinates
        :param x:
        :param y:
        :param the_string:
        """
        self.lines[y] = self.lines[y][:x] + the_string + self.lines[y][x + len(the_string):]

    def draw_axes(self) -> None:
        """
        Draw the basic features of the Chart
            - Chart title, X-Axis label, Y-Axis Label
            - numeric values for the max and min X and Y values on the series plots
            - the lines for the outer borders, and the lines for the X and Y zero axes
        """
        # do graph title
        self.draw_string(self.plot_offset[0] + round((self.plot_range[0] - len(self.title)) / 2),
                         self.plot_offset[1] - 2,
                         self.title)

        # do x-axis label
        self.draw_string(self.plot_offset[0] + round((self.plot_range[0] - len(self.xlabel)) / 2),
                         self.plot_offset[1] + self.plot_range[1] + 2,
                         self.xlabel)

        # do y-axis label
        for i in range(len(self.ylabel)):
            plot_char = self.ylabel[i]
            self.draw_string(self.plot_offset[0] - 5,
                             self.plot_offset[1] + round((self.plot_range[1] - len(self.ylabel))/2) + i,
                             plot_char)

        # do the range labels
        # each label will be in the form +1.23e+45
        # x-min label
        label = f'{self.min_raw[0]:.2E}'
        self.draw_string(self.plot_offset[0],
                         self.plot_offset[1] + self.plot_range[1] + 1,
                         label)

        # x-max label
        label = f'{self.max_raw[0]:.2E}'
        self.draw_string(self.plot_offset[0] + self.plot_range[0] + 1 - len(label),
                         self.plot_offset[1] + self.plot_range[1] + 1,
                         label)

        # y-min label
        label = f'{self.min_raw[1]:.2E}'
        self.draw_string(self.plot_offset[0] - len(label) - 1,
                         self.plot_offset[1] + self.plot_range[1],
                         label)

        # y-max label
        label = f'{self.max_raw[1]:.2E}'
        self.draw_string(self.plot_offset[0] - len(label) - 1,
                         self.plot_offset[1],
                         label)

        # do top/bottom lines
        # outer_horiz_line = '='
        outer_horiz_line = '*'
        for x in range(self.plot_range[0] + 1):
            # top line
            self.draw_string(self.plot_offset[0] + x,
                             self.plot_offset[1],
                             outer_horiz_line)

            # bottom line
            self.draw_string(self.plot_offset[0] + x,
                             self.plot_offset[1] + self.plot_range[1],
                             outer_horiz_line)

        # do side lines
        # outer_vert_line = '|'
        outer_vert_line = '*'
        for y in range(0, self.plot_range[1] + 1):
            # left side
            self.draw_string(self.plot_offset[0],
                             self.plot_offset[1] + y,
                             outer_vert_line)

            # right side
            self.draw_string(self.plot_offset[0] + self.plot_range[0],
                             self.plot_offset[1] + y,
                             outer_vert_line)

        # do the 0 axes, if in range
        (screen_zero_x, screen_zero_y) = self.transform(0.0, 0.0)

        # vertical axis
        # axis_vertical_line = '/'
        axis_vertical_line = '|'
        if (self.min_raw[0] < 0.0) and (self.max_raw[0] > 0.0):
            for y in range(1, self.plot_range[1]):
                self.draw_string(screen_zero_x,
                                 self.plot_offset[1] + y,
                                 axis_vertical_line)

        # horiz axis
        # axis_horiz_line = '+'
        axis_horiz_line = '-'
        if (self.min_raw[1] < 0.0) and (self.max_raw[1] > 0.0):
            for x in range(1, self.plot_range[0]):
                self.draw_string(self.plot_offset[0] + x,
                                 screen_zero_y,
                                 axis_horiz_line)

        # horiz and vertical axis intersection
        axis_center = '+'
        if ((self.min_raw[1] < 0.0)
                and (self.max_raw[1] > 0.0)
                and (self.min_raw[0] < 0.0)
                and (self.max_raw[0] > 0.0)):
            self.draw_string(screen_zero_x,
                             screen_zero_y,
                             axis_center)

    def draw_series(self) -> None:
        """
        Walk the list of all series, and plot the datapoints for each onto the Chart
        """
        # walk the list of series
        for series_id in self.series_dict.keys():
            series = self.series_dict[series_id]

            # now walk the list of data point
            # walk the list of datapoints
            for point in series.point_list:
                x = point[0]
                y = point[1]

                (transformed_x, transformed_y) = self.transform(x, y)
                self.draw_string(transformed_x,
                                 transformed_y,
                                 series_id)


def main():

    c = Chart()

    # c.add_datapoint(1, 2)
    # c.add_datapoint(3, 6)
    # c.add_datapoint(5, 4)
    # c.add_datapoint(-1, 3)
    #
    # c.add_datapoint(11, 21, '2')
    # c.add_datapoint(31, 61, '2')
    # c.add_datapoint(51, 41, '2')

    # for i in range(-5, 5):
    #     c.add_datapoint(i, i, '3')
    #     c.add_datapoint(i, -2*i, '4')

    for i in range(37):
        x = 2*math.pi / 36.0 * i
        y = math.sin(x)
        c.add_datapoint(x, y, '5')

        y = math.cos(x)
        c.add_datapoint(x, y, '7')

    # for i in range(-10, 21):
    #     x = i
    #     y = x * x - 100
    #     c.add_datapoint(x, y, '6')

    c.draw()

    # (x,y) = c.transform(0, 0)
    #
    # c.draw_char(x, y, '+')
    # c.draw()


if __name__ == '__main__':
    main()
