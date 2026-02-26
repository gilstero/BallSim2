from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QSizePolicy
from PyQt5.QtGui import QFont, QColor, QPalette, QFontDatabase, QPixmap
from PyQt5.QtCore import Qt, QTimer
import os

class options(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_window = parent

        self.setWindowTitle("Options")

        layout = QVBoxLayout()

        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto', 'static', 'Roboto-Regular.ttf')
        QFontDatabase.addApplicationFont(font_path)
        font = QFont("Roboto", 18, QFont.Bold)
        
        # Ball Size Slider
        self.ball_size_label = QLabel("Ball Size: 50", self)
        self.ball_size_label.setFont(font)
        self.ball_size_label.setStyleSheet("""
            background-color: rgb(202, 237, 207);                      
            padding: 5px;
            border-radius: 5px;
        """)
        self.ball_size_label.setFixedSize(self.ball_size_label.sizeHint())
        self.ball_size_slider = QSlider(Qt.Horizontal)
        self.ball_size_slider.setMinimum(10)
        self.ball_size_slider.setMaximum(99)
        self.ball_size_slider.setValue(50)
        self.ball_size_slider.valueChanged.connect(self.update_ball_size_label)
        self.ball_size_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #d3d3d3;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: rgb(202, 237, 207); 
                border: 2px solid rgb(202, 237, 207);
                width: 20px;
                height: 20px;
                margin: -5px 0; 
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: rgb(154, 227, 165);
                border: 2px solid rgb(154, 227, 165);
            }
        """)

        # Gravity Slider
        self.gravity_label = QLabel("Gravity: 1.0", self)
        self.gravity_label.setFont(font)
        self.gravity_label.setStyleSheet("""
            background-color: rgb(202, 237, 207);                      
            padding: 5px;
            border-radius: 5px;
        """)
        self.gravity_label.setFixedSize(self.gravity_label.sizeHint())
        self.gravity_slider = QSlider(Qt.Horizontal)
        self.gravity_slider.setMinimum(1)
        self.gravity_slider.setMaximum(20)
        self.gravity_slider.setValue(10)
        self.gravity_slider.valueChanged.connect(self.update_gravity_label)
        self.gravity_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #d3d3d3;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: rgb(202, 237, 207); 
                border: 2px solid rgb(202, 237, 207);
                width: 20px;
                height: 20px;
                margin: -5px 0; 
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: rgb(154, 227, 165);
                border: 2px solid rgb(154, 227, 165);
            }
        """)

        # Speed Slider
        self.speed_label = QLabel("Speed: 5", self)
        self.speed_label.setFont(font)
        self.speed_label.setStyleSheet("""
            background-color: rgb(202, 237, 207);                      
            padding: 5px;
            border-radius: 5px;
        """)
        self.speed_label.setFixedSize(self.speed_label.sizeHint())
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(5)
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #d3d3d3;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: rgb(202, 237, 207); 
                border: 2px solid rgb(202, 237, 207);
                width: 20px;
                height: 20px;
                margin: -5px 0; 
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: rgb(154, 227, 165);
                border: 2px solid rgb(154, 227, 165);
            }
        """)

        # Apply button
        self.apply_button = QPushButton("Apply Changes", self)
        self.apply_button.setFont(font)
        self.apply_button.setStyleSheet(
            "background-color: rgb(202, 237, 207); color: black; padding: 15px; border-radius: 10px; border: none;"
            "font-size: 18px;"
        )
        self.apply_button.clicked.connect(self.apply_changes)

        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setFont(font)
        self.back_button.setStyleSheet(
            "background-color: rgb(202, 237, 207); color: black; padding: 15px; border-radius: 10px; border: none;"
            "font-size: 18px;"
        )
        self.back_button.clicked.connect(self.apply_back_button)

        
        sliders_layout = QVBoxLayout()
        sliders_layout.addWidget(self.ball_size_label)
        sliders_layout.addWidget(self.ball_size_slider)
        sliders_layout.addSpacing(100)
        sliders_layout.addWidget(self.gravity_label)
        sliders_layout.addWidget(self.gravity_slider)
        sliders_layout.addSpacing(100)
        sliders_layout.addWidget(self.speed_label)
        sliders_layout.addWidget(self.speed_slider)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.apply_button)
        buttons_layout.addWidget(self.back_button)

        layout.addLayout(sliders_layout)
        layout.addStretch()
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def update_ball_size_label(self, value):
        self.ball_size_label.setText(f"Ball Size: {value}")

    def update_gravity_label(self, value):
        self.gravity_label.setText(f"Gravity: {value / 10:.1f}")

    def update_speed_label(self, value):
        self.speed_label.setText(f"Speed: {value}")

    def apply_back_button(self):
        self.back_button.clicked.connect(self.main_window.show_start_page)

    def apply_changes(self):
        self.apply_button.setStyleSheet(
        "background-color: rgb(154, 227, 165); color: black; padding: 15px; border-radius: 10px; border: none;"
        "font-size: 18px;"
        )

        # Restore original color after a short delay
        QTimer.singleShot(200, lambda: self.apply_button.setStyleSheet(
            "background-color: rgb(202, 237, 207); color: black; padding: 15px; border-radius: 10px; border: none;"
            "font-size: 18px;"
        ))

        ball_size = self.ball_size_slider.value()
        gravity = self.gravity_slider.value() / 10
        speed = self.speed_slider.value()

        self.main_window.simulator.update_settings(ball_size, gravity, speed)

    def set_dark_theme(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, QColor(30, 30, 30))
        self.setPalette(p)

    def set_light_theme(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, QColor(228, 240, 229))
        self.setPalette(p)