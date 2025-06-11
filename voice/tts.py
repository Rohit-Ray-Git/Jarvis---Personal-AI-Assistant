# tts.py
# Placeholder for text-to-speech logic using Edge-TTS 

import pyttsx3
import re

engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Adjust speaking rate if desired

def speak_text(text):
    cleaned = clean_markdown_for_tts(text)
    engine.say(cleaned)
    engine.runAndWait()

def stop_speech():
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