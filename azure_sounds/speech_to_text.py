import os
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load Azure credentials from .env
load_dotenv()
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_REGION")


class SpeechRecognitionApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Azure Speech-to-Text (Audio File)")
        self.setGeometry(100, 100, 600, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Language selection
        self.lang_combo = QtWidgets.QComboBox()
        self.lang_combo.addItems(["EN", "DE", "JP"])
        layout.addWidget(QtWidgets.QLabel("Select Language:"))
        layout.addWidget(self.lang_combo)

        # Input audio file
        self.audio_btn = QtWidgets.QPushButton("Select Audio File")
        self.audio_btn.clicked.connect(self.select_audio_file)
        self.audio_path_label = QtWidgets.QLabel("No file selected")
        layout.addWidget(self.audio_btn)
        layout.addWidget(self.audio_path_label)

        # Output text file
        self.output_btn = QtWidgets.QPushButton("Select Output File Path")
        self.output_btn.clicked.connect(self.select_output_file)
        self.output_path_label = QtWidgets.QLabel("No output path selected")
        layout.addWidget(self.output_btn)
        layout.addWidget(self.output_path_label)

        # Start recognition
        self.start_btn = QtWidgets.QPushButton("Start Recognition")
        self.start_btn.clicked.connect(self.recognize_speech)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

    def select_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav *.mp3 *.mp4)")
        if file_path:
            self.audio_path = file_path
            self.audio_path_label.setText(file_path)

    def select_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "Text Files (*.txt)")
        if file_path:
            self.output_path = file_path
            self.output_path_label.setText(file_path)

    def recognize_speech(self):
        if not hasattr(self, "audio_path") or not os.path.isfile(self.audio_path):
            QMessageBox.warning(self, "Warning", "Please select a valid audio file.")
            return

        if not hasattr(self, "output_path"):
            QMessageBox.warning(self, "Warning", "Please select a valid output file path.")
            return

        language_code = self.lang_combo.currentText()
        if language_code == "EN":
            lang = "en-US"
        elif language_code == "DE":
            lang = "de-DE"
        elif language_code == "JP":
            lang = "ja-JP"
        else:
            QMessageBox.critical(self, "Error", "Unsupported language selected.")
            return

        try:
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
            speech_config.speech_recognition_language = lang

            audio_input = speechsdk.AudioConfig(filename=self.audio_path)
            recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

            print("Recognizing...")
            result = recognizer.recognize_once()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                with open(self.output_path, "w", encoding="utf-8") as f:
                    f.write(result.text)
                QMessageBox.information(self, "Success", "Recognition complete.\nOutput saved.")
            elif result.reason == speechsdk.ResultReason.NoMatch:
                QMessageBox.warning(self, "No Match", "No speech could be recognized.")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                error_msg = f"Recognition canceled: {cancellation.reason}"
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    error_msg += f"\nDetails: {cancellation.error_details}"
                QMessageBox.critical(self, "Error", error_msg)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SpeechRecognitionApp()
    window.show()
    sys.exit(app.exec_())
