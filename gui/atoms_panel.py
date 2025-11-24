from PyQt5.QtWidgets import QWidget, QVBoxLayout
from gui.atom_view import AtomsView


class AtomsPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.view = AtomsView()
        layout.addWidget(self.view)

        self.setLayout(layout)


