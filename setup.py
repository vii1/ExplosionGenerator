from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': [],
    'excludes': [],
    'optimize': 1,
    'include_files': [
        ('locale/', 'locale/'),
        ('explo/img/', 'img/'),
    ],
    'include_msvcr': True,
    'zip_include_packages': [
        'cffi',
        'cffi-1.14.1.dist-info',
        'collections',
        'concurrent',
        'ctypes',
        'curses',
        'distutils',
        'email',
        'encodings',
        'explo',
        'html',
        'http',
        'importlib',
        'json',
        'lib2to3',
        'logging',
        'multiprocessing',
        'numpy',
        'numpy-1.19.1.dist-info',
        'pkg_resources',
        'pycparser',
        'pycparser-2.20.dist-info',
        'pydoc_data',
        'setuptools',
        'setuptools-46.4.0.dist-info',
        'unittest',
        'urllib',
        'win32com',
        'wx',
        'xml',
        'xmlrpc',
    ],
}

base = 'Win32GUI'

executables = [
    Executable('explo.py', base=base,
               icon='explo.ico',
               targetName='ExplosionGenerator'
               )
]

setup(name='explo',
      version='1.0',
      description='Explosion Generator',
      options={'build_exe': build_options},
      executables=executables)
