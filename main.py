# main.py
"""
Entry point for Jarvis AI Assistant
"""

# Import core modules (to be implemented)
# from gui import JarvisGUI
# from voice import VoiceAssistant
# from commands import CommandHandler

import sys
from gui.gui_main import JarvisGUI
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = JarvisGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 