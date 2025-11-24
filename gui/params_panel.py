from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLineEdit, QLabel, QGroupBox, QFormLayout
)
from PyQt5.QtCore import pyqtSignal


class ParamsPanel(QWidget):

        # Signals
        ## PyQt Signals should be defined as Class attributes and not Instance
        # params_valid = pyqtSignal(dict)
        # params_invalid = pyqtSignal(list)

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

            # ----- Parameters -----
            # Define parameters
            self.params = {
                "boxsize": ("Box size", int),
                "temperature": ("Temperature", float),
                "timestep": ("Time step", float),
                "nsteps": ("Number of Steps", int),
                "n_atoms": ("Number of Atoms", int),
            }

            self.params_box = QGroupBox("Parameters")
            self.params_layout = QFormLayout()
            self.params_layout.setContentsMargins(5, 20, 5, 5)
            # Params : iteratively add params          
            self._populate_params_layout()
            self.params_box.setLayout(self.params_layout)

            # ----- Add Boxes to panel -----
            self.layout.addSpacing(20)
            self.layout.addWidget(self.button_box)
            self.layout.addSpacing(20)
            self.layout.addWidget(self.params_box)
            # Flexible space at the end to up the boxes
            self.layout.addStretch()
            
        def _populate_params_layout(self):
            # Heights and Width for the widget
            h, w = 20, 120
            for param, (label, expected_type) in self.params.items():
                label_widget = QLabel(label)
                label_widget.setMinimumWidth(w)
                label_widget.setMinimumHeight(h)
                
                widget = QLineEdit()
                widget.setMinimumHeight(h)
                
                # Store the widget inside the class
                setattr(self, param, widget)
                self.params_layout.addRow(label_widget, widget)
                
        def _check_params(self):
            errors = []
            values = {}

            for param, (label, expected_type) in self.params.items():
                # Retrieve the widget by its attr
                widget = getattr(self, param)
                text = widget.text()

                try:
                    value = expected_type(text)
                except:
                    errors.append(f"Missing value or {label} \
                                  value must be of type: {expected_type.__name__}")
                    value = None

                values[param] = value

            if errors:
                return None, errors
            else:
                return values, None