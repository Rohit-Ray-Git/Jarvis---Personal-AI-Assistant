# gui_main.py
# Placeholder for GUI logic (PyQt5 or customtkinter) 

import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QLabel, QHBoxLayout, QDialog, QFormLayout, QCheckBox, QDialogButtonBox, QLineEdit as QLineEditDialog, QFileDialog
)
from PyQt5.QtCore import QUrl, QTimer, Qt, pyqtSignal
from commands.llm import get_llm_response
from voice.tts import speak_text, stop_speech, clean_markdown_for_tts, pause_speech, resume_speech
from voice.stt import listen_and_transcribe
from commands.system import shutdown, open_folder, open_default_browser, open_application
from commands.web import search_and_summarize
from utils.file_search import search_files
import threading
import re
import subprocess
import markdown
import datetime

SETTINGS_FILE = 'settings.json'
HISTORY_FILE = 'history.json'

LIGHT_THEME = """
QWidget { background-color: #f0f0f0; color: #333; }
QTextBrowser, QLineEdit {
    background-color: #ffffff;
    color: #333;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 5px;
}
QPushButton {
    background-color: #e0e0e0;
    color: #333;
    border-radius: 5px;
    padding: 5px;
    border: 1px solid #c0c0c0;
}
QPushButton:hover { background-color: #d0d0d0; }
QTextBrowser {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
}
h1, h2, h3, h4, h5, h6 {
    color: #0055a4; /* A nice blue */
    margin-top: 1em;
    margin-bottom: 0.5em;
}
p {
    margin-bottom: 0.5em;
    line-height: 1.5;
}
ul, ol {
    margin-left: 1.5em;
    margin-bottom: 0.5em;
}
li {
    margin-bottom: 0.2em;
}
code {
    background-color: #e8e8e8;
    color: #d63369; /* A nice pink/red */
    font-family: 'Courier New', Courier, monospace;
    padding: 2px 4px;
    border-radius: 3px;
}
pre {
    background-color: #f7f7f7;
    border: 1px solid #ddd;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
    font-family: 'Courier New', Courier, monospace;
    white-space: pre-wrap; /* Allows text to wrap */
}
pre code {
    background-color: transparent;
    padding: 0;
    border-radius: 0;
}
blockquote {
    border-left: 3px solid #0055a4;
    margin-left: 10px;
    padding-left: 10px;
    color: #555;
}
a { color: #007bff; text-decoration: none; }
a:hover { text-decoration: underline; }
"""
DARK_THEME = """
QWidget { background-color: rgb(40, 40, 40); color: #f5f5f5; }
QTextBrowser, QLineEdit {
    background-color: rgb(30, 30, 30);
    color: #f5f5f5;
    border: 1px solid rgb(50, 50, 50);
    border-radius: 5px;
    padding: 5px;
}
QPushButton {
    background-color: rgb(60, 60, 60);
    color: #f5f5f5;
    border-radius: 5px;
    padding: 5px;
    border: 1px solid rgb(70, 70, 70);
}
QPushButton:hover { background-color: rgb(80, 80, 80); }
QTextBrowser {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
}
h1, h2, h3, h4, h5, h6 {
    color: #a9f;
    margin-top: 1em;
    margin-bottom: 0.5em;
}
p {
    margin-bottom: 0.5em;
    line-height: 1.5;
}
ul, ol {
    margin-left: 1.5em;
    margin-bottom: 0.5em;
}
li {
    margin-bottom: 0.2em;
}
code {
    background-color: rgb(50, 50, 50);
    color: #da5;
    font-family: 'Courier New', Courier, monospace;
    padding: 2px 4px;
    border-radius: 3px;
}
pre {
    background-color: rgb(30, 30, 30);
    border: 1px solid rgb(50, 50, 50);
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
    font-family: 'Courier New', Courier, monospace;
    white-space: pre-wrap; /* Allows text to wrap */
}
pre code {
    background-color: transparent;
    padding: 0;
    border-radius: 0;
}
blockquote {
    border-left: 3px solid #a9f;
    margin-left: 10px;
    padding-left: 10px;
    color: #ccc;
}
a { color: #8af; text-decoration: none; }
a:hover { text-decoration: underline; }
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
    assistant_message_signal = pyqtSignal(str, bool)  # (message, is_markdown)
    error_signal = pyqtSignal(str)
    remove_loading_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_dark = False
        self.settings = load_settings()
        self.history = load_history()
        self.loading_timer = None
        self.loading_msg_cursor = None
        self.loading_dots = 1
        self.init_ui()
        self.load_conversation()
        # Connect signals
        self.assistant_message_signal.connect(self.append_conversation)
        self.error_signal.connect(self.show_error)
        self.remove_loading_signal.connect(self.remove_loading)

    def init_ui(self):
        self.setWindowTitle('Jarvis - Personal AI Assistant')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel('Jarvis Conversation')
        layout.addWidget(self.label)

        self.conversation = QTextBrowser()
        self.conversation.setReadOnly(True)
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

        self.stop_voice_button = QPushButton('⏹️ Stop Voice')
        input_layout.addWidget(self.stop_voice_button)

        self.pause_voice_button = QPushButton('⏸️ Pause Voice')
        input_layout.addWidget(self.pause_voice_button)

        self.resume_voice_button = QPushButton('▶️ Resume Voice')
        input_layout.addWidget(self.resume_voice_button)

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
        self.stop_voice_button.clicked.connect(self.handle_stop_voice)
        self.pause_voice_button.clicked.connect(self.handle_pause_voice)
        self.resume_voice_button.clicked.connect(self.handle_resume_voice)

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

    def show_loading(self):
        # Add loading message and keep cursor
        self.loading_dots = 1
        self.loading_msg_cursor = self.conversation.textCursor()
        self.conversation.append('<b>Jarvis is typing<span id="dots">.</span></b>')
        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.animate_loading)
        self.loading_timer.start(400)

    def animate_loading(self):
        self.loading_dots = (self.loading_dots % 3) + 1
        # Move cursor to the end and select the last block
        cursor = self.conversation.textCursor()
        cursor.movePosition(cursor.End)
        cursor.select(cursor.BlockUnderCursor)
        text = f'<b>Jarvis is typing<span id="dots">{"." * self.loading_dots}</span></b>'
        cursor.removeSelectedText()
        cursor.insertHtml(text)
        self.conversation.setTextCursor(cursor)

    def remove_loading(self):
        if self.loading_timer:
            self.loading_timer.stop()
            self.loading_timer = None
        # Remove the last block (loading message)
        cursor = self.conversation.textCursor()
        cursor.movePosition(cursor.End)
        cursor.select(cursor.BlockUnderCursor)
        cursor.removeSelectedText()
        self.conversation.setTextCursor(cursor)
        # Add a newline to ensure separation
        self.conversation.append("")

    def handle_send(self):
        user_text = self.input_box.text().strip()
        if not user_text:
            return
        self.append_conversation(f'<b>{self.settings.get("user_name", "You")}:</b> {user_text}')
        self.input_box.clear()
        response = None
        user_text_lower = user_text.lower()

        try:
            # Make file search intent more specific
            file_search_match = re.match(r"(find|search for|locate) (file|document) (.+)", user_text_lower)
            if file_search_match:
                query = file_search_match.group(3).strip()
                self.show_loading()
                def file_search_thread():
                    try:
                        results = search_files(query)
                        if results:
                            links = '\n'.join([f'<a href="file:///{path}">{path}</a>' for path in results])
                            response = f"Found {len(results)} file(s):<br>{links}"
                            self.remove_loading_signal.emit()
                            self.assistant_message_signal.emit(f'<b>{self.settings.get("assistant_name", "Jarvis")}:</b> {response}', False)
                            if self.settings.get('voice', True):
                                speak_text(f"Found {len(results)} file{'s' if len(results) > 1 else ''}.")
                        else:
                            response = f"No files found matching '{query}'."
                            self.remove_loading_signal.emit()
                            self.assistant_message_signal.emit(f'<b>{self.settings.get("assistant_name", "Jarvis")}:</b> {response}', False)
                            if self.settings.get('voice', True):
                                speak_text(response)
                    except Exception as e:
                        self.remove_loading_signal.emit()
                        self.error_signal.emit(f"File search error: {e}")
                threading.Thread(target=file_search_thread, daemon=True).start()
                return
            # In-app web search and summarization (explicit)
            elif user_text_lower.startswith(("search for ", "search ")):
                query_match = re.match(r"search (for )?(.+)", user_text_lower)
                query = query_match.group(2).strip()

                self.show_loading()
                def web_search_thread():
                    try:
                        result = search_and_summarize(query)
                        # The 'summary' key now contains the full markdown content
                        markdown_response = result['summary']
                        self.remove_loading_signal.emit()
                        # Pass the full markdown response to be rendered
                        self.assistant_message_signal.emit(
                            f'<b>{self.settings.get("assistant_name", "Jarvis")} (Web):</b>\n{markdown_response}', 
                            True
                        )
                        # For TTS, we need a plain text summary.
                        # The clean_markdown_for_tts function handles removal of links, etc.
                        if self.settings.get('voice', True):
                            speak_text(markdown_response[:1000]) # Speak the first 1000 chars of the summary
                    except Exception as e:
                        self.remove_loading_signal.emit()
                        self.error_signal.emit(f"Web search error: {e}")
                threading.Thread(target=web_search_thread, daemon=True).start()
                return
            # Automatic news/current event detection
            elif is_news_query(user_text):
                self.show_loading()
                def web_search_thread():
                    try:
                        result = search_and_summarize(user_text)
                        markdown_response = result['summary']
                        self.remove_loading_signal.emit()
                        self.assistant_message_signal.emit(
                            f'<b>{self.settings.get("assistant_name", "Jarvis")} (Web):</b>\n{markdown_response}',
                            True
                        )
                        if self.settings.get('voice', True):
                            speak_text(markdown_response[:1000]) # Speak the first 1000 chars of the summary
                    except Exception as e:
                        self.remove_loading_signal.emit()
                        self.error_signal.emit(f"Web search error: {e}")
                threading.Thread(target=web_search_thread, daemon=True).start()
                return
            # Open default browser for web tasks
            elif re.match(r"^(open|launch) browser$", user_text_lower):
                try:
                    response = open_default_browser()
                except Exception as e:
                    self.show_error(f"Browser error: {e}")
                    return
            elif re.match(r"^open https?://", user_text_lower):
                try:
                    url = user_text.split(" ", 1)[1].strip()
                    response = open_default_browser(url)
                except Exception as e:
                    self.show_error(f"Browser error: {e}")
                    return
            elif re.match(r"^open folder ", user_text_lower):
                try:
                    folder = user_text_lower.replace("open folder", "").strip()
                    response = open_folder(folder)
                except Exception as e:
                    self.show_error(f"Open folder error: {e}")
                    return
            elif user_text_lower.startswith("open "):
                app_name = user_text_lower.replace("open ", "").strip()
                try:
                    # If it looks like a URL, open in browser
                    if app_name.startswith("http://") or app_name.startswith("https://"):
                        response = open_default_browser(app_name)
                    else:
                        response = open_application(app_name)
                except Exception as e:
                    self.show_error(f"Open application error: {e}")
                    return
            elif "shutdown" in user_text_lower:
                try:
                    response = shutdown()
                except Exception as e:
                    self.show_error(f"Shutdown error: {e}")
                    return
            # Add more intents here as needed
            if response:
                if user_text_lower.startswith("search for ") or (response and response.startswith('Here are')):
                    self.append_conversation(f'**{self.settings.get("assistant_name", "Jarvis")}:**\n' + response, is_markdown=True)
                else:
                    self.append_conversation(f'<b>{self.settings.get("assistant_name", "Jarvis")}:</b> {response}')
                if not file_search_match and self.settings.get('voice', True):
                    speak_text(response)
            else:
                # Fallback to LLM
                self.show_loading()
                def llm_thread():
                    try:
                        response = get_llm_response(user_text, self.history)
                        self.remove_loading_signal.emit()
                        self.assistant_message_signal.emit(
                            f'<b>{self.settings.get("assistant_name", "Jarvis")}:</b>\n{response}', 
                            True
                        )
                        if self.settings.get('voice', True):
                            speak_text(clean_markdown_for_tts(response))
                    except Exception as e:
                        self.remove_loading_signal.emit()
                        self.error_signal.emit(f"LLM error: {e}")
                threading.Thread(target=llm_thread, daemon=True).start()
        except Exception as e:
            self.remove_loading()
            self.show_error(f"Unexpected error: {e}")

    def append_conversation(self, text, is_markdown=False):
        if is_markdown:
            # Split sender from message
            parts = text.split('\n', 1)
            sender = parts[0]
            message = parts[1] if len(parts) > 1 else ''
            
            # Add sender to view and history
            self.conversation.append(sender)
            self.history.append(sender)

            # Convert markdown and add message to view and history
            html = markdown.markdown(message, extensions=['fenced_code', 'tables', 'sane_lists'])
            self.conversation.append(html)
            self.history.append(html)
        else:
            self.conversation.append(text)
            self.history.append(text)
        
        save_history(self.history)

    def load_conversation(self):
        self.conversation.clear()
        # self.history is already loaded in __init__
        for item in self.history:
            self.conversation.append(item)

    def clear_conversation(self):
        self.history = []
        self.conversation.clear()
        save_history(self.history)

    def handle_file_link(self, url: QUrl):
        file_path = url.toLocalFile()
        if os.path.exists(file_path):
            os.startfile(file_path)

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

    def show_error(self, message):
        self.append_conversation(f'<span style="color:#c00;"><i>⚠️ {message}</i></span>')

    def handle_stop_voice(self):
        stop_speech()

    def handle_pause_voice(self):
        pause_speech()

    def handle_resume_voice(self):
        resume_speech()

def is_news_query(text):
    keywords = [
        "news", "today", "latest", "current", "update", "updates", "recent", "now", "headline", "happening", "breaking", "event", "events"
    ]
    text_lower = text.lower()
    # If the query contains a date (today, yesterday, this week, etc.) or news-related keywords
    if any(word in text_lower for word in keywords):
        return True
    # If the query contains a date string (e.g., 2024, month names)
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    if any(month in text_lower for month in months):
        return True
    if any(str(year) in text_lower for year in range(2020, datetime.datetime.now().year + 1)):
        return True
    return False

# For standalone testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JarvisGUI()
    window.show()
    sys.exit(app.exec_()) 