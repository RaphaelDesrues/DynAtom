import numpy as np # type: ignore
from pyqtgraph import PlotWidget, ScatterPlotItem, PlotDataItem, mkPen # type: ignore
from PyQt5.QtWidgets import QVBoxLayout, QWidget


class AtomsView(QWidget):
    """AtomsView is a QWidget that provides a visual representation of atomic positions using a scatter plot.
    
    Attributes:
        layout (QVBoxLayout): The layout manager for the widget.
        scatter (ScatterPlotItem): The scatter plot item used to display atomic positions.
        plot (PlotWidget): The plot widget that contains the scatter plot and additional items.
    
    Methods:
        __init__():
            Initializes the AtomsView with a given boxsize, setting up the layout, scatter plot, and plot widget.
        
        update_positions():
            Updates the positions of the atoms in the scatter plot based on the data from the engine.
            that provides the box size and atomic positions for visualization.
    """
    def __init__(self):
        super().__init__()

        self.boxsize = 10
        self.box_item = None
        self.layout = QVBoxLayout()

        self.scatter = ScatterPlotItem()
        self.scatter.setSize(size=20)
        self.scatter.setSymbol(symbol="o")
        self.scatter.setBrush("w")

        self.plot = PlotWidget()

        # Full box always visible
        self.plot.setXRange(min=0, max=self.boxsize)
        self.plot.setYRange(min=0, max=self.boxsize)

        self.plot.addItem(self.scatter)

        self.layout.addWidget(self.plot)

        self.setLayout(self.layout)

    def update_positions(self, engine):
        positions = np.array(engine.recorder.positions)
        self.scatter.setData(pos=positions)
        # print("positions: ", positions)

    def add_box(self, boxsize):
        box = self.box_item
        if box is not None:
            self.plot.removeItem(box)

        # Draw a box border
        self.boxsize = boxsize
        
        # Redefine ViewRange with actual bowsize
        self.plot.setXRange(0, boxsize)
        self.plot.setYRange(0, boxsize)

        # Display a white box around the atoms
        box = PlotDataItem(
            [0, boxsize, boxsize, 0, 0],
            [0, 0, boxsize, boxsize, 0],
            pen=mkPen('w', width=2)
        )
        self.plot.addItem(box)
        self.box_item = box


