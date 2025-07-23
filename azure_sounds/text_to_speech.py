import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load API key and region from .env
load_dotenv()
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_REGION")


class SpeechSynthApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Azure Text-to-Speech Generator")
        self.setGeometry(100, 100, 600, 400)
        self.ID = 0
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Language Selection
        self.lang_combo = QtWidgets.QComboBox()
        self.lang_combo.addItems(["EN", "DE", "JA"])
        layout.addWidget(QtWidgets.QLabel("Select Language:"))
        layout.addWidget(self.lang_combo)

        # Output folder
        self.folder_btn = QtWidgets.QPushButton("Select Output Folder")
        self.folder_btn.clicked.connect(self.select_folder)
        self.folder_path_label = QtWidgets.QLabel("No folder selected")
        layout.addWidget(self.folder_btn)
        layout.addWidget(self.folder_path_label)

        # Input Text
        self.text_input = QtWidgets.QTextEdit()
        self.text_input.setPlaceholderText("Enter text separated by '|'")
        layout.addWidget(QtWidgets.QLabel("Input Text:"))
        layout.addWidget(self.text_input)

        # Synthesize Button
        self.start_btn = QtWidgets.QPushButton("Start Synthesis")
        self.start_btn.clicked.connect(self.synthesize)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.folder_path = folder
            self.folder_path_label.setText(folder)

    def synthesize(self):
        language = self.lang_combo.currentText()
        content = self.text_input.toPlainText()
        separator = "|"
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

        if language == "DE":
            speech_config.speech_synthesis_voice_name = "de-DE-SeraphinaMultilingualNeural"
        elif language == "EN":
            speech_config.speech_synthesis_voice_name = "en-US-AvaMultilingualNeural"
        elif language == "JA":
            speech_config.speech_synthesis_voice_name = "ja-JP-AoiNeural"
        else:
            QMessageBox.critical(self, "Error", f"Unsupported language code: {language}")
            return

        segments = content.split(separator)
        success_count = 0

        for idx, segment in enumerate(segments):
            output_filename = f"{language}_{idx}.wav"
            output_path = os.path.join(output_folder, output_filename)

            audio_config = speechsdk.audio.AudioConfig(filename=output_path)
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            result = speech_synthesizer.speak_text_async(segment.strip()).get()

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
    sys.exit(app.exec_())
