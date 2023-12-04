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

    def __init__(self, plot_char: str):
        # what character is used to plot this series
        self.plot_char = plot_char

        # create empty list of points
        self.pointList = list()



class Chart:
    """
    Basic data structure

    Chart has many Series, each of which has many tuples of (x, y) raw data points
    """

    def __init__(self, num_series: int = 1):

        # create the list of num_series series
        self.seriesList = list()
        for i in range(num_series):
            # each series is a list of points
            s = Series('1')
            self.seriesList.append(s)

        # the plotting range will be 115 columns wide, and 74 rows tall
        self.plotRange = (115, 74)

        # the plotting surface will be offset 11 columns from the left, and 3 rows from the top
        self.plotOffset = (11, 3)

        num_cols = self.plotRange[0]
        num_rows = self.plotRange[1]

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

    def draw(self):

        for ll in self.lines:
            print(ll)


def main():

    c = Chart()
    c.draw()


if __name__ == '__main__':
    main()
