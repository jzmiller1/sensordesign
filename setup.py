from distutils.core import setup
import glob, os
import py2exe

# Matplotlib
import matplotlib as mpl
data_files = mpl.get_py2exe_datafiles()

setup(console=['sensordesign.py'],
      options={'py2exe': {'bundle_files': 3, 'compressed': True,
                          "dll_excludes": ["MSVCP90.dll"],
                          'packages': ['FileDialog',],
                          'includes': ['numpy', 'numpy.*', 'numpy.core', "matplotlib.backends.backend_tkagg"]}},
      zipfile=None,
      data_files=data_files)

