import os
import zipfile


def zip_folder(source_folder, zip_name, zip_save_folder='.temp'):
    os.makedirs(zip_save_folder, exist_ok=True)
    zip_file_path = os.path.join(zip_save_folder, zip_name)
    zip_file = zipfile.ZipFile(zip_file_path, mode='w')
    zip_file.write(source_folder)
    zip_file.close()
    return zip_file_path
