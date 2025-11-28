from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from gui.atom_view import AtomsView


class AtomsPanel(QWidget):
    """AtomsPanel is a QWidget that provides a user interface for viewing and interacting with atomic dynamics.
    
    This class initializes a vertical layout containing a group box labeled "Atoms View Dynamics" 
    and an instance of AtomsView. The layout is designed to organize the visual components related 
    to atomic dynamics.
    
    Attributes:
        layout (QVBoxLayout): The vertical layout for the widget.
        atoms_box (QGroupBox): A group box that contains the AtomsView.
        view (AtomsView): An instance of AtomsView that displays atomic dynamics.
    
    Methods:
        __init__(): Initializes the AtomsPanel and sets up the layout and components.
    """
    def __init__(self):
        super().__init__()


        self.layout = QVBoxLayout(self)
        self.atoms_box = QGroupBox("Atoms View Dynamics")

        self.view = AtomsView()
        self.atoms_box.setLayout(self.view.layout)

        self.layout.addSpacing(20)
        self.layout.addWidget(self.atoms_box)




