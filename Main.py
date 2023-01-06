'''
    pip freeze > requirements.txt
    pyi-makespec --onefile Main.py
    pyinstaller Main.spec
'''
import sys
import os

from GUI import *


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


if __name__ == '__main__':
    ico = resource_path(os.path.join('data', 'flaticon.ico'))
    sg.set_global_icon(ico)
    main_window()


