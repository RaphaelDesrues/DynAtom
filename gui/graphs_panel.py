from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox,
    QGridLayout, QCheckBox
)
from PyQt5.QtCore import QSize
from assets.graph_manager import GraphManager


class GraphsPanel(QWidget):
    """GraphsPanel is a QWidget that provides an interface for selecting and displaying graphs.
    
    This panel allows users to choose from a set of graphs and view them in a grid layout. It manages the visibility of the graphs based on user selection.
    
    Attributes:
        graph_manager (GraphManager): An instance of GraphManager that holds the available graphs.
        layout (QVBoxLayout): The main layout for the panel.
        graph_picker_box (QGroupBox): A group box containing checkboxes for selecting graphs.
        graph_picker_layout (QGridLayout): The layout for the graph picker checkboxes.
        visible_graphs (list): A list of currently visible graphs.
        graph_display_box (QGroupBox): A group box for displaying the selected graphs.
        graph_display_layout (QGridLayout): The layout for displaying the visible graphs.
    
    Methods:
        _populate_picker(): Populates the graph picker with checkboxes for each available graph.
        _display_graph_onclick(state, graph_name): Updates the visibility of the graph based on the checkbox state.
        _rebuild_grid(): Rebuilds the grid layout to display the currently visible graphs.
    """
    def __init__(self):
        super().__init__()
        self.graph_manager = GraphManager()

        # For qss style
        self.setObjectName("GraphsPanel")
        self.layout = QVBoxLayout(self) # else: self.setLayout(self.layout)

        # ----- Graph picker -----
        self.graph_picker_box = QGroupBox("Select Graphs")
        self.graph_picker_layout = QGridLayout()
        self._populate_picker()
        
        self.graph_picker_box.setLayout(self.graph_picker_layout)
        
        # ----- Graph display -----
        self.visible_graphs = []
        self.graph_display_box = QGroupBox("Graphs")
        self.graph_display_layout = QGridLayout()

        self.graph_display_box.setLayout(self.graph_display_layout)

        # ----- Add boxes to main layout panel -----
        self.layout.addSpacing(20)
        self.layout.addWidget(self.graph_picker_box)
        self.layout.addWidget(self.graph_display_box)
        self.layout.addStretch()

    def _populate_picker(self): # from MDRecorder
        for i, (graph_name, graph_view) in enumerate(self.graph_manager.graphs.items()):
            label = graph_view.name
            widget = QCheckBox(label)
            row = i // 2
            col = i % 2
            self.graph_picker_layout.addWidget(widget, row, col)

            # Store the QCheckBox inside the class
            setattr(self, graph_name, widget)

            # Connect each CheckBox to its graph display
            widget.stateChanged.connect(
                lambda state, graph_name=graph_name: self._display_graph_onclick(state, graph_name)
            )

    def _display_graph_onclick(self, state, graph_name):
        graph = self.graph_manager.graphs[graph_name].plot
        graph.setMinimumSize(300, 200)

        if state == 2:
            if graph not in self.visible_graphs:
                self.visible_graphs.append(graph)
                graph.setVisible(True)
        else:
            if graph in self.visible_graphs:
                self.visible_graphs.remove(graph)
                # graph.setVisible(False)

        self._rebuild_grid()

    def _rebuild_grid(self):
        # Remove all widgets from layout (safe)
        while self.graph_display_layout.count():
            item = self.graph_display_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Re-add visible graphs only
        for idx, graph in enumerate(self.visible_graphs):
            row = idx // 2
            col = idx % 2
            self.graph_display_layout.addWidget(graph, row, col)



