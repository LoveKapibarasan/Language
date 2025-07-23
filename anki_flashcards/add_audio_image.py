import sys
import json
import shutil
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QComboBox, QMessageBox
)

from check_duplication import check_duplication
from reformat_word_list import reformat

separator = "|"


def find_start(lines):
    start_index = 0
    for i in range(len(lines)):
        if lines[i].startswith("<start>"):
            start_index = i + 1
            break
    return start_index


class FlashcardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard Processor")
        self.setWindowIcon(QIcon("ico/anki_flashcards.ico"))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Select Language:")
        self.layout.addWidget(self.label)

        self.language_select = QComboBox()
        self.layout.addWidget(self.language_select)

        self.process_button = QPushButton("Process Files")
        self.process_button.clicked.connect(self.process_files)
        self.layout.addWidget(self.process_button)

        self.load_settings()

    def load_settings(self):
        with open("setting.json", "r", encoding="utf-8") as f:
            self.settings = json.load(f)
            for entry in self.settings:
                self.language_select.addItem(entry["name"])

    def process_files(self):
        selected_lang = self.language_select.currentText()
        config = next((x for x in self.settings if x["name"] == selected_lang), None)

        if not config:
            QMessageBox.critical(self, "Error", "Configuration not found.")
            return

        try:
            input_path = config["input_data_file"]
            output_path = config["output_data_file"]
            info_path = config["id_info_file"]

            # Back up for safety
            backup_path = input_path + ".bak"  # 例: original.txt → original.txt.bak
            shutil.copy(input_path, backup_path)

            with open(info_path, "r", encoding="utf-8") as f:
                ID = int(f.read().strip())

            with open(input_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            # reformat
            reformat()


            index = find_start(lines)
            result1 = []
            result2 = []
            # for result 1
            for i in range(len(lines[:index - 1] + lines[index:])): # remove index - 1
                if "<start>" in lines[i]:
                    raise Exception("index is wrong at result 1")
                line = lines[i]
                new_line = f"{selected_lang}_{i}{separator}{line}{separator}{selected_lang}_{i}.wav{separator}{selected_lang}_{i}.png"
                result1.append(new_line)

            # for result 2
            for line in lines[index:]:
                if "<start>" in line:
                    raise Exception("index is wrong at result 2")
                if not line.strip():
                    continue
                ID += 1
                text = line.split(separator)[1]
                cleaned_text = text.replace("<br>", ".")
                result2.append(f"{cleaned_text}{separator}\n")

            with open(info_path, "w", encoding="utf-8") as fi:
                fi.write(str(ID))

            with open(input_path, "w", encoding="utf-8") as f0:
                f0.write("\n".join(lines).replace("<start>", "") + "\n<start>")

            with open(output_path, "w", encoding="utf-8") as f1:
                f1.write("\n".join(result1))

            temp_txt_file_path, _ = QFileDialog.getSaveFileName(self, "Save Temp Text File", "", "Text Files (*.txt)")
            if temp_txt_file_path:
                with open(temp_txt_file_path, "w", encoding="utf-8") as f2:
                    f2.write("\n".join(result2))

            QMessageBox.information(self, "Success", "Files processed successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    check_duplication()
    app = QApplication(sys.argv)
    window = FlashcardApp()
    window.resize(400, 200)
    window.show()
    sys.exit(app.exec())
