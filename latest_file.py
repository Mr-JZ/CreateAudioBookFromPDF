import os
import re


def find_latest_file(folder_path):
    # List of all files in the directory
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    if not files:
        print("No files found in the folder.")
        return

    # Finding the latest file
    latest_file = max(files, key=os.path.getctime)
    latest_file = os.path.basename(latest_file)
    numbers = re.findall(r"\d+", latest_file)
    integer_values = [int(num) for num in numbers]
    print(integer_values[0])
    print(f"The latest created file is: {latest_file}")


# Replace 'your_folder_path_here' with your folder path
folder_path = "/home/mr-jz/github/CreateAudioBookFromPDF/audio"
find_latest_file(folder_path)
