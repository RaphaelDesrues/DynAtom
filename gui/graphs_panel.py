from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox,
    QGridLayout, QCheckBox
)
from assets.graph_manager import GraphManager


class GraphsPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.graph_manager = GraphManager()

        # For qss style
        self.setObjectName("GraphsPanel")
        self.layout = QVBoxLayout(self) # else: self.setLayout(self.layout)

        # ----- Graph picker -----
        self.graph_picker_box = QGroupBox()
        self.graph_picker_layout = QGridLayout()
        self._populate_picker()
        self.graph_picker_box.setLayout(self.graph_picker_layout)
        
        # ----- Graph display -----
        self.graph_display_box = QGroupBox()
        self.graph_display_layout = QGridLayout()

        self.graph_display_box.setLayout(self.graph_display_layout)

        # ----- Add boxes to main layout panel -----
        self.layout.addWidget(self.graph_picker_box)
        self.layout.addWidget(self.graph_display_box)
        self.layout.addStretch()

    def add_graph_widget(self, widget):
        for w in self.graph_manager.get_widgets():
            self.graphs_panel.add_graph_widget(w)
            self.graph_display_layout.addWidget(widget)

    def _populate_picker(self): # from MDRecorder
        for i, graph_view in enumerate(self.graph_manager.graphs.values()):
            label = graph_view.name
            widget = QCheckBox(label)
            row = i // 2
            col = i % 2

            self.graph_picker_layout.addWidget(widget, row, col)
            
    def _display_onclick(self):
        pass