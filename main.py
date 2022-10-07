import os

from dotenv import load_dotenv

from file import File
from recognizer import Recognizer


def main():
    load_dotenv()

    print('対象フォルダ格納ファイル数: ' + str(len(File.get_filenames(os.path.join(os.environ['UNKNOWN_FOLDER'], os.environ['TARGET_EXT'])))))
    print('移動前ファイル数: ' + str(File.count_files_in_dest_folder()))
    recognizer = Recognizer()
    recognizer.compare()
    print('移動後ファイル数: ' + str(File.count_files_in_dest_folder()))
    print('残り対象フォルダ格納ファイル数: ' + str(len(File.get_filenames(os.path.join(os.environ['UNKNOWN_FOLDER'], os.environ['TARGET_EXT'])))))

main()











