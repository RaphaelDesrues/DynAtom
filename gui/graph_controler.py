import pyqtgraph as pg # type: ignore


class GraphControler():

    def __init__(self, name):
        
        super().__init__()

        self.name = name

        # Create plot
        self.plot = pg.PlotWidget()
        self.plot.setTitle(name)

        # Creat curve
        self.curve = self.plot.plot(pen='y')

    def update(self, engine):
        data = engine.recorder.potential
        self.curve.setData(data)

