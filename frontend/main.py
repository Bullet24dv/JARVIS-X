import sys
import asyncio
import qasync
from PyQt6.QtWidgets import QApplication

# Importación relativa desde el mismo paquete
from .jarvis_app import JarvisApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    window = JarvisApp()
    window.show()
    
    with loop:
        loop.run_forever()