from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsEllipseItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QTimer, QRectF, Qt, QUrl
from PyQt5.QtGui import QBrush, QColor, QPen, QPainter, QPalette, QFont, QFontDatabase
import os

class BallSimulator(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_window = parent

        self.setWindowTitle('Ball Simulator')
        self.setGeometry(100, 100, 800, 800)

        # Layout setup for top and main window
        layout = QVBoxLayout(self)

        self.spawn_mode = True
        self.dragged_ball = None

        # sound
        # self.media_player = QMediaPlayer()
        # self.sound_file = "sounds/pop.mp3"
        # self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.sound_file)))
        # self.media_player.error.connect(self.handle_media_error)

        top_widget = QWidget(self)
        top_layout = QHBoxLayout(top_widget)
        top_widget.setFixedHeight(50)

        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto', 'static', 'Roboto-Regular.ttf')
        QFontDatabase.addApplicationFont(font_path)
        font = QFont("Roboto", 18, QFont.Bold)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, QColor(228, 240, 229))
        self.setPalette(p)

        self.toggle_button = QPushButton('Toggle Spawn/Move', self)
        self.toggle_button.setFont(font)
        self.toggle_button.setStyleSheet("""
        QPushButton {
            background-color: rgb(202, 237, 207); 
            color: black; 
            padding: 5px; 
            border-radius: 5px; 
        }
        QPushButton:hover {
            background-color: rgb(154, 227, 165);
        }
        """)
        self.toggle_button.setFixedSize(self.toggle_button.sizeHint())
        top_layout.addWidget(self.toggle_button, 0, Qt.AlignLeft)
        self.toggle_button.clicked.connect(self.toggle_mode)

        self.backButton = QPushButton("Back", self)
        self.backButton.setFont(font)
        self.backButton.setStyleSheet("""
        QPushButton {
            background-color: rgb(202, 237, 207); 
            color: black; 
            padding: 5px; 
            border-radius: 5px; 
        }
        QPushButton:hover {
            background-color: rgb(154, 227, 165);
        }
        """)
        self.backButton.setFixedSize(self.backButton.sizeHint())
        self.backButton.clicked.connect(self.apply_back_button)

        top_layout.addWidget(self.backButton, 0, Qt.AlignRight)

        # Create QGraphicsView and QGraphicsScene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setInteractive(False)
        if self.main_window.start_page.is_dark_mode:
            self.view.setStyleSheet("background-color: rgb(30, 30, 30);")
            self.ball_color = QColor(228, 240, 229)
        else:
            self.view.setStyleSheet("background-color: rgb(228, 240, 229);")
            self.ball_color = QColor(30, 30, 30)
        
        view_size = self.view.size()
        self.scene.setSceneRect(0, 0, view_size.width(), view_size.height())

        layout.addWidget(top_widget)
        layout.addWidget(self.view)


        # Set initial simulation parameters
        self.ball_radius = 50 // 4 
        self.gravity = 1
        self.speed = 5
        self.friction = .99


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_simulation)
        self.timer.start(16)

        self.ball = None
        self.ball_x = 0
        self.ball_y = 0
        self.ball_vx = 0
        self.ball_vy = 0
        self.balls = []

        self.view.mousePressEvent = self.spawn
        self.view.mouseMoveEvent = self.move_ball
        self.view.mouseReleaseEvent = self.release_ball
        self.view.resizeEvent = self.handle_resize

    def spawn(self, event):
        if self.spawn_mode:
            mouse_pos = event.pos()
        
            # Convert to scene coordinates
            scene_pos = self.view.mapToScene(mouse_pos)
            ball_x = scene_pos.x()
            ball_y = scene_pos.y()

            ball_vx = 0
            ball_vy = 0

            print(ball_x)
            print(self.view.width())
            print(ball_y)
            print(self.view.height())

            ball = QGraphicsEllipseItem(0, 0, self.ball_radius * 2, self.ball_radius * 2)
            ball.setBrush(QBrush(self.ball_color))
            ball.setPen(QPen(self.ball_color))
            ball.setPos(ball_x - self.ball_radius, ball_y - self.ball_radius)

            self.scene.addItem(ball)

            self.balls.append({
                'ball': ball,
                'x': ball_x,
                'y': ball_y,
                'vx': ball_vx,
                'vy': ball_vy,
                'tracers': [],
                'clicked': False
            })
        else:
            for ball_info in self.balls:
                ball_x = ball_info['x']
                ball_y = ball_info['y']

                mouse_pos = event.pos()
        
                # Convert to scene coordinates
                scene_pos = self.view.mapToScene(mouse_pos)

                distance = ((scene_pos.x() - ball_x) ** 2 + (scene_pos.y() - ball_y) ** 2) ** 0.5

                # If mouse is inside the ball, apply a velocity (throw the ball)
                if distance <= self.ball_radius:
                    ball_info['clicked'] = True
                    self.dragged_ball = ball_info
                    ball_info['ball'].setBrush(QBrush(QColor(154, 227, 165))) 
                    break
    
    def move_ball(self, event):
        if self.dragged_ball is not None:
            mouse_pos = event.pos()
            scene_pos = self.view.mapToScene(mouse_pos)

            if hasattr(self, 'last_mouse_pos'):
                self.last_mouse_pos = self.current_mouse_pos
            else:
                self.last_mouse_pos = scene_pos

            self.current_mouse_pos = scene_pos

            self.dragged_ball['x'] = scene_pos.x()
            self.dragged_ball['y'] = scene_pos.y()
            self.dragged_ball['ball'].setPos(scene_pos.x() - self.ball_radius, scene_pos.y() - self.ball_radius)
    
    def release_ball(self, event):
        if self.dragged_ball is not None:
            if hasattr(self, 'last_mouse_pos') and hasattr(self, 'current_mouse_pos'):
                delta_x = self.current_mouse_pos.x() - self.last_mouse_pos.x()
                delta_y = self.current_mouse_pos.y() - self.last_mouse_pos.y()

                # Set the ball's velocity to match the cursor's velocity
                self.dragged_ball['vx'] = delta_x
                self.dragged_ball['vy'] = delta_y
            

            self.dragged_ball['clicked'] = False
            self.dragged_ball['ball'].setBrush(QBrush(self.ball_color))
            self.dragged_ball = None

            # Clean up cursor position tracking
            if hasattr(self, 'last_mouse_pos'):
                del self.last_mouse_pos
            if hasattr(self, 'current_mouse_pos'):
                del self.current_mouse_pos
        

    def handle_resize(self, event):
        new_size = event.size()
        self.scene.setSceneRect(0, 0, new_size.width(), new_size.height())
        super(QGraphicsView, self.view).resizeEvent(event)

    def run_simulation(self):
        for ball_info in self.balls:
            if ball_info['clicked'] == False:
                # Apply gravity to the vertical velocity (vy)
                ball_info['vy'] += self.gravity

                # Update the ball's position based on its velocity
                ball_info['x'] += ball_info['vx']
                ball_info['y'] += ball_info['vy']

                scene_rect = self.view.mapToScene(self.view.viewport().rect()).boundingRect()
                # print(scene_rect)

                ball_info['ball'].setBrush(QBrush(self.ball_color))

                # Bottom boundary
                if ball_info['y'] + self.ball_radius >= scene_rect.height():
                    ball_info['y'] = scene_rect.bottom() - self.ball_radius
                    ball_info['vy'] *= -self.friction

                # Top boundary
                if ball_info['y'] - self.ball_radius <= 0:
                    ball_info['y'] = scene_rect.top() + self.ball_radius
                    ball_info['vy'] *= -self.friction

                # Left boundary
                if ball_info['x'] - self.ball_radius <= 0:
                    ball_info['x'] = scene_rect.left() + self.ball_radius
                    ball_info['vx'] *= -self.friction

                # Right boundary
                if ball_info['x'] + self.ball_radius >= scene_rect.width():
                    ball_info['x'] = scene_rect.right() - self.ball_radius
                    ball_info['vx'] *= -self.friction  
                
                # Update the ball's position on the scene (for graphical rendering)
                ball_info['ball'].setPos(ball_info['x'] - self.ball_radius, ball_info['y'] - self.ball_radius)

            tracer = QGraphicsEllipseItem(0, 0, self.ball_radius*.2, self.ball_radius*.2)
            tracer.setBrush(QBrush(self.ball_color))
            tracer.setPen(QPen(self.ball_color))
            tracer.setPos(ball_info['x'], ball_info['y'])
            
            self.scene.addItem(tracer)
            ball_info['tracers'].append(tracer)

            if len(ball_info['tracers']) > 10:
                old_tracer = ball_info['tracers'].pop(0)
                self.scene.removeItem(old_tracer)

    def update_settings(self, ball_size, gravity, speed):
        self.ball_size = ball_size
        self.ball_radius = self.ball_size // 4
        self.gravity = gravity
        self.speed = speed

    def set_dark_theme(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, QColor(30, 30, 30))
        self.view.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.ball_color = QColor(228, 240, 229)
        self.setPalette(p)

    def set_light_theme(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, QColor(228, 240, 229))
        self.view.setStyleSheet("background-color: rgb(228, 240, 229);")
        self.ball_color = QColor(30, 30, 30)
        self.setPalette(p)

    def apply_back_button(self):
        for ball in self.balls:
            self.scene.removeItem(ball['ball'])
            for tracers in ball['tracers']:
                self.scene.removeItem(tracers)
        self.balls.clear()
        self.balls = []

        self.backButton.clicked.connect(self.main_window.show_start_page)

    def toggle_mode(self):
        self.spawn_mode = not self.spawn_mode