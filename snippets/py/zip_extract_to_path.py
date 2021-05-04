import zipfile
from pathlib import Path

def unzip(zip_path, extract_dir_path):
    '''Get a zip path and a directory path to extract to'''
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir_path)