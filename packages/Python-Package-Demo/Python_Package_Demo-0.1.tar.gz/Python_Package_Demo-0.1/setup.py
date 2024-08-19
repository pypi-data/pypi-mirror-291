# This file contains instruction on how to bundle and publish the package.

from setuptools import setup, find_packages

setup(
    name="Python_Package_Demo",  # This needs to match folder name.
    version="0.1",  # Needs to be updated if new versions are releases by you.
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
)

# After the above things are done type the following command in the terminal:
# { python setup.py sdist bdist_wheel }

# The command creates 2 distributions:
# ** A source distribution which is generally the python scripts.
# ** And a wheel distribution which contains binaries and are platform specific.

# These archieves will have all the necessary for installing and running the package.
