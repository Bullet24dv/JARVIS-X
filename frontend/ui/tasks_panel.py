from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class TasksPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("Tasks")
        title.setStyleSheet("font-size: 24px; color: cyan;")
        layout.addWidget(title)
        self.task_table = QTableWidget(0, 3)
        self.task_table.setHorizontalHeaderLabels(["ID", "Task", "Status"])
        layout.addWidget(self.task_table)
        self.setLayout(layout)