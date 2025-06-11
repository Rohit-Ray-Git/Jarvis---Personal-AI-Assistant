# gui_main.py
# Placeholder for GUI logic (PyQt5 or customtkinter) 

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout
from commands.llm import get_llm_response
from voice.tts import speak_text
from voice.stt import listen_and_transcribe
from commands.system import open_chrome, shutdown, open_folder, open_default_browser, open_application
from utils.file_search import search_files
import threading
import re
import os
import subprocess

class JarvisGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Jarvis - Personal AI Assistant')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel('Jarvis Conversation')
        layout.addWidget(self.label)

        self.conversation = QTextEdit()
        self.conversation.setReadOnly(True)
        layout.addWidget(self.conversation)

        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText('Type your message...')
        input_layout.addWidget(self.input_box)

        self.send_button = QPushButton('Send')
        input_layout.addWidget(self.send_button)

        self.speak_button = QPushButton('Speak')
        input_layout.addWidget(self.speak_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

        # Connect buttons
        self.send_button.clicked.connect(self.handle_send)
        self.input_box.returnPressed.connect(self.handle_send)
        self.speak_button.clicked.connect(self.handle_speak)

    def handle_send(self):
        user_text = self.input_box.text().strip()
        if user_text:
            self.conversation.append(f'<b>You:</b> {user_text}')
            self.input_box.clear()
            response = None
            user_text_lower = user_text.lower()

            # File search intent
            file_search_match = re.match(r"(find|search for|locate) (file|document|) ?(.+)", user_text_lower)
            if file_search_match:
                query = file_search_match.group(3).strip()
                results = search_files(query)
                if results:
                    response = f"Found {len(results)} file(s):\n" + '\n'.join(results)
                    speak_text(f"Found {len(results)} file{'s' if len(results) > 1 else ''}.")
                    # Optionally, open the first file or its folder
                    # Uncomment below to auto-open the first file:
                    # os.startfile(results[0])
                else:
                    response = f"No files found matching '{query}'."
                    speak_text(response)
            # Open default browser for web tasks
            elif re.match(r"^(open|launch) browser$", user_text_lower):
                response = open_default_browser()
            elif user_text_lower.startswith("search for "):
                query = user_text[11:].strip()
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                response = open_default_browser(url)
            elif re.match(r"^open https?://", user_text_lower):
                url = user_text.split(" ", 1)[1].strip()
                response = open_default_browser(url)
            elif re.match(r"^open folder ", user_text_lower):
                folder = user_text_lower.replace("open folder", "").strip()
                response = open_folder(folder)
            elif user_text_lower.startswith("open "):
                app_name = user_text_lower.replace("open ", "").strip()
                # If it looks like a URL, open in browser
                if app_name.startswith("http://") or app_name.startswith("https://"):
                    response = open_default_browser(app_name)
                else:
                    response = open_application(app_name)
            elif "shutdown" in user_text_lower:
                response = shutdown()
            # Add more intents here as needed
            if response:
                self.conversation.append(f'<b>Jarvis:</b> {response}')
                if not file_search_match:
                    speak_text(response)
            else:
                # Fallback to LLM
                response = get_llm_response(user_text)
                self.conversation.append(f'<b>Jarvis:</b> {response}')
                speak_text(response)

    def handle_speak(self):
        def stt_thread():
            text = listen_and_transcribe()
            if text:
                self.input_box.setText(text)
                self.handle_send()
        threading.Thread(target=stt_thread, daemon=True).start()

# For standalone testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JarvisGUI()
    window.show()
    sys.exit(app.exec_()) 