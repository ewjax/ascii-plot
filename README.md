# ascii-plot


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
