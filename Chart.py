import copy


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
        blank_char = '.'
        for i in range(num_cols):
            blank_line += blank_char

        # create a list of blank lines
        for i in range(num_rows):
            self.lines.append(copy.copy(blank_line))

        # create a pair of points to use for scaling, to hold the maxima and minima of all Series
        self.max_raw = (0, 0)
        self.min_raw = (0, 0)

    def add_datapoint(self, x: int, y: int, series_id: str = '1'):

        # which series will this data point be added to?

        # if there is not already a series with the passed series_id, create a new one
        if series_id not in self.series_dict.keys():
            self.series_dict[series_id] = Series()

        # get the desired Series
        point = (x, y)
        s = self.series_dict[series_id]
        s.point_list.append(point)

    def draw(self):

        # find_bounds()
        self.find_bounds()

        # draw_axes()
        # draw each series

        # print them to the screen
        for ll in self.lines:
            print(ll)

    def find_bounds(self):

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

                if x > self.max_raw[0]:
                    self.max_raw = (x, self.max_raw[1])
                if y > self.max_raw[1]:
                    self.max_raw = (self.max_raw[0], y)

                if x < self.min_raw[0]:
                    self.min_raw = (x, self.min_raw[1])
                if y < self.min_raw[1]:
                    self.min_raw = (self.min_raw[0], y)

        # print(self.max_raw, self.min_raw)


def main():

    c = Chart()

    c.add_datapoint(1, 2)
    c.add_datapoint(3, 6)
    c.add_datapoint(5, 4)
    c.add_datapoint(-1, 3)

    c.add_datapoint(11, 21, '2')
    c.add_datapoint(31, 61, '2')
    c.add_datapoint(51, 41, '2')

    c.draw()


if __name__ == '__main__':
    main()
