import os
import zipfile


def zip_folder(source_folder, zip_name, zip_save_folder='.temp'):
    os.makedirs(zip_save_folder, exist_ok=True)
    zip_file_path = os.path.join(zip_save_folder, zip_name)
    zip_file = zipfile.ZipFile(zip_file_path, mode='w')
    for path, _, filenames in os.walk(source_folder):

        fpath = path.replace(source_folder, '')

        for filename in filenames:
            zip_file.write(os.path.join(path, filename),
                           os.path.join(fpath, filename))

    zip_file.close()
    return zip_file_path
