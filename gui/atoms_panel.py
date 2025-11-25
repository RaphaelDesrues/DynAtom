from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from gui.atom_view import AtomsView


class AtomsPanel(QWidget):

    def __init__(self):
        super().__init__()


        self.layout = QVBoxLayout(self)
        self.atoms_box = QGroupBox("Atoms View Dynamics")

        self.view = AtomsView()
        self.atoms_box.setLayout(self.view.layout)

        self.layout.addSpacing(20)
        self.layout.addWidget(self.atoms_box)




