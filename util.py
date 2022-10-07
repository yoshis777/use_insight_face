import os
import re
import numpy


class Util:
    def __init__(self):
        pass

    @classmethod
    def get_max_index(cls, target_list):
        return numpy.argmax(target_list)

    @classmethod
    def delete_filename_num(cls, filename):
        m = re.search(r'(?P<FILENAME>.*)\(\d+\)', filename)
        if m is None:
            return filename
        else:
            return m.group('FILENAME').rstrip()

