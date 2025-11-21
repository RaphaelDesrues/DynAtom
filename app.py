from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    # Instance of Qt application (handle keyboard, mouse, rendering, events...)
    # Qt app cannot exist without it
    app = QApplication([])

    # Create the window
    window = MainWindow()

    # Display the window (Qt widgets invisible by default)
    window.show()

    # Start the Qt event loop
    app.exec_()

    # The application won't reach here until you exit and the event loop has stopped.

if __name__ == "__main__":
    main()