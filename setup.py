from distutils.core import setup
import glob, os
import py2exe

# Matplotlib
import matplotlib as mpl
data_files = mpl.get_py2exe_datafiles()

#TEMP MKL HACK
folder = r'C:\Users\zmiller\AppData\Local\Enthought\Canopy\App\appdata\canopy-1.3.0.1715.win-x86_64\Scripts'
data_files.append((r'numpy/linalg', glob.glob(os.path.join(folder,'*mk2*.dll'))))
data_files.append((r'numpy/linalg', [r'C:\Users\zmiller\AppData\Local\Enthought\Canopy\User\Lib\site-packages\matplotlib\backends\msvcr90.dll']))

setup(console=['sensordesign5.py'],
      options={'py2exe': {'bundle_files': 3, 'compressed': True,
                          "dll_excludes": ["MSVCP90.dll"],
                          'includes': ['pylab', 'scipy', 'numpy', 'numpy.linalg', 'numpy.*', 'numpy.core']}},
      zipfile=None,
      data_files=data_files)

