from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSignal


class ParamsPanel(QWidget):

        # Signals
        ## PyQt Signals should be defined as Class attributes and not Instance
        # params_valid = pyqtSignal(dict)
        # params_invalid = pyqtSignal(list)

        def __init__(self):
            super().__init__()

            self.layout = QVBoxLayout()
            self.button_layout = QHBoxLayout()
            self.params_layout = QVBoxLayout()


            # Buttons
            self.start_btn = QPushButton("Start")
            self.button_layout.addWidget(self.start_btn)

            self.stop_btn = QPushButton("Stop")
            self.button_layout.addWidget(self.stop_btn)

            self.check_btn = QPushButton("Check Parameters")
            self.button_layout.addWidget(self.check_btn)


            # Params : iteratively add params
            self.params = {
                "boxsize": ("Box size", int),
                "temperature": ("Temperature", float),
                "timestep": ("Time step", float),
                "nsteps": ("Number of Steps", int),
                "n_atoms": ("Number of Atoms", int),
            }
            self._populate_panel()

            self.layout.addLayout(self.button_layout)
            self.layout.addLayout(self.params_layout)

            self.setStyleSheet("border: 1px solid #666;")
            self.setLayout(self.layout)

        def _populate_panel(self):

            for param, (label, expected_type) in self.params.items():
                row = QHBoxLayout()
                row.addWidget(QLabel(label))
                widget = QLineEdit()
                # Store the widget inside the class
                setattr(self, param, widget)
                row.addWidget(widget)
                
                self.params_layout.addLayout(row)

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