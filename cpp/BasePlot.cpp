
#include "BasePlot.h"


//
// BasePlot() constructor
//
// construct the base plot.  The passed value is used to determine the
// max number of graphs which will be contained in this plot, default 1
//
BasePlot::BasePlot(int aNumGraphs) : numGraphs(aNumGraphs), current(0), xlabel(0), ylabel(0), title(0)
{
    // allocate memory for the array of {doublelists of DoublePair} types
    geList = new list<GraphElement*> [numGraphs];
}


//
// ~BasePlot() destructor
//
// free up allocated memory
//
BasePlot::~BasePlot()
{
    delete[] geList;
    delete[] xlabel;
    delete[] ylabel;
    delete[] title;
}


//
// setTitle()
//
// function to set the value of the overall title
//
void BasePlot::SetTitle(const char *s)
{
    delete[] title;
    title = new char[strlen(s)+1];
    strcpy(title, s);
}

//
// setXLabel()
//
// function to set the value of the X label.
//
void BasePlot::SetXLabel(const char *s)
{
    delete[] xlabel;
    xlabel = new char[strlen(s)+1];
    strcpy(xlabel, s);
}

//
// setYLabel()
//
// function to set the value of the X label.
//
void BasePlot::SetYLabel(const char *s)
{
    delete[] ylabel;
    ylabel = new char[strlen(s)+1];
    strcpy(ylabel, s);
}



//
// draw()
//
// draw the plot on the screen
//

void BasePlot::Draw()
{
    // pre-plotting processes
    PreProcess();

    // set max, min, and plot axes
    FindBounds();
    DrawAxes();

    // draw the contents
    DrawGraphs();

    // post-plotting processes
    PostProcess();
}


//
// plot all the contents of the graph, all curves/points
//
void BasePlot::DrawGraphs()
{
    // plot all points, all curves
    for (int c = 0; c < numGraphs; c++)
    {
        // init each graph, set colors, etc.
        GraphInit(c);

        list<GraphElement*>::iterator iter = geList[c].begin();
        while (iter != geList[c].end())
        {
            GraphElement *ge = *iter++;
            ge->Plot();
        }
    }
}

//
// do any necessary setup for this graph, colors, plotting char, etc
//
void BasePlot::GraphInit(int c)
{
    current = c;
}



//
// findBounds()
//
// Determine the maximum and minimum values for X and Y, and store them
// in the maxPair and minPair DoublePair data members.  
//
// maxPair and minPair therefore represent
// a bounding rectangle for the data contained in all the graphs
//
void BasePlot::FindBounds()
{
    // start with the 0-th point in the 0-th graph
    if (geList[0].size() > 0)
    {
        GraphElement *ge = geList[0].front();
        maxPair = ge->GetMax();
        minPair = ge->GetMin();
    }
    else
    {
        maxPair.first = maxPair.second = 0;
        minPair.first = minPair.second = 0;
    }

    // for each graph in the plot...
    for (int c = 0; c < numGraphs; c++)
    {
        // for each graphelement in the graph...
        list<GraphElement*>::iterator iter = geList[c].begin();
        while (iter != geList[c].end())
        {
            // get the i-th graphelement
            GraphElement *ge = *iter++;

            DoublePair testmax = ge->GetMax();
            DoublePair testmin = ge->GetMin();

            if (testmax.first > maxPair.first)
                maxPair.first = testmax.first;

            if (testmin.first < minPair.first)
                minPair.first = testmin.first;

            if (testmax.second > maxPair.second)
                maxPair.second = testmax.second;

            if (testmin.second < minPair.second)
                minPair.second = testmin.second;
        }
    }
}


//
// transform()
//
// convert the raw data into the screen coordinates necessary to plot
// data
//
// this algorithm is built assuming that the actual screen coordinate
// system is set up with the origin in the upper left corner, as is common
// with most systems.
//
IntPair BasePlot::Transform(DoublePair& raw)
{
    IntPair Coord;

    Coord.first = Round( screenRange.first * (raw.first - minPair.first) / (maxPair.first - minPair.first) );
    Coord.second = screenRange.second - Round( screenRange.second * (raw.second - minPair.second) / (maxPair.second - minPair.second) );

    Coord.first += screenOffset.first;
    Coord.second += screenOffset.second;

    return Coord;
}


//
// clear()
//
// clear all points in all graphs
//
void BasePlot::Clear()
{
    int tmp = GetCurrentGraph();

    for (int i = 0; i < numGraphs; i++)
    {
        SetCurrentGraph(i);
        ClearCurrent();
    }

    SetCurrentGraph(tmp);
}


//
// currentGraph()
//
// a function to allow the setting of the 'current' data member, indicating
// which graph is gaining the data points.
//
void BasePlot::SetCurrentGraph(int c)
{
    if ( (c >=0) && (c < numGraphs) )
        current = c;
}


//
// function to add a graphing element
//
void BasePlot::AddElement(GraphElement *ge)
{
    if (ge)
    {
        ge->SetOwner(this);
        geList[current].push_back(ge);
    }
}

//
// clear all points from the current graph
//
void BasePlot::ClearCurrent()
{
    while (geList[current].size() > 0)
    {
        GraphElement *ge = geList[current].back();
        delete ge;
        geList[current].pop_back();
    }
}


//
// round()
//
// function which will round any value to the nearest integer
//
int BasePlot::Round(double value)
{
    return (int) floor(value + 0.5);
}




