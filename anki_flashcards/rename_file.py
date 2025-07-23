import os
import re


def increment_audio_file(n, folder_path):
    for filename in os.listdir(folder_path):
        match = re.match(r"^(.*?)_(\d+)\.", filename)
        if match:
            number = int(match.group(2))
            new_name = f"{match.group(1)}_{number + n}.wav"
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)

            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_name}")



if __name__ == "__main__":
    n = int(input("Enter the number to increase: "))
    folder_path = input("Enter the folder path: ").strip("\"")
    increment_audio_file(n, folder_path)
