
#ifndef __BASEPLOT_H
#define __BASEPLOT_H

#include <math.h>
#include <string.h>
                 
#include <utility>
#include <list>

using namespace std;                 

// handy typedefs - the stl 'first' and 'second' values
// will represent 'x' and 'y' values, respectively
typedef pair<double, double> DoublePair;
typedef pair<int, int> IntPair;

// forward declaration
class GraphElement;

//
// base class for plot 
//
class BasePlot
{
protected:

    // pointer to array of {doublelists of DoublePairs}
    list<GraphElement*> *geList;

    // number of graphs in this plot
    int numGraphs;

    // which graph is current, 0 to (maxgraphs-1)
    int current;

    // maximum, minimum values in real units
    DoublePair maxPair;
    DoublePair minPair;

    // Range and Offset values in "screen" units
    IntPair screenRange;
    IntPair screenOffset;

    // x and y axis labels, and overall plot title
    char *title;
    char *xlabel;
    char *ylabel;

    // load max and min values into maxPair, minPair
    void FindBounds();

    // plot all the contents of the graph, all curves/points
    void            DrawGraphs();
    virtual void    GraphInit(int which);

    // transform raw data into screen coordinate
    IntPair         Transform(DoublePair& raw);

    // utility function
    static int      Round(double value);


    //
    // pure virtual functions which must be defined by Child classes
    //

    // set values for viewport
    virtual void    ScreenValues() = 0;

    // draw the basic axes
    virtual void    DrawAxes() = 0;

    // processes to occur before and after the plotting
    virtual void    PreProcess() = 0;
    virtual void    PostProcess() = 0;

public:

    BasePlot(int numGraphs = 1);
    virtual ~BasePlot();

    // set and get the current graph number, 0 to (maxgraphs-1)
    int             GetCurrentGraph() {return current;}
    void            SetCurrentGraph(int c);

    // add a graph element
    void            AddElement(GraphElement *ge);

    // set the title, x and y labels
    void            SetTitle(const char *s);
    void            SetXLabel(const char *s);
    void            SetYLabel(const char *s);

    // clear all points in the current graph
    void            ClearCurrent();

    // clear all points in all graphs
    void            Clear();

    // draw the plot
    void            Draw();
};


//
// GraphElement base class for all child graphing classes
//
// The 'owner' pointer is a pointer to the BasePlot object that contains
// the graph elements, and is typically used in order to access the
// owner->transform(DoublePair) function, which transforms the raw data
// contained in the graph element data members into actual screen
// coordinates for use in actual screen drawing functions.  It is not
// necessary to call setOwner(), this is done automatically in
// BasePlot::addElement(GraphElement *).
//
// Child classes must provide definitions for 3 virtual functions:
//    void Plot();              Paint self
//    DoublePair GetMax();      Provide a DoublePair with the max x,y values
//                              which 'contain' this entire GraphElement
//    DoublePair GetMin();      Similar to getMax()
//
// getMax() and getMin() thus define two DoublePairs which taken together,
// represent a rectangle which completely bounds this GraphElement.  These
// values are used in the automatic scaling routines of the plotting
// engine, to ensure that all the GraphElements of this particular plot
// will fit on the screen.
//
class GraphElement
{
protected:

    BasePlot *owner;

public:

    // ctor, dtor
    GraphElement() {}
    virtual ~GraphElement() {}

    // set the owner
    void SetOwner(BasePlot *bp) {owner = bp;}


    //
    // pure virtuals to be defined by children
    //

    // every element must know how to plot itself
    virtual void Plot() = 0;

    // these functions define a rectangle which will bound the element
    virtual DoublePair GetMax() = 0;
    virtual DoublePair GetMin() = 0;
};


#endif //#ifndef __BASEPLOT_H
