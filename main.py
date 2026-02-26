import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QFont, QFontDatabase
from landing import StartPage
from simulator import BallSimulator
from options import options

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ball Simulator")
        self.setGeometry(100, 100, 800, 550)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Initialize the pages
        self.start_page = StartPage(self)
        self.stacked_widget.addWidget(self.start_page)

        self.simulator = BallSimulator(self)
        self.stacked_widget.addWidget(self.simulator)

        self.options_page = options(self)
        self.stacked_widget.addWidget(self.options_page)

    def show_simulator(self):
        self.stacked_widget.setCurrentWidget(self.simulator)

    def show_start_page(self):
        self.stacked_widget.setCurrentWidget(self.start_page)

    def options(self):
        self.stacked_widget.setCurrentWidget(self.options_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())