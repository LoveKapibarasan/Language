# 🎙️ Speech & Flashcard Utility Suite

This repository provides a dual-purpose GUI tool:

1. **Azure Speech Service Launcher** – for Text-to-Speech (TTS) and Speech-to-Text (STT) using Azure.
2. **Flashcard File Processor** – for preparing multilingual Anki flashcards with audio/image support.

---

## 🚀 Features

### 🧠 1. Azure Speech Mode Selector (`main.py`)
**Purpose**: Launches either a TTS or STT GUI built with PyQt5.

- Uses Microsoft Azure Cognitive Services
- GUI options:
  - 🔊 **Text to Speech** (input text → output audio)
  - 🗣️ **Speech to Text** (input audio → transcribed text)
- Icons and layout included (`ico/azure.ico` required)

---

### 🧩 2. Flashcard Generator (`add_audio_image.py`)
**Purpose**: A multilingual GUI tool to structure word lists into Anki-ready TSV format.

- Reads language configuration from `setting.json`
- Supports:
  - Audio filename mapping
  - Image filename placeholders
  - Automatic ID tracking (`id_info_file`)
  - Word formatting (`reformat_word_list.py`)
- Detects duplicates before proceeding

---




## ⚙️ Configuration Example (`setting.json`)

```json
[
  {
    "name": "English",
    "input_data_file": "input/english.txt",
    "output_data_file": "output/anki_english.tsv",
    "id_info_file": "id_info_english.txt",
    "separator": "|",
    "separator_words": ["example", "test"]
  }
]
```

---



## 📄 License

MIT License

