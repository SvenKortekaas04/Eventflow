from eventflow.version import __version__
from setuptools import setup

NAME = "Eventflow"
VERSION = __version__
DESCRIPTION = "Eventflow provides functionalities for event-based applications."
AUTHOR = "Sven Kortekaas"
URL = "https://github.com/SvenKortekaas04/Eventflow"
LICENSE = "MIT License"
REQUIRES_PYTHON = ">=3.6.0"

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()


setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    url=URL,
    license=LICENSE,
    python_requires=REQUIRES_PYTHON
)
