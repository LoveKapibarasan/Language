# 🎙️ Speech & Flashcard Utility Suite


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
### 🧑‍💻 3. Google TTS Utility (`google_tts_module.py`)

**Purpose**: Provides a minimal interface for generating speech using **Google Text-to-Speech** (`gTTS`).



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

