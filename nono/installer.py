import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource (for dev and for PyInstaller onefile)"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
