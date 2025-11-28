import pyqtgraph as pg # type: ignore


class GraphView():
    """GraphView class for visualizing data in a graphical plot.
    
    This class initializes a plot with specified titles for the x and y axes, and provides a method to update the plot with new data.
    
    Attributes:
        name (str): The title of the graph.
        plot (pg.PlotWidget): The plot widget used for rendering the graph.
        curve: The curve object representing the data series in the plot.
    
    Args:
        name (str): The name of the graph.
        x_axis (str, optional): The label for the x-axis. Defaults to None.
        y_axis (str, optional): The label for the y-axis. Defaults to None.
    
    Methods:
        update(engine, key):
            Updates the plot with new data from the specified engine and key.
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
        axis_style = {"color": "white", "font-size": "16px"}

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

