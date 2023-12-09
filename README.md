# ascii-plot

A utility that provides quick and dirty (x, y) plotting visualization from data contained in an input file, using ascii characters to create the plots.

Each line of the input file is assumed to contain a single data point:
* (x, y) for a single data set (defaults to series_id '1')
* (x, y, series_id) for multiple data sets

Example for a single series to be graphed (series_id defaults to '1'):
```commandline
    1.234   5.678
    2.345   6.789
    etc
```

Example for when multiple series are to be graphed:
```commandline
    1.234   5.678   1
    2.345   6.789   1
    3.456   7.890   1
    12.345  16.789  2
    22.345  26.789  2
    32.345  36.789  2
    etc
```
The values for x and y (and series_id, if included) can be separated by whitespace, commas, semi-colons, or colons.

For multiple data sets, the value of the 'series_id' should ideally be a single alpha-numeric character.

Special cases:  If user wishes to provide special labels for X-Axis, Y-Axis, or Chart Title

Example:
```commandline
    xlabel      X-Axis Label Text
    ylabel      Y-Axis Label Text
    title       Chart Title Text
```




### Build and Installation Steps:
The ascii-plot utility makes use of a virtual python environment, and creates a standalone executable, which can be copied to a local directory such as /usr/local/bin or similar.

The build process is controlled via a makefile.

Build steps:
```
git clone git@github.com:ewjax/ascii-plot.git
cd ascii-plot
make venv
```
Activate the python virtual environment, then continue the build process:
```
(unix): source .ascii-plot.venv/bin/activate
(windows): .ascii-plot.venv\Scripts\activate
make all
Executable will be placed in ./dist subdirectory
```
Test the executable, by running it with the 'help' option:
```
./dist/ascii-plot -h
```
Assuming it shows a list of command line options, indicating it built successfully, copy the ascii-plot (or ascii-plot.exe) executable from the /dist subdirectory to somewhere in your path.

Cleanup steps:
```
(while still in the python virtual environment): 
make clean
deactivate
make venv.clean
```
