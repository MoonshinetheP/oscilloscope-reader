from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'oscilloscope-reader',
    version = '1.0.0',
    author = 'Steven Linfield',
    author_email = 'S.Linfield@outlook.com',
    description = 'Open oscilloscope files and observe analogue current in cyclic staircase voltammetry',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    url = 'https://github.com/MoonshinetheP/oscilloscope-reader',
    keywords = 'Electrochemistry',
    python_requires = ">=3.9",
    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis"],
    install_requires = ['numpy','pandas','matplotlib'],
)
