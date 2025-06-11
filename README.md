# Jarvis: Your Personal AI Assistant

A modern, extensible personal assistant for Windows, inspired by Iron Man's Jarvis. Supports both voice and text interfaces, beautiful neural voices, offline speech recognition, system control, web search, and more.

## Features
- Voice and text input
- Beautiful neural voice output (Edge-TTS)
- Offline speech recognition (Vosk)
- Modern GUI (PyQt5/customtkinter)
- System control (open apps, search files, etc.)
- Web search and scraping
- LLM integration (OpenAI or local models)
- Extensible command/plugin system

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download Vosk model (see [Vosk models](https://alphacephei.com/vosk/models)) and place in `models/` directory.
4. Run the assistant:
   ```bash
   python main.py
   ```

## Configuration
- Place your API keys (if needed) in a `.env` file or as environment variables.
- Edit `config.py` for custom settings.

## License
MIT 