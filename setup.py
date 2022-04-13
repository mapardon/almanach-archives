import sys
from cx_Freeze import setup, Executable

""" Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

example
{"build_exe": {"packages": ["pygame", "random", "ConfigParser", "sys"],
    "include_files": ["images", "settings.ini", "arialbd.ttf"]}}
"""

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Almanach",
      version="1.4.4",
      description="Almanach autumn release",
      options={"build_exe": {"packages": ["shelve"],
                             "include_files": ["Icons\\", "Fonts\\"]}},
      executables=[Executable("main.py", base=base)])
