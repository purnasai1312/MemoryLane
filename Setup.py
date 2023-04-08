import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os", "time", "datetime", "csv", "json", "requests", "threading", "queue"],
                     "excludes": ["tkinter"],
                     "include_files": ["gps_data.csv", "model.json"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Memory Lane",
      version="1.0",
      description="An app that uses GPS data and machine learning to create a digital map of your life's most important moments, making it easy to revisit them.",
      options={"build_exe": build_exe_options},
      executables=[Executable("memory_lane.py", base=base)])
