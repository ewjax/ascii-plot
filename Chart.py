import copy


#
# set up the values for the screen locations of the outer grid.  The
# values to be set up correspond to the following diagram, where the
# (0,0) screen origin is in the upper left corner
# 
#    **************************************************************
#    *                      |                                     *
#    *                   plotOffset.y                             *
#    *                      |                                     *
#    *                      |                                     *
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

    # def __init__(self, series_id: str):
    #     # what character is used to identify this series, and also to plot this series
    #     # best to make this a single character, rather than a full string
    #     self.series_id = series_id
    #
    #     # create empty list of points
    #     self.point_list = list()


class Chart:
    """
    Basic data structure

    Chart has many Series, each of which has many tuples of (x, y) raw data points
    """
    series_dict: dict[str, Series]

    # type declaration

    def __init__(self):

        # create the dictionary of series, with key = series_id, val = Series object
        # best to make the keys a single character, rather than a full string, since they are also
        # used to plot that particular series
        self.series_dict = {}

        # the plotting range will be 115 columns wide, and 74 rows tall
        self.plot_range = (115, 74)

        # the plotting surface will be offset 11 columns from the left, and 3 rows from the top
        self.plot_offset = (11, 3)

        num_cols = self.plot_range[0]
        num_rows = self.plot_range[1]

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

    def add_datapoint(self, x: int, y: int, series_id: str = '1'):

        # which series will this data point be added to?

        # if there is not already a series with the passed series_id, create a new one
        if series_id not in self.series_dict:
            self.series_dict[series_id] = Series()

        # get the desired Series
        point = (x, y)
        s = self.series_dict[series_id]
        s.point_list.append(point)

    def draw(self):

        # find_bounds()
        # draw_axes()
        # draw each series

        # print them to the screen
        for ll in self.lines:
            print(ll)


    def find_bounds(self):

        pass



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
