import os
import pathlib
import shutil


class File:
    def __init__(self):
        pass

    @classmethod
    def get_filenames(cls, target_dir_path, contain_subdir=False):
        p_temp = pathlib.Path(target_dir_path)
        extensions = os.environ['TARGET_EXT'].split('|')
        target_glob = '*.*'
        if contain_subdir:
            target_glob = '**/' + target_glob
        return [i for i in p_temp.glob(target_glob) if i.suffix in extensions]

    @classmethod
    def get_containing_dirname(cls, target_file_path):
        return os.path.basename(os.path.dirname(target_file_path))

    @classmethod
    def extract_filename(cls, filepath):
        return os.path.splitext(os.path.basename(filepath))[0]

    @classmethod
    def move_file(cls, target_filepath, dest_path, message):
        os.makedirs(dest_path, exist_ok=True)
        shutil.move(target_filepath, dest_path)
        print(message + ': ' + str(target_filepath))

    @classmethod
    def count_files(cls, target_dir_path, contain_subdir=False):
        return len(cls.get_filenames(target_dir_path, contain_subdir))

    @classmethod
    def count_files_in_dest_folder(cls):
        dest_dir_files_count = cls.count_files(os.environ['SORTED_FOLDER'], True) +\
            cls.count_files(os.environ['UNIDENTIFIED_FOLDER'], True) +\
            cls.count_files(os.environ['THRESHOLD_FOLDER'], True)

        return dest_dir_files_count
