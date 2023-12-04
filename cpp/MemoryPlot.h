
#ifndef __MEMPLOT_H
#define __MEMPLOT_H


#include "BasePlot.h"


//
// MemoryPlot class
//
// plot values on Memory screen using ascii characters
//

class MemoryPlot : public BasePlot
{
protected:

    // memory buffer
    IntPair buffsize;
    char **membuff;

    // cursor
    IntPair cursor;

    // provide definitions for pure virtuals of base
    virtual void ScreenValues();
    virtual void DrawAxes();
    virtual void PreProcess();
    virtual void PostProcess();

    // buffer manipulation functions
    void clrscr(char ch = ' ');
    void gotoxy(int x, int y);
    void memputs(const char *s);

public:

    // ctor, dtor
    MemoryPlot(int numGraphs = 1);
    virtual ~MemoryPlot();

    // add a point
    void AddPoint(double x, double y);

    // dump to stream
    friend ostream& operator<< (ostream& os, MemoryPlot& m);

    friend class MemoryGraphElement;
};


class MemoryGraphElement : public GraphElement
{
    DoublePair pnt;

public:

    MemoryGraphElement(DoublePair pnt);
    virtual ~MemoryGraphElement() {}

    // plot self
    virtual void Plot();

    // these functions define a rectangle which will bound the element
    virtual DoublePair GetMax() {return pnt;}
    virtual DoublePair GetMin() {return pnt;}
};


#endif //#ifndef __MEMPLOT_H
