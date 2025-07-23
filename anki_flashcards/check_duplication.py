import json
import os

def check_duplication(setting_file="setting.json"):
    with open(setting_file, "r", encoding="utf-8") as f:
        settings = json.load(f)

    has_error = False
    for config in settings:
        lang = config["name"]
        word_file = config["word_data"]

        if not os.path.exists(word_file):
            print(f"[ERROR] Word data file not found for {lang}: {word_file}")
            has_error = True
            continue

        with open(word_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        word_set = set()
        duplicates = set()

        for word in lines:
            if word in word_set:
                duplicates.add(word)
            else:
                word_set.add(word)

        if duplicates:
            has_error = True
            print(f"\n[❌ Duplicate Found] Language: {lang}")
            print(f"File: {word_file}")
            for dup in sorted(duplicates):
                print(f"  - {dup}")
        else:
            print(f"[✔️ OK] No duplicates in {lang} word file.")

    if has_error:
        print("\n🚫 Duplication check failed. Please fix the issues above.")
    else:
        print("\n✅ All files passed duplication check.")

if __name__ == "__main__":
    check_duplication()