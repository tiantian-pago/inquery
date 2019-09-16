from setuptools import setup

setup(
    name='ticktes',
    py_modules=['ticktes', 'station'],
    install_requires=['requests', 'docopt', 'prettytable', 'colorama'],
    entry_points={
        'console_scripts': ['ticktes=ticktes:cli']
    }
)
