import logging
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QSplitter, QMessageBox
from gui.params_panel import ParamsPanel
from gui.graphs_panel import GraphsPanel
from gui.atoms_panel import AtomsPanel
from engine.md_engine import Engine
from assets.recorder import MDRecorder
from pyqtgraph.Qt import QtCore # type: ignore


class MainWindow(QMainWindow):
    """MainWindow class for the DynAtom application.
    
    This class represents the main window of the DynAtom application, which is a graphical user interface for molecular dynamics simulations. It initializes the GUI components, manages the simulation phases, and handles user interactions.
    
    Attributes:
        params_panel (ParamsPanel): Panel for parameter input and control buttons.
        atoms_panel (AtomsPanel): Panel for visualizing atoms.
        graphs_panel (GraphsPanel): Panel for displaying graphs related to the simulation.
        recorder (MDRecorder): Recorder for storing simulation data.
        step (int): Counter for the current step in the simulation.
        timer (QTimer): Timer for managing the execution of simulation phases.
        md_params (dict): Dictionary containing parameters for the molecular dynamics simulation.
        phases (list): List of phases to be executed during the simulation.
        phase_index (int): Index of the current phase being executed.
    
    Methods:
        __init__(): Initializes the main window, sets up the GUI, and connects buttons to their respective functions.
        _check_params_wrapper(): Validates the parameters entered by the user and displays a message box with the results.
        _start_md(): Starts the molecular dynamics simulation after validating parameters.
        set_fonction(fonction): Sets a function to be called at regular intervals using a timer.
        _stop_md(): Stops the molecular dynamics simulation and resets the recorder.
        update_all(): Updates the visualization of atoms and graphs.
        minimization(): Performs a minimization step in the simulation.
        equilibration(): Performs an equilibration step in the simulation.
        production(): Runs a production step in the simulation.
        run_md(): Initiates the molecular dynamics simulation phases based on user-selected options.
        start_phase(phase_name): Starts the specified phase of the simulation.
        next_phase(): Advances to the next phase of the simulation, if available.
    """
    def __init__(self):
        super().__init__()

        # Load style
        with open("gui/style.qss", "r") as f:
            self.setStyleSheet(f.read())

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

        main_splitter.setSizes([100, 800, 500])

        self.setCentralWidget(main_splitter)


        # ==========================
        #  Engine
        # ==========================
        self.recorder = MDRecorder()
        self.step = 0


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
            logging.warning("Errors in starting MD")
            return # TEMP

        if values:
            logging.info("MD starting normally")
            logging.info(f"MD parameters are: {values}")
            self.md_params = values

        self.engine = Engine(self.md_params, self.recorder)

        self.atoms_panel.view.add_box(values["boxsize"])

        self.run_md()

    def set_fonction(self, fonction):
        if not hasattr(self, "timer"):
            self.timer = QtCore.QTimer()

        try:
            self.timer.timeout.disconnect()
        except TypeError:
            pass

        self.timer.timeout.connect(fonction)

        if not self.timer.isActive():
            self.timer.start(16)

    def _stop_md(self):
        if hasattr(self, "timer"):
            self.timer.stop()
        # reset recorder = reset atomview et graphview
        self.recorder = MDRecorder()
    def update_all(self):
        self.atoms_panel.view.update_positions(self.engine)
        self.graphs_panel.graph_manager.update_all(self)

    def minimization(self):
        keys = ["mini_n_steps", "mini_dt", "mini_conv_crit"]
        n_steps, dt, conv_crit = [self.md_params.get(k) for k in keys]

        self.step += 1
        if (self.step % 1000) == 0:
            logging.info(f"Minimisation step {self.step}")

        converged  = self.engine.minimize_step(dt, conv_crit)
        self.update_all()

        if converged:
            logging.info(f"Minimisation converged in {self.step} steps")
            self.next_phase()
            return

        if self.step >= n_steps:
            logging.info("Minimisation has not converged")
            self.next_phase()
            return

    def equilibration(self):
        keys = ["eq_n_steps", "eq_dt", "temperature", "eq_tau"]
        n_steps, dt, T_target, tau = [self.md_params.get(k) for k in keys]

        self.step += 1
        if (self.step % 1000) == 0:
            logging.info(f"Equilibration step {self.step}")

        self.engine.equilibrate_step(self.step, dt, T_target, tau)
        self.update_all()

        if self.step >= n_steps:
            logging.info("Equilibration finished")
            self.next_phase()
            return

    def production(self):
        keys = ["prod_n_steps", "prod_dt"]
        n_steps, dt = [self.md_params.get(k) for k in keys]

        self.engine.run_once(dt)
        self.update_all()

        if self.step >= n_steps:
            logging.info("Production finished")
            self.next_phase
            return

    def run_md(self):

        # Build list of actions
        self.phases = []
        if self.md_params["enable_min"]:
            self.phases.append("min")
        if self.md_params["enable_eq"]:
            self.phases.append("eq")
        if self.md_params["enable_prod"]:
            self.phases.append("prod")

        if not self.phases:
            logging.warning("Nothing to run in run_md().")
            return

        self.phase_index = 0
        self.step = 0

        # Lancer la première phase
        self.start_phase(self.phases[self.phase_index])

    def start_phase(self, phase_name):
        # Initiate the timer
        if not hasattr(self, "timer"):
            self.timer = QtCore.QTimer()

        try:
            self.timer.timeout.disconnect()
        except TypeError:
            pass

        if phase_name == "min":
            logging.info("Starting minimization...")
            self.timer.timeout.connect(self.minimization)

        elif phase_name == "eq":
            logging.info("Starting equilibration...")
            self.timer.timeout.connect(self.equilibration)

        elif phase_name == "prod":
            logging.info("Starting production...")
            self.timer.timeout.connect(self.production)

        self.step = 0
        self.timer.start(16)

    def next_phase(self):

        self.phase_index += 1

        if self.phase_index >= len(self.phases):
            logging.info("All selected phases completed")
            self.timer.stop()
            return

        next_phase = self.phases[self.phase_index]
        self.start_phase(next_phase)
