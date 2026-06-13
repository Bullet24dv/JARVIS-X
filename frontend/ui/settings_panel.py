from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; color: cyan;")
        layout.addWidget(title)
        
        form = QFormLayout()
        self.llm_provider = QLineEdit("deepseek")
        self.tts_voice = QLineEdit("elevenlabs")
        form.addRow("LLM Provider:", self.llm_provider)
        form.addRow("TTS Voice:", self.tts_voice)
        layout.addLayout(form)
        
        save_btn = QPushButton("Save")
        layout.addWidget(save_btn)
        self.setLayout(layout)