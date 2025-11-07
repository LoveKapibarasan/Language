import os
import sys
import json
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load API key, region, and separator from .env
load_dotenv()
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_REGION")
separator = os.getenv("SEPARATOR", "|")  # Default to "|" if not set


class SpeechSynthApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Azure Text-to-Speech Generator")
        self.setGeometry(100, 100, 600, 400)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(__file__), "ico", "azure.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Set default output folder
        self.default_folder = os.path.join(os.path.dirname(__file__), "output")
        self.folder_path = self.default_folder
        
        # Create default folder if it doesn't exist
        os.makedirs(self.default_folder, exist_ok=True)
        
        self.ID = 0
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Language Selection
        self.lang_combo = QtWidgets.QComboBox()
        
        # Load available languages from voice.json
        voice_config_path = os.path.join(os.path.dirname(__file__), "setting", "voice.json")
        try:
            with open(voice_config_path, 'r', encoding='utf-8') as f:
                voice_config = json.load(f)
            languages = list(voice_config.keys())
            self.lang_combo.addItems(languages)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Fallback to default languages if config file is not available
            self.lang_combo.addItems(["EN"])
            print(f"Warning: Could not load voice config, using defaults. Error: {e}")
        
        layout.addWidget(QtWidgets.QLabel("Select Language:"))
        layout.addWidget(self.lang_combo)

        # Output folder
        self.folder_btn = QtWidgets.QPushButton("Select Output Folder")
        self.folder_btn.clicked.connect(self.select_folder)
        self.folder_path_label = QtWidgets.QLabel(self.folder_path)
        layout.addWidget(self.folder_btn)
        layout.addWidget(self.folder_path_label)

        # Input Text
        self.text_input = QtWidgets.QTextEdit()
        self.text_input.setPlaceholderText(f"Enter text separated by '{separator}'")
        layout.addWidget(QtWidgets.QLabel("Input Text:"))
        layout.addWidget(self.text_input)

        # Synthesize Button
        self.start_btn = QtWidgets.QPushButton("Start Synthesis")
        self.start_btn.clicked.connect(self.synthesize)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", self.folder_path)
        if folder:
            self.folder_path = folder
            # Create the folder if it doesn't exist
            os.makedirs(self.folder_path, exist_ok=True)
            self.folder_path_label.setText(folder)

    def synthesize(self):
        language = self.lang_combo.currentText()
        content = self.text_input.toPlainText()
        output_folder = getattr(self, "folder_path", None)

        if not output_folder or not os.path.isdir(output_folder):
            QMessageBox.warning(self, "Warning", "Please select a valid output folder.")
            return

        if not content.strip():
            QMessageBox.warning(self, "Warning", "Input text cannot be empty.")
            return

        os.makedirs(output_folder, exist_ok=True)

        # Configure voice based on language
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        # Load voice configuration from JSON file
        voice_config_path = os.path.join(os.path.dirname(__file__), "setting", "voice.json")
        try:
            with open(voice_config_path, 'r', encoding='utf-8') as f:
                voice_config = json.load(f)
            
            if language in voice_config:
                speech_config.speech_synthesis_voice_name = voice_config[language]
            else:
                QMessageBox.critical(self, "Error", f"Unsupported language code: {language}")
                return
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"Voice configuration file not found: {voice_config_path}")
            return
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Invalid JSON format in voice configuration file.")
            return

        segments = content.split(separator)
        success_count = 0

        for idx, segment in enumerate(segments):
            output_filename = f"{language}_{idx}.wav"
            output_path = os.path.join(output_folder, output_filename)

            # First synthesize and save to file
            audio_config_file = speechsdk.audio.AudioConfig(filename=output_path)
            speech_synthesizer_file = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config_file)
            result_file = speech_synthesizer_file.speak_text_async(segment.strip()).get()

            # Then play the audio (synthesize again for playback)
            if result_file.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                audio_config_speaker = speechsdk.audio.AudioConfig(use_default_speaker=True)
                speech_synthesizer_speaker = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config_speaker)
                result_speaker = speech_synthesizer_speaker.speak_text_async(segment.strip()).get()
                
                result = result_file  # Use file result for error checking
            else:
                result = result_file

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                success_count += 1
            else:
                error_msg = f"Failed to synthesize segment {idx}"
                if result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    error_msg += f": {cancellation_details.reason} - {cancellation_details.error_details}"
                QMessageBox.warning(self, "Synthesis Error", error_msg)

        QMessageBox.information(self, "Done", f"Synthesized {success_count} segments.")




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SpeechSynthApp()
    window.show()
    sys.exit(app.exec())
