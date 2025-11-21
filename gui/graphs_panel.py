from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class GraphsPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        
        self.setLayout(self.layout)
        
        self.setStyleSheet("border: 1px solid #666;")

    def add_graph_widget(self, widget):
        self.layout.addWidget(widget)
