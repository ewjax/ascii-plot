
#include <iostream>

#include <strstream>



#include <iomanip>

#include "MemoryPlot.h"

//
// MemoryPlot() constructor
//
// set up the viewport and turn off the cursor
//
MemoryPlot::MemoryPlot(int numGraphs) : BasePlot(numGraphs)
{
    // set up the screenvalues
    ScreenValues();
}

//
// MemoryPlot() destructor
//
// free up allocated memory
//
MemoryPlot::~MemoryPlot(void)
{
    for (int i = 0; i < buffsize.second; i++)
    {
        delete[] membuff[i];
    }
    delete[] membuff;
}

//
// screenValues()
//
// set up the values for the screen locations of the outer grid.  The
// values to be set up correspond to the following diagram:
//
//       Memory Map:
//    ************************************************************
//    *                    |                                     *
//    *                 Offset.second                            *
//    *                    |                                     *
//    *                    |                                     *
//    *                *************************************     *
//    * Offset.first   *   |                               *     *
//    *----------------*   |                               *     *
//    *                *   |                  Plot         *     *
//    *                *   |                               *     *
//    *                *   |                               *     *
//    *                * Range.second                      *     *
//    *                *   |                               *     *
//    *                *   |                               *     *
//    *                *   |                               *     *
//    *                *   |                               *     *
//    *                *---|-------Range.first-------------*     *
//    *                *   |                               *     *
//    *                *************************************     *
//    *                                                          *
//    *                                                          *
//    ************************************************************
//
//
void MemoryPlot::ScreenValues()
{
    // big screens
    screenRange.first = 115;
    screenRange.second = 74;

    screenOffset.first = 11;
    screenOffset.second = 3;

    buffsize.first = screenRange.first + screenOffset.first + 5;
    buffsize.second = screenRange.second + screenOffset.second + 5;

    membuff = new char*[buffsize.second];
    for (int i = 0; i < buffsize.second; i++)
    {
        membuff[i] = new char[buffsize.first + 1];
        membuff[i][buffsize.first] = '\0';
    }
}

//
// process to run just prior to plotting.  MemoryPlot class won't need this
//
void MemoryPlot::PreProcess(void)
{
}

//
// process to run just after plotting.  MemoryPlot class won't need this either
//
void MemoryPlot::PostProcess(void)
{
}

//
// dump to stream
//
ostream& operator<< (ostream&os, MemoryPlot& m)
{
    for (int i = 0; i < m.buffsize.second; i++)
        os << m.membuff[i] << endl;

    return os;
}


//
// draw the basic lines around the plot, and set the viewport
//
void MemoryPlot::DrawAxes(void)
{
    // init
    clrscr();

    // start with the text
    if (title)
    {
        gotoxy(screenOffset.first + (screenRange.first - strlen(title))/2, screenOffset.second - 2);
        memputs(title);
    }

    if (xlabel)
    {
        gotoxy(screenOffset.first + (screenRange.first - strlen(xlabel))/2, screenOffset.second + screenRange.second + 2);
        memputs(xlabel);
    }

    if (ylabel)
    {
        char buff[2];
        buff[1] = '\0';

        for (unsigned int i = 0; i < strlen(ylabel); i++)
        {
            buff[0] = ylabel[i];
            gotoxy(screenOffset.first - 5, screenOffset.second + (screenRange.second - strlen(ylabel))/2 + i);
            memputs(buff);
        }
    }

    // do the range labels
    // each label will be in the form +1.23e+45
    char buffer[200];
    ostrstream label(buffer, 200);
    label.setf(ios::scientific|ios::showpoint|ios::showpos);
    label << setprecision(2);

    // x range labels
    label << minPair.first << ends;
    label.width(screenRange.first - strlen(buffer) + 1);
    label.fill(' ');
    label.setf(ios::right);
    label.seekp(-1, ios::cur);     // back up over the terminating null
    label << maxPair.first << ends;

    gotoxy(screenOffset.first, screenOffset.second + screenRange.second + 1);
    memputs(buffer);

    // y range labels
    label.seekp(0);
    label.setf(ios::left);
    label << maxPair.second << ends;
    gotoxy(screenOffset.first - strlen(buffer) - 1, screenOffset.second);
    memputs(buffer);

    label.seekp(0);
    label << minPair.second << ends;
    gotoxy(screenOffset.first - strlen(buffer) - 1, screenOffset.second + screenRange.second);
    memputs(buffer);

    // top line
    gotoxy(screenOffset.first, screenOffset.second);
    int x;
    for (x = 0; x <= screenRange.first; x++)
    {
        memputs("*");
    }

    // bottom line
    gotoxy(screenOffset.first, screenOffset.second + screenRange.second);
    for (x = 0; x <= screenRange.first; x++)
    {
        memputs("*");
    }

    // side lines
    for (int y = 1; y < screenRange.second; y++)
    {
        gotoxy(screenOffset.first, screenOffset.second + y);
        memputs("*");
        gotoxy(screenOffset.first + screenRange.first, screenOffset.second + y);
        memputs("*");
    }

    // do the 0 axes, if in range
    DoublePair zero;
    zero.first = 0.0;
    zero.second = 0.0;
    IntPair screenZero = Transform(zero);

    if ( (minPair.first < 0) && (maxPair.first > 0) )
    {
        for (int y = 1; y < screenRange.second; y++)
        {
            gotoxy(screenZero.first, screenOffset.second + y);
            memputs("|");
        }
    }

    if ( (minPair.second < 0) && (maxPair.second > 0) )
    {
        gotoxy(screenOffset.first + 1, screenZero.second);
        for (x = 1; x < screenRange.first; x++)
            memputs("-");
    }
}



//
// function to add a point
//
void MemoryPlot::AddPoint(double x, double y)
{
    MemoryGraphElement *ge = new MemoryGraphElement(DoublePair(x, y));
    AddElement(ge);
}



//
// MemoryPlot functions to manipulate the buffer
//
void MemoryPlot::clrscr(char ch)
{
    for (int i = 0; i < buffsize.second; i++)
    {
        for (int j = 0; j < buffsize.first; j++)
        {
            membuff[i][j] = ch;
        }
    }
}

void MemoryPlot::gotoxy(int x, int y)
{
    cursor.first = x;
    cursor.second = y;

    if (x >= buffsize.first )
    {
        cursor.first = buffsize.first - 1;
    }
    if (x < 0)
    {
        cursor.first = 0;
    }

    if (y >= buffsize.second)
    {
        cursor.second = buffsize.second - 1;
    }
    if (y < 0)
    {
        cursor.second = 0;
    }
}

void MemoryPlot::memputs(const char *s)
{
    // how much to copy; prevent going off edge
    int limit = buffsize.first - cursor.first;
    int len = strlen(s);

    if (len > limit)
        len = limit;

    // starting location
    char *p = &membuff[cursor.second][cursor.first];

    // copy
    memcpy(p, s, len);

    // advance cursor
    cursor.first += len;
    if (cursor.first >= buffsize.first)
        cursor.first = buffsize.first - 1;
}


//
// define the routines for the various GraphElement functions
//


// ctor
MemoryGraphElement::MemoryGraphElement(DoublePair p)
{
    pnt.first = p.first;
    pnt.second = p.second;
}



// plot
void MemoryGraphElement::Plot()
{
    // use RTTI to do a down-cast
    MemoryPlot *mp = dynamic_cast<MemoryPlot *>(owner);
    if (mp)
    {
        // let the owner transform the coords to local values
        IntPair coord = mp->Transform(pnt);
    
        char buff[2];
        buff[0] = owner->GetCurrentGraph() + '0';
        buff[1] = '\0';

        mp->gotoxy(coord.first, coord.second);
        mp->memputs(buff);
    }
}
