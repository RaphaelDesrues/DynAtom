from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QSplitter, QLabel, QWidget, QVBoxLayout
from gui.params_panel import ParamsPanel
from gui.graphs_panel import GraphsPanel
from engine.md_engine import Engine
from assets.graph_manager import GraphManager
from pyqtgraph.Qt import QtCore # type: ignore


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DynAtom")
        self.setFixedSize(QSize(800, 600))

        # ==========================
        #  UI
        # ==========================


        main_splitter = QSplitter()

        main_splitter.setOrientation(Qt.Horizontal)

        # ------------------
        #  Parameters panel
        # ------------------

        params_panel = ParamsPanel()

        # ------------------
        #  Atom dynamic panel
        # ------------------

        atoms_panel = QWidget()
        atoms_layout = QVBoxLayout()
        atoms_panel.setLayout(atoms_layout)

        atoms_layout.addWidget(QLabel("Atoms Dynamic"))

        atoms_panel.setStyleSheet("border: 1px solid #666;")


        # ------------------
        #  Graphs panel
        # ------------------

        graphs_panel = GraphsPanel()

        # ------------------
        #  Main Splitter
        # ------------------

        main_splitter.addWidget(params_panel)
        main_splitter.addWidget(atoms_panel)
        main_splitter.addWidget(graphs_panel)

        main_splitter.setSizes([200, 400, 200])

        self.setCentralWidget(main_splitter)



        # ==========================
        #  Engine
        # ==========================

        self.engine = Engine()
        self.graph_manager = GraphManager()

        # Add all plots to graphs panel
        for w in self.graph_manager.get_widgets():
            graphs_panel.add_graph_widget(w)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(16)

    def update_all(self):
        self.engine.run_once()
        self.graph_manager.update_all(self.engine)