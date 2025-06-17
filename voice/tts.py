# tts.py
# Placeholder for text-to-speech logic using Edge-TTS 

import pyttsx3
import re
import threading
import time

engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Adjust speaking rate if desired

# Global state for pause/resume
_speech_state = {
    'chunks': [],
    'index': 0,
    'paused': False,
    'stopped': False,
    'thread': None
}

def speak_text(text):
    stop_speech()  # Stop any ongoing speech
    cleaned = clean_markdown_for_tts(text)
    # Split into sentences/chunks
    chunks = re.split(r'(?<=[.!?]) +', cleaned)
    _speech_state['chunks'] = chunks
    _speech_state['index'] = 0
    _speech_state['paused'] = False
    _speech_state['stopped'] = False
    def run():
        while _speech_state['index'] < len(_speech_state['chunks']):
            if _speech_state['stopped']:
                break
            if _speech_state['paused']:
                time.sleep(0.1)
                continue
            chunk = _speech_state['chunks'][_speech_state['index']]
            engine.say(chunk)
            engine.runAndWait()
            _speech_state['index'] += 1
    t = threading.Thread(target=run, daemon=True)
    _speech_state['thread'] = t
    t.start()

def pause_speech():
    _speech_state['paused'] = True

def resume_speech():
    _speech_state['paused'] = False

def stop_speech():
    _speech_state['stopped'] = True
    engine.stop()

def clean_markdown_for_tts(text):
    # Remove markdown headings, bold, italics, code, etc.
    text = re.sub(r'#+' , '', text)  # Remove headings
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Italic
    text = re.sub(r'`([^`]+)`', r'\1', text)  # Inline code
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
    text = re.sub(r'\!\[(.*?)\]\(.*?\)', '', text)  # Images
    text = re.sub(r'> ', '', text)  # Blockquotes
    text = re.sub(r'- ', '', text)  # List dashes
    text = re.sub(r'\d+\. ', '', text)  # Numbered lists
    text = re.sub(r'\n+', '. ', text)  # Newlines to pause
    text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
    # Remove emoji
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002700-\U000027BF"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    return text.strip() 