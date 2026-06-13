from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QRadialGradient, QPen
import math
import random

class HologramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.pulse = 0
        self.pulse_direction = 1
        self.particles = []
        for _ in range(150):
            self.particles.append({
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "size": random.uniform(2, 6),
                "speed": random.uniform(0.005, 0.02)
            })
        timer = QTimer(self)
        timer.timeout.connect(self.update_animation)
        timer.start(30)
        
    def update_animation(self):
        self.angle += 0.02
        self.pulse += 0.03 * self.pulse_direction
        if self.pulse >= 1.0 or self.pulse <= 0:
            self.pulse_direction *= -1
        for p in self.particles:
            p["x"] += p["speed"] * (random.uniform(-1, 1))
            p["y"] += p["speed"] * (random.uniform(-1, 1))
            if p["x"] < 0: p["x"] = 1
            if p["x"] > 1: p["x"] = 0
            if p["y"] < 0: p["y"] = 1
            if p["y"] > 1: p["y"] = 0
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        center = QPointF(w/2, h/2)
        radius = min(w, h) * 0.4
        
        gradient = QRadialGradient(center, radius + 20)
        gradient.setColorAt(0, QColor(0, 255, 255, 80))
        gradient.setColorAt(0.7, QColor(0, 100, 150, 40))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, radius+20, radius+20)
        
        painter.setPen(QPen(QColor(0, 255, 255, 200), 6))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for i in range(3):
            r = radius - i * 12
            painter.drawEllipse(center, r, r)
            
        painter.save()
        painter.translate(center)
        painter.rotate(self.angle * 180 / math.pi)
        for i in range(4):
            painter.setPen(QPen(QColor(0, 200, 255, 150 - i*30), 2))
            r = radius * (0.3 + i*0.15)
            painter.drawEllipse(QPointF(0,0), r, r)
        painter.restore()
        
        for p in self.particles:
            x = p["x"] * w
            y = p["y"] * h
            alpha = int(150 + 105 * math.sin(self.angle + p["x"]*20))
            painter.setBrush(QBrush(QColor(0, 255, 255, alpha)))
            painter.drawEllipse(QPointF(x, y), p["size"]/2, p["size"]/2)
            
        core_size = 40 + int(10 * self.pulse)
        painter.setBrush(QBrush(QColor(0, 255, 255, 180)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, core_size, core_size)