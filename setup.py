from setuptools import setup

APP = ['main.py']  # Your main application script
DATA_FILES = ['duck.gif']  # Include your GIF and other data files
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PIL'],  # Include required packages
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)