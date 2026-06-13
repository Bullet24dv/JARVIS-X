from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget

class MemoryPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("Memory Panel")
        title.setStyleSheet("font-size: 24px; color: cyan;")
        layout.addWidget(title)
        self.memory_list = QListWidget()
        layout.addWidget(self.memory_list)
        self.setLayout(layout)