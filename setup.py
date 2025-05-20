from setuptools import setup
from theophanie_utils.metadata.__version__ import __version__

setup(
    name='theophanie_utils',
    packages=['theophanie_utils'],
    description='Some utils (starting the app, ...) for the Theophanie Project',
    version='1.2.2',  # updated
    url='https://github.com/Pier4413/PythonUtils',
    author='Panda',
    author_email='panda@delmasweb.net',
    install_requires=[
        'python-dotenv',
        'logger',
        'settings'
    ],
    keywords=['theophanie']
)
