import cx_Freeze
import sys
import os
from tkinter import *
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"C:\Users\DELL\AppData\Local\Programs\Python\Python381\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\DELL\AppData\Local\Programs\Python\Python381\tcl\tk8.6"

executables = [cx_Freeze.Executable("Inventory Management.py", base=base, icon="icon.ico")]


cx_Freeze.setup(
    name = "Inventory System",
    options = {"build_exe": {"packages":["tkinter","os"], "include_files":['icon.ico','tcl86t.dll','tk86t.dll', 'gne.png' ,'gndpcstock.sql','project_icon.jpg','.idea','__pycache__']}},
    version = "0.01",
    description = "Tkinter Application",
    executables = executables
    )
# run on CMD = python setup.py bdist_msi