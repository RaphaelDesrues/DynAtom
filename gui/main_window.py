from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QSplitter, QMessageBox
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
        self.params_panel.stop_btn.clicked.connect(self._stop_md)

        # Check correct parameters for MD
        # self.params_panel.params_valid.connect(self._params_valid)
        # self.params_panel.params_invalid.connect(self._params_invalid)
        self.params_panel.check_btn.clicked.connect(self._check_params_wrapper)

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
        
        self.graph_manager = GraphManager()


    def _check_params_wrapper(self):
        values, errors = self.params_panel._check_params()
        if errors:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Parameter Error")
            msg.setText("Please correct the following errors:")
            msg.setInformativeText("\n".join(errors))
            msg.exec_()
            return None, errors
        
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Parameters checked")
            msg.setText("All parameters are correct")
            msg.exec_()
            return values, None

    def _start_md(self):
        
        values, errors = self._check_params_wrapper() 
        
        if errors:
            values = {
                "boxsize": 10,
                "temperature": 300,
                "timestep": 0.001,
                "nsteps": 200,
                "n_atoms": 10,
            }
            return # TEMP

        self.engine = Engine(values)

        # Add all plots to graphs panel
        for w in self.graph_manager.get_widgets():
            self.graphs_panel.add_graph_widget(w)

        self.atoms_panel.view.add_box(values["boxsize"])

        # Update Graphs and atoms positions

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(16)

    def _stop_md(self):
        if hasattr(self, "timer"):
            self.timer.stop()

    def update_all(self):
        self.engine.run_once()
        self.graph_manager.update_all(self.engine)
        self.atoms_panel.view.update_positions(self.engine)