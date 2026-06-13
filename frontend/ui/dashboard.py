from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; color: cyan;")
        layout.addWidget(title)
        
        grid = QGridLayout()
        stats = [
            ("Estado", "Activo"),
            ("Modelo IA", "DeepSeek"),
            ("Agentes", "10"),
            ("Memoria", "Cargada")
        ]
        for i, (label, value) in enumerate(stats):
            lbl = QLabel(f"{label}: {value}")
            lbl.setStyleSheet("font-size: 16px; color: white;")
            grid.addWidget(lbl, i//2, i%2)
        layout.addLayout(grid)
        self.setLayout(layout)