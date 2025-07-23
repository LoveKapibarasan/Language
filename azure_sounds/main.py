import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from text_to_speech import SpeechSynthApp
from speech_to_text import SpeechRecognitionApp

class ModeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Azure Speech: Mode Selection")
        self.setWindowIcon(QIcon("ico/azure.ico"))
        self.setGeometry(100, 100, 300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Select Mode:")
        layout.addWidget(label)

        # Text-to-Speech
        self.tts_button = QPushButton("Text to Speech (TTS)")
        self.tts_button.clicked.connect(self.launch_tts)
        layout.addWidget(self.tts_button)

        # Speech-to-Text
        self.stt_button = QPushButton("Speech to Text (STT)")
        self.stt_button.clicked.connect(self.launch_stt)
        layout.addWidget(self.stt_button)

        self.setLayout(layout)

    def launch_tts(self):
        self.tts_window = SpeechSynthApp()
        self.tts_window.show()

    def launch_stt(self):
        self.stt_window = SpeechRecognitionApp()
        self.stt_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = ModeSelector()
    selector.show()
    sys.exit(app.exec_())
