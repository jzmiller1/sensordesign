import os

try:
    BASE_DIR = os.path.dirname(__file__)
except NameError:
    import sys
    BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
