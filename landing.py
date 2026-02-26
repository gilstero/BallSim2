from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame, QSizePolicy
from PyQt5.QtGui import QFont, QColor, QPalette, QFontDatabase
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import os

class StartPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.main_window = parent

        self.is_dark_mode = False

        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto', 'static', 'Roboto-Regular.ttf')
        QFontDatabase.addApplicationFont(font_path)
        font = QFont("Roboto", 18, QFont.Bold)
        
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, QColor(228, 240, 229))
        self.setPalette(p)
        self.setContentsMargins(50, 50, 50, 50)
       
        title_label = QLabel("Ball Simulator V.2", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(font)

        title_container = QFrame(self)
        title_container.setStyleSheet("""
            QFrame {
                background-color: rgb(202, 237, 207); 
                color: black; 
                padding: 15px; 
                border-radius: 10px; 
                border: none;
                font-size: 18px; 
            }
        """)
        title_layout = QVBoxLayout(title_container)
        title_layout.addWidget(title_label)

        title_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        layout.addWidget(title_container)
        

        # Below is the implementation of the toggle dark theme button for the simulator
        self.theme_button = QPushButton("DARK MODE", self)
        self.theme_button.setFont(font)
        self.theme_button.setStyleSheet(
            "background-color: rgb(202, 237, 207); color: black; padding: 15px; border-radius: 10px; border: none;"
            "font-size: 18px; margin-top: 30px;"
        )
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)

        #options button
        self.options = QPushButton("OPTIONS", self)
        self.options.setFont(font)
        self.options.setStyleSheet("""
            QPushButton {
            background-color: rgb(202, 237, 207); 
            color: black; 
            padding: 15px; 
            border-radius: 10px; 
            border: none;
            font-size: 18px; 
            margin-top: 30px;
        }
        QPushButton:hover {
            background-color: rgb(154, 227, 165);
        }
        """)
        self.options.clicked.connect(parent.options)
        layout.addWidget(self.options)

        # Style for the start button
        self.start_button = QPushButton("START", self)
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("""
            QPushButton {
            background-color: rgb(202, 237, 207); 
            color: black; 
            padding: 15px; 
            border-radius: 10px; 
            border: none;
            font-size: 18px; 
            margin-top: 30px;
        }
        QPushButton:hover {
            background-color: rgb(154, 227, 165);
        }
        """)
        self.start_button.clicked.connect(parent.show_simulator)
        
        layout.addWidget(self.start_button)
        layout.addStretch()
        
        self.setLayout(layout)

    def toggle_theme(self):
        if self.is_dark_mode:
            self.set_light_theme()
            self.main_window.options_page.set_light_theme()
            self.main_window.simulator.set_light_theme()
        else:
            self.set_dark_theme()
            self.main_window.options_page.set_dark_theme()
            self.main_window.simulator.set_dark_theme()

        self.is_dark_mode = not self.is_dark_mode

    def set_light_theme(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, QColor(228, 240, 229))
        self.setPalette(p)

        self.theme_button.setStyleSheet(
            "background-color: rgb(202, 237, 207); color: black; padding: 15px; border-radius: 10px; border: none;"
            "font-size: 18px; margin-top: 30px;"
        )

    def set_dark_theme(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, QColor(30, 30, 30))
        self.setPalette(p)

        self.theme_button.setStyleSheet(
            "background-color: rgb(50, 50, 50); color: white; padding: 15px; border-radius: 10px; border: none;"
            "font-size: 18px; margin-top: 30px;"
        )