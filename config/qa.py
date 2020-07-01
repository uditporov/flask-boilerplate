from config.base import *
from ConfigParser import RawConfigParser


# Path of the project where confidential settings are installed
FILE_PATH = "file path needs to be decide"
config = RawConfigParser()
config.read(FILE_PATH)
DEBUG = False
