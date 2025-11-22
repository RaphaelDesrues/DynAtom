import pyqtgraph as pg # type: ignore


class GraphView():
    """GraphView is a class that manages a graphical representation of data using a plot widget.
    
    Attributes:
        name (str): The name of the graph, which is also used as the title of the plot.
        plot (pg.PlotWidget): The plot widget used to display the graph.
        curve (pg.PlotDataItem): The curve representing the data in the plot.
    
    Methods:
        __init__(name):
            Initializes the GraphView with a given name and sets up the plot.
        
        update(engine):
            Updates the plot with new data from the provided engine's recorder.
    """
    def __init__(self, name, x_axis=None, y_axis=None):
        
        self.name = name

        # Create plot
        self.plot = pg.PlotWidget()
        self.plot.setTitle(name)

        # Creat curve
        self.curve = self.plot.plot(pen='y')

        # Axis labels
        ## Axis style
        axis_style = {"color": "black", "font-size": "16px"}

        if x_axis:
            self.plot.setLabel("bottom", x_axis, **axis_style)
        
        if y_axis:
            self.plot.setLabel("left", y_axis, **axis_style)

        # Background grid
        self.plot.showGrid(x=True, y=True)


    def update(self, engine, key):
        
        data = getattr(engine.recorder, key, None)

        if data is None:
            return

        self.curve.setData(data)

