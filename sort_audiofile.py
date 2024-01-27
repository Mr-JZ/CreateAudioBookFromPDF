import os

folder_path = "/home/mr-jz/Nextcloud/Music/hsos/it-sicherheit/Audiobook/"
files = sorted(os.listdir(folder_path))

for index, file in enumerate(files):
    if file.endswith(".wav"):
        new_name = f"Track_{index:03d}.wav"  # Formats the number with leading zeros
        os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))
