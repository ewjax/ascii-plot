

#include <iostream>
#include "MemoryPlot.h"


int main()
{

    double x;
    MemoryPlot plot(5);

    plot.SetTitle("This is the Main Plotting Title");
    plot.SetXLabel("This is the X Axis");
    plot.SetYLabel("Longer Y Axis");

    for ( x = 0; x <= 2*M_PI + 0.05; x += (M_PI_4/4))
    {
        plot.SetCurrentGraph(0);
        double y = sin(x);
        plot.AddPoint(x, y);

        plot.SetCurrentGraph(1);
        y = cos(x);
        plot.AddPoint(x, y);

        plot.SetCurrentGraph(2);
        y = 2.0 * (1.0 - exp(-1.0 * x));
        plot.AddPoint(x, y);

        plot.SetCurrentGraph(3);
        y = (2.0 * (1.0 - exp(-1.0 * x))) * cos(x);
        plot.AddPoint(x, y);

        plot.SetCurrentGraph(4);
        y = -0.5 * x + 3.0;
        plot.AddPoint(0.5*x + 1.0, y);
    }


    plot.Draw();
    cout << plot;


    plot.Clear();

    for (x = -5; x < 10; x++)
    {
        plot.SetCurrentGraph(0);
        double y = -3*x + 4;
        plot.AddPoint(x, y);

        plot.SetCurrentGraph(1);
        y = x - 3.5;
        plot.AddPoint(x, y);
    }

    plot.Draw();
    cout << plot;


    plot.Clear();

    for (x = -10; x <= 20; x++)
    {
        double y = x*x - 100;
        plot.AddPoint(x, y);
    }

    plot.Draw();
    cout << plot;



    plot.Clear();

    plot.AddPoint(0, 0);
    plot.SetCurrentGraph(1);

    for ( x = 0; x <= 2*M_PI + 0.05; x += (M_PI_4/4))
    {
        double y = sin(x);
        plot.AddPoint(x, y);

    }

    plot.Draw();
    cout << plot;

    return 0;
}
