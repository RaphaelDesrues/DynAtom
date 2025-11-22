from csv import Error
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QSplitter
from gui.params_panel import ParamsPanel
from gui.graphs_panel import GraphsPanel
from gui.atoms_panel import AtomsPanel
from engine.md_engine import Engine
from assets.graph_manager import GraphManager
from pyqtgraph.Qt import QtCore # type: ignore


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DynAtom")
        self.setFixedSize(QSize(2400, 1800))    

        # ==========================
        #  UI
        # ==========================

        main_splitter = QSplitter()

        main_splitter.setOrientation(Qt.Horizontal)

        # ------------------
        #  Parameters panel
        # ------------------

        self.params_panel = ParamsPanel()

        ## Handle MD
        self.params_panel.start_btn.clicked.connect(self._start_md)
        # self.params_panel.stop_btn.clicked.connect(self._stop_md)

        # Check correct parameters for MD
        self.params_panel.check_params.clicked.connect(lambda: self._check_params)

        # ------------------
        #  Atom dynamic panel
        # ------------------

        self.atoms_panel = AtomsPanel()

        # ------------------
        #  Graphs panel
        # ------------------

        self.graphs_panel = GraphsPanel()

        # ------------------
        #  Main Splitter
        # ------------------

        main_splitter.addWidget(self.params_panel)
        main_splitter.addWidget(self.atoms_panel)
        main_splitter.addWidget(self.graphs_panel)

        main_splitter.setSizes([200, 400, 200])

        self.setCentralWidget(main_splitter)


        # ==========================
        #  Engine
        # ==========================
        
        self.engine = Engine(
            temperature=temperature,
            boxsize=boxsize,
        )

        self.graph_manager = GraphManager()

    
    def _check_params(self):
        
        errors = []
        
        boxsize = self.params_panel.boxsize.text()
        try:
            boxsize = int(boxsize)
        except ValueError:
            errors.append("Boxsize is missing or must be an integer")

        temperature = self.params_panel.temperature.text()
        try:
            temperature = float(temperature)
        except Error:
            errors.append("Temperature value missing or must be a float")

        if errors:
            print("ERRORS; ", errors)

        return boxsize, temperature

    def _start_md(self):

        # Add all plots to graphs panel
        for w in self.graph_manager.get_widgets():
            self.graphs_panel.add_graph_widget(w)

        # Update Graphs and atoms positions

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(16)

    def update_all(self):
        self.engine.run_once()
        self.graph_manager.update_all(self.engine)
        self.atoms_panel.view.update_positions(self.engine)