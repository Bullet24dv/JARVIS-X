from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient
import random

class VoiceVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.bars = [0.0] * 40
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
        self.active = False
        self.setFixedHeight(100)
        
    def update_animation(self):
        if self.active:
            for i in range(len(self.bars)):
                self.bars[i] = max(0.1, self.bars[i] + random.uniform(-0.15, 0.25))
                self.bars[i] = min(1.0, self.bars[i])
        else:
            for i in range(len(self.bars)):
                self.bars[i] *= 0.95
        self.update()
        
    def show_response(self, text: str):
        self.active = True
        self.parent().statusBar.showMessage(text, 3000)
        QTimer.singleShot(2000, lambda: setattr(self, 'active', False))
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        bar_width = w / len(self.bars)
        
        for i, amp in enumerate(self.bars):
            bar_height = int(amp * h * 0.8)
            x = i * bar_width
            y = (h - bar_height) // 2
            gradient = QLinearGradient(x, y, x, y + bar_height)
            gradient.setColorAt(0, QColor(0, 255, 255, 200))
            gradient.setColorAt(1, QColor(0, 100, 200, 150))
            painter.fillRect(QRectF(x, y, bar_width - 2, bar_height), QBrush(gradient))