import os
import sys


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
