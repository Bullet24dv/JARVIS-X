from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem

class AgentsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("Agents")
        title.setStyleSheet("font-size: 24px; color: cyan;")
        layout.addWidget(title)
        self.agent_list = QListWidget()
        self.agents = ["Programmer", "Researcher", "Analyst", "Financial", "Marketing", "Sales", "Automation", "Security", "SmartHome", "StarCars"]
        for agent in self.agents:
            item = QListWidgetItem(agent)
            self.agent_list.addItem(item)
        layout.addWidget(self.agent_list)
        self.setLayout(layout)
        
    def update_status(self, agent: str, status: str):
        for i in range(self.agent_list.count()):
            if self.agent_list.item(i).text() == agent:
                self.agent_list.item(i).setText(f"{agent} - {status}")