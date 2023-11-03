import os

# __file__ is a special variable that holds the path to the current file.
# os.path.realpath() will resolve any symbolic links to the actual file path.
# os.path.dirname() will give you the directory that the file is in.
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))