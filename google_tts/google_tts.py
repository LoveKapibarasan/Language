from google.cloud import texttospeech
import os
import sys
import json
from sanitize_text import sanitize_text

# Set environment variable for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Initialize client
client = texttospeech.TextToSpeechClient()

print("Enter the text to synthesize (end with Ctrl+D):")
text = sys.stdin.read()

text = sanitize_text(text)


synthesis_input = texttospeech.SynthesisInput(text=text)

# --- Read lang config ---
with open("lang.json", "r", encoding="utf-8") as f:
    lang_config = json.load(f)

# --- Show options to user ---
print("Available languages:")
for i, (lang_code, voice) in enumerate(lang_config.items(), start=1):
    print(f"{i}. {lang_code} ({voice['name']}, {voice['gender']})")

# --- User selects language ---
try:
    choice = int(input("Choose language number: ").strip())
    lang_code = list(lang_config.keys())[choice - 1]
except (IndexError, ValueError):
    print("Invalid choice. Exiting.")
    sys.exit(1)

voice_info = lang_config[lang_code]

# --- Create VoiceSelectionParams ---
voice = texttospeech.VoiceSelectionParams(
    language_code=lang_code,
    name=voice_info["name"],
    ssml_gender=texttospeech.SsmlVoiceGender[voice_info["gender"]]
)

print(f"Using voice: {voice.name} ({lang_code}, {voice_info['gender']})")


audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform request
response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

# Save output
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print("Audio content written to output.mp3")

