from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit


class ParamsPanel(QWidget):
        
        def __init__(self):
            super().__init__()

            self.layout = QVBoxLayout()
            self.button_layout = QHBoxLayout()
            self.params_layout = QHBoxLayout()

            # Buttons

            self.start_btn = QPushButton("Start")
            self.button_layout.addWidget(self.start_btn)

            self.stop_btn = QPushButton("Stop")
            self.button_layout.addWidget(self.stop_btn)

            self.check_params = QPushButton("Check Parameters")
            self.button_layout.addWidget(self.check_params)


            # Params
            ## Number of atoms
            self.boxsize = QLineEdit()
            self.boxsize.setPlaceholderText("Enter the chosen BoxSize")
            self.params_layout.addWidget(self.boxsize)

            ## System's temperature
            self.temperature = QLineEdit()
            self.temperature.setPlaceholderText("Chose Temperature")
            self.params_layout.addWidget(self.temperature)



            self.layout.addLayout(self.button_layout)
            self.layout.addLayout(self.params_layout)

            self.setStyleSheet("border: 1px solid #666;")
            self.setLayout(self.layout)
