# 🤖 Jarvis: Your Personal AI Assistant

A modern, extensible, and beautiful personal assistant for Windows, inspired by Iron Man's Jarvis. Supports both voice and text interfaces, neural voices, offline speech recognition, system control, web search, file search, and more—all in a chat-like, themeable GUI.

---

## ✨ Features

- 💬 **Voice & Text Input**: Talk or type to Jarvis
- 🗣️ **Natural Voice Output**: Beautiful TTS (pyttsx3, Edge-TTS optional)
- 🎨 **Modern GUI**: Light/dark themes, chat bubbles, settings, and more
- 🗂️ **File Search**: Find and open files anywhere on your PC (with clickable results)
- 🌐 **In-App Web Search**: Real-time web search & summarization, clickable links
- 🖥️ **System Control**: Open any app, folder, or browser
- 📝 **Conversation History**: Auto-save/load, clear, and export chat
- ⚙️ **Settings Dialog**: Voice toggle, user/assistant names, theme
- 🛑 **Stop Voice Button**: Instantly stop TTS output
- 🚦 **Robust Error Handling**: Friendly feedback for all actions

---

## 🚀 Quick Start

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Download a Vosk model** ([see here](https://alphacephei.com/vosk/models)) and place it in the `models/` directory. Update `config.py` if needed.
4. **Set up your `.env` file** in the project root:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
   ```
5. **Run the assistant**:
   ```bash
   python main.py
   ```

---

## 🖥️ Usage

- **Type or speak** your query in the chat window.
- **See your message instantly**; Jarvis will show a "typing..." indicator while processing.
- **Click links** in web/file results to open them.
- **Switch themes** with the 🌙/☀️ button.
- **Open settings** (⚙️) to change names or toggle voice.
- **Clear** (🗑️) or **export** (📄) your conversation.
- **Stop voice** output anytime with ⏹️.

---

## 🛠️ Configuration

- **API Keys**: Place your OpenRouter API key in `.env`.
- **Vosk Model**: Download and set the path in `config.py`.
- **Settings**: User/assistant names, theme, and voice toggle are saved in `settings.json`.

---

## 🧩 Extending Jarvis

- Add new commands in `commands/` or utilities in `utils/`.
- Improve intent detection in `gui/gui_main.py`.
- Add plugins for reminders, calendar, smart home, etc.

---

## 📝 Example Queries

- `search for latest AI news`
- `find file resume`
- `open notepad`
- `open browser`
- `locate document budget`
- `shutdown`

---

## 🧑‍💻 Contributing

Pull requests and suggestions are welcome! Please open an issue to discuss major changes.

---

## 📄 License

MIT 