from setuptools import setup

setup(
    name='theophanie_utils',
    packages=['theophanie_utils'],
    description='Some utils (starting the app, ...) for the Theophanie Project',
    version='1.0.1',  # updated
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
