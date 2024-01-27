import pickle
import os

directory_path = "/home/mr-jz/Nextcloud/Documents/hsos-osnabrueck/Semester_7/IT-Sicherheit/Vorlesung/"

# List all files and directories in the specified path
files_and_directories = os.listdir(directory_path)

files = [
    f for f in files_and_directories if os.path.isfile(os.path.join(directory_path, f))
]

with open("list_of_files.pkl", "wb") as file:
    pickle.dump(files, file)
