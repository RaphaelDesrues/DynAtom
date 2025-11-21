from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit


class ParamsPanel(QWidget):
        
        def __init__(self):
            super().__init__()

            layout = QVBoxLayout()
            button_layout = QHBoxLayout()
            params_layout = QHBoxLayout()

            # Buttons

            start_btn = QPushButton("Start")
            button_layout.addWidget(start_btn)

            stop_btn = QPushButton("Stop")
            button_layout.addWidget(stop_btn)


            # Params

            nb_atoms = QLineEdit()
            nb_atoms.setPlaceholderText("Enter Temperature")
            params_layout.addWidget(nb_atoms)


            layout.addLayout(button_layout)
            layout.addLayout(params_layout)

            self.setStyleSheet("border: 1px solid #666;")
            self.setLayout(layout)
