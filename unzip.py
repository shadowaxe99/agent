import os
import zipfile

# File path
zip_file_path = "/mnt/data/untitled folder 5.zip"

# Unzip
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall("/mnt/data/")

# List contents of the unzipped folder
unzipped_folder_path = zip_file_path.replace(".zip", "")
os.listdir(unzipped_folder_path)