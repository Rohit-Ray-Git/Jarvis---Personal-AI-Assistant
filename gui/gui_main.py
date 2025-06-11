# gui_main.py
# Placeholder for GUI logic (PyQt5 or customtkinter) 

import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout, QDialog, QFormLayout, QCheckBox, QDialogButtonBox, QLineEdit as QLineEditDialog, QFileDialog
)
from PyQt5.QtCore import QUrl
from commands.llm import get_llm_response
from voice.tts import speak_text
from voice.stt import listen_and_transcribe
from commands.system import open_chrome, shutdown, open_folder, open_default_browser, open_application
from commands.web import search_and_summarize
from utils.file_search import search_files
import threading
import re
import subprocess

SETTINGS_FILE = 'settings.json'
HISTORY_FILE = 'history.json'

LIGHT_THEME = """
QWidget { background-color: #f5f5f5; color: #222; }
QTextEdit, QLineEdit { background-color: #fff; color: #222; }
QPushButton { background-color: #e0e0e0; color: #222; border-radius: 5px; padding: 5px; }
QPushButton:hover { background-color: #d0d0d0; }
"""
DARK_THEME = """
QWidget { background-color: #232629; color: #f5f5f5; }
QTextEdit, QLineEdit { background-color: #2c2f34; color: #f5f5f5; }
QPushButton { background-color: #444; color: #f5f5f5; border-radius: 5px; padding: 5px; }
QPushButton:hover { background-color: #555; }
"""

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"voice": True, "user_name": "User", "assistant_name": "Jarvis"}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f)

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        layout = QFormLayout(self)
        self.voice_checkbox = QCheckBox('Enable Voice Output')
        self.voice_checkbox.setChecked(settings.get('voice', True))
        layout.addRow(self.voice_checkbox)
        self.user_name_edit = QLineEditDialog(settings.get('user_name', 'User'))
        layout.addRow('User Name:', self.user_name_edit)
        self.assistant_name_edit = QLineEditDialog(settings.get('assistant_name', 'Jarvis'))
        layout.addRow('Assistant Name:', self.assistant_name_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    def get_settings(self):
        return {
            "voice": self.voice_checkbox.isChecked(),
            "user_name": self.user_name_edit.text(),
            "assistant_name": self.assistant_name_edit.text()
        }

class JarvisGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark = False
        self.settings = load_settings()
        self.history = load_history()
        self.init_ui()
        self.load_conversation()

    def init_ui(self):
        self.setWindowTitle('Jarvis - Personal AI Assistant')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel('Jarvis Conversation')
        layout.addWidget(self.label)

        self.conversation = QTextEdit()
        self.conversation.setReadOnly(True)
        self.conversation.setOpenExternalLinks(False)
        self.conversation.anchorClicked.connect(self.handle_file_link)
        layout.addWidget(self.conversation)

        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText('Type your message...')
        input_layout.addWidget(self.input_box)

        self.send_button = QPushButton('Send')
        input_layout.addWidget(self.send_button)

        self.speak_button = QPushButton('Speak')
        input_layout.addWidget(self.speak_button)

        self.theme_button = QPushButton('🌙 Theme')
        input_layout.addWidget(self.theme_button)

        self.settings_button = QPushButton('⚙️ Settings')
        input_layout.addWidget(self.settings_button)

        self.clear_button = QPushButton('🗑️ Clear')
        input_layout.addWidget(self.clear_button)

        self.export_button = QPushButton('📄 Export')
        input_layout.addWidget(self.export_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

        # Connect buttons
        self.send_button.clicked.connect(self.handle_send)
        self.input_box.returnPressed.connect(self.handle_send)
        self.speak_button.clicked.connect(self.handle_speak)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.settings_button.clicked.connect(self.open_settings)
        self.clear_button.clicked.connect(self.clear_conversation)
        self.export_button.clicked.connect(self.export_conversation)

        self.apply_theme()

    def apply_theme(self):
        if self.is_dark:
            self.setStyleSheet(DARK_THEME)
            self.theme_button.setText('☀️ Theme')
        else:
            self.setStyleSheet(LIGHT_THEME)
            self.theme_button.setText('🌙 Theme')

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def handle_send(self):
        user_text = self.input_box.text().strip()
        if user_text:
            self.append_conversation(f'<b>{self.settings.get("user_name", "You")}:</b> {user_text}')
            self.input_box.clear()
            response = None
            user_text_lower = user_text.lower()

            # File search intent
            file_search_match = re.match(r"(find|search for|locate) (file|document|) ?(.+)", user_text_lower)
            if file_search_match:
                query = file_search_match.group(3).strip()
                results = search_files(query)
                if results:
                    links = '\n'.join([f'<a href="file:///{path}">{path}</a>' for path in results])
                    response = f"Found {len(results)} file(s):<br>{links}"
                    if self.settings.get('voice', True):
                        speak_text(f"Found {len(results)} file{'s' if len(results) > 1 else ''}.")
                else:
                    response = f"No files found matching '{query}'."
                    if self.settings.get('voice', True):
                        speak_text(response)
            # In-app web search and summarization
            elif user_text_lower.startswith("search for "):
                query = user_text[11:].strip()
                self.append_conversation(f'<i>Searching the web for: {query} ...</i>')
                def web_search_thread():
                    summary = search_and_summarize(query)
                    self.append_conversation(f'<b>{self.settings.get("assistant_name", "Jarvis")} (Web):</b> {summary}')
                    if self.settings.get('voice', True):
                        speak_text(summary[:400])  # Limit spoken summary length
                threading.Thread(target=web_search_thread, daemon=True).start()
                return
            # Open default browser for web tasks
            elif re.match(r"^(open|launch) browser$", user_text_lower):
                response = open_default_browser()
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
                self.append_conversation(f'<b>{self.settings.get("assistant_name", "Jarvis")}:</b> {response}')
                if not file_search_match and self.settings.get('voice', True):
                    speak_text(response)
            else:
                # Fallback to LLM
                response = get_llm_response(user_text)
                self.append_conversation(f'<b>{self.settings.get("assistant_name", "Jarvis")}:</b> {response}')
                if self.settings.get('voice', True):
                    speak_text(response)
            self.save_conversation()

    def append_conversation(self, text):
        self.conversation.append(text)
        self.history.append(text)

    def save_conversation(self):
        save_history(self.history)

    def load_conversation(self):
        for line in self.history:
            self.conversation.append(line)

    def clear_conversation(self):
        self.conversation.clear()
        self.history = []
        self.save_conversation()

    def handle_file_link(self, url: QUrl):
        path = url.toLocalFile()
        if os.path.exists(path):
            os.startfile(path)

    def handle_speak(self):
        def stt_thread():
            text = listen_and_transcribe()
            if text:
                self.input_box.setText(text)
                self.handle_send()
        threading.Thread(target=stt_thread, daemon=True).start()

    def open_settings(self):
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_():
            self.settings = dialog.get_settings()
            save_settings(self.settings)

    def export_conversation(self):
        if not self.history:
            return
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Conversation", "conversation.txt", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                for line in self.history:
                    # Remove HTML tags for plain text export
                    plain = re.sub('<[^<]+?>', '', line)
                    f.write(plain + '\n')

# For standalone testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JarvisGUI()
    window.show()
    sys.exit(app.exec_()) 