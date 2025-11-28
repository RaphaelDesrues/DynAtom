from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLineEdit, QLabel, QGroupBox, QFormLayout,
    QCheckBox
)
from PyQt5.QtCore import pyqtSignal


class ParamsPanel(QWidget):
    """ParamsPanel is a QWidget that provides a user interface for configuring simulation parameters.
    
    This panel includes controls for starting, stopping, and checking parameters, as well as sections for general, minimization, equilibration, and production parameters. Each section contains input fields for the user to specify values, which are validated upon checking.
    
    Attributes:
        layout (QVBoxLayout): The main layout of the ParamsPanel.
        button_box (QGroupBox): A group box containing control buttons.
        params_general (dict): A dictionary of general parameters with their labels, default values, and expected types.
        params_min (dict): A dictionary of minimization parameters with their labels, default values, and expected types.
        params_eq (dict): A dictionary of equilibration parameters with their labels, default values, and expected types.
        params_prod (dict): A dictionary of production parameters with their labels, default values, and expected types.
    
    Methods:
        _add_parameters_box(param_name, params):
            Creates and adds a parameter group box to the layout.
    
        _populate_params_layout(layout, params):
            Populates a layout with parameter input fields based on the provided parameters.
    
        _check_params():
            Validates the input values and returns them along with any error messages.
    
        _update_visibility():
            Updates the visibility of the parameter sections based on the state of the corresponding checkboxes.
    """
    def __init__(self):
        super().__init__()

        # For qss style
        self.setObjectName("ParamsPanel")
        # Set the panel layout
        self.layout = QVBoxLayout(self)

        # ----- Control Buttons -----
        self.button_box = QGroupBox("Controls") # QGroupBox can't hold widget -> layout
        self.button_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.check_btn = QPushButton("Check Parameters")

        # Add buttons to layout
        self.button_layout.addWidget(self.start_btn)
        self.button_layout.addWidget(self.stop_btn)
        self.button_layout.addWidget(self.check_btn)

        # Add the layout inside the box
        self.button_box.setLayout(self.button_layout)
        # self.button_box.setContentsMargins(5, 40, 5, 5)
        # Add Boxes to panel
        self.layout.addSpacing(20)
        self.layout.addWidget(self.button_box)

        # ----- Parameters -----
        # Define parameters
        self.params_general = {
            "boxsize": ("Box size", 10, int),
            "temperature": ("Temperature", 300, int),
            "n_atoms": ("Number of Atoms", 50, int),

            "enable_min": ("Compute Minimisation", None, bool),
            "enable_eq": ("Compute Equilibration", None, bool),
            "enable_prod": ("Compute Production", None, bool),
        }

        self.params_min = {
            "mini_n_steps": ("Minimization steps", 1000, int),
            "mini_dt": ("Step size", 1e-3, float),
            "mini_conv_crit": ("Convergence", 1e-3, float),
        }

        self.params_eq = {
            "eq_n_steps": ("Equilibration steps", 1000, int),
            "eq_dt": ("Integration step", 1e-4, float),
            "temperature": ("Target temperature", 300, float),
            "eq_tau": ("Tau", 1e-3, float),
        }

        self.params_prod = {
            "prod_n_steps": ("Production steps", 1000, int),
            "prod_dt": ("Integration step", 1e-4, float),
        }

        # Iteratively add parameters
        self._add_parameters_box("General Parameters", self.params_general)
        self._add_parameters_box("Minimisation Parameters", self.params_min)
        self._add_parameters_box("Equilibration Parameters", self.params_eq)
        self._add_parameters_box("Production Parameters", self.params_prod)

        # Add visibility logic for general parameters checkboxes
        self.enable_min.stateChanged.connect(self._update_visibility)
        self.enable_eq.stateChanged.connect(self._update_visibility)
        self.enable_prod.stateChanged.connect(self._update_visibility)

        # Flexible space at the end to up the boxes
        self.layout.addStretch()

    def _add_parameters_box(self, param_name, params):
        box = QGroupBox(param_name)
        box.setObjectName(param_name.replace(" ", "_"))
        layout = QFormLayout()
        layout.setContentsMargins(5, 20, 5, 5)
        # Params : iteratively add params          
        layout = self._populate_params_layout(layout, params)
        box.setLayout(layout)
        
        self.layout.addSpacing(20)
        self.layout.addWidget(box)

    def _populate_params_layout(self, layout, params):
        # Heights and Width for the widget
        h, w = 20, 120
        for param, (label, text, expected_type) in params.items():
            label_widget = QLabel(label)
            label_widget.setMinimumWidth(w)
            label_widget.setMinimumHeight(h)
            
            if expected_type is bool:
                widget = QCheckBox()
                widget.setChecked(True)
            else:
                widget = QLineEdit()
                widget.setText(str(text))
                widget.setMinimumHeight(h)
            
            # Store the widget inside the class
            setattr(self, param, widget)
            layout.addRow(label_widget, widget)
        
        return layout
            
    def _check_params(self):
        errors = []
        values = {}

        # Retrieve only the active params and not the control box
        sections = [
            (self.params_general, True),
            (self.params_min, self.enable_min.isChecked()),
            (self.params_eq, self.enable_eq.isChecked()),
            (self.params_prod, self.enable_prod.isChecked()),
        ]
        for params, active in sections:
            if not active:
                continue
            for param, (label, _, expected_type) in params.items():
                # Retrieve the widget by its attr
                widget = getattr(self, param)
                text = widget.text()

                if expected_type is bool:
                    values[param] = widget.isChecked()
                    continue

                try:
                    value = expected_type(text)
                except:
                    errors.append(f"Missing value or {label} \n \
                                value must be of type: {expected_type.__name__}")
                    value = None

                values[param] = value

        if errors:
            return None, errors
        else:
            return values, None

    def _update_visibility(self):
        box_min = self.findChild(QGroupBox, "Minimisation_Parameters")
        box_eq = self.findChild(QGroupBox, "Equilibration_Parameters")
        box_prod = self.findChild(QGroupBox, "Production_Parameters")

        # Show visible if checked
        box_min.setVisible(self.enable_min.isChecked())
        box_eq.setVisible(self.enable_eq.isChecked())
        box_prod.setVisible(self.enable_prod.isChecked())