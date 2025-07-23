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

## 📂 Directory Structure

```
project/
├── main.py                   # Azure Speech GUI launcher
├── add_audio_image.py        # Flashcard file processor
├── reformat_word_list.py     # Reformatter for raw word lists
├── extract_word_list.py      # Pattern-based extractor
├── check_duplication.py      # Optional duplicate checker
├── setting.json              # Configuration file for each language
├── id_info_file.txt          # Auto-increment ID tracker
├── ico/
│   └── azure.ico             # Icon used in GUI
└── input/, output/           # Working directories
```

---

## 📦 Requirements

Install required libraries:

```bash
pip install PyQt5 openai python-dotenv
```

Other modules used:
- `json`, `shutil`, `re`, `os`, `sys`
- `PIL` (for image conversion if extended)
- Azure SDK (if using speech service integration)

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

## 🧪 Example Flashcard Output

| ID           | Text                          | Audio           | Image           |
|--------------|-------------------------------|------------------|------------------|
| English_1    | Hello<br>world                 | English_1.wav    | English_1.png    |
| English_2    | Nice<br>to<br>meet<br>you      | English_2.wav    | English_2.png    |

---

## 🖥️ How to Launch

### 🔊 Speech Mode Selector:

```bash
python main.py
```

### 🧩 Flashcard Generator:

```bash
python add_audio_image.py
```

---

## ✅ Notes

- Ensure all paths in `setting.json` exist and are valid.
- Placeholders like `.wav` and `.png` can be later filled with real audio/image data.
- Text formatting rules are automatically applied based on language.

---

## 📄 License

MIT License

