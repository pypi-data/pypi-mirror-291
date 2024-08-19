# This file contains instruction on how to bundle and publish the package.

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="Python_Package_Demo",  # This needs to match folder name.
    version="0.3",  # Needs to be updated if new versions are releases by you.
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        "console_scripts": ["Python-Package-Demo = Python_Package_Demo:hello"]
    },  # This allows the functions of the package to be run from the terminal.
    long_description=description,
    long_description_content_type="text/markdown",
)

# After the above things are done type the following command in the terminal:
# { python setup.py sdist bdist_wheel }

# The command creates 2 distributions:
# ** A source distribution which is generally the python scripts.
# ** And a wheel distribution which contains binaries and are platform specific.

# These archieves will have all the necessary for installing and running the package.

# Rum the command below to test the installation of the package.

# [ pip install dist/Python_Package_Demo-0.1-py3-none-any.whl ]

# Run the command:
# [ twine upload dist/* -u __token__ -p <your-api-token> ]
# This uploads anything in the dist folder to pypi.

# PyPI token - 'pypi-AgEIcHlwaS5vcmcCJGNhOWMzYzdmLWQxOTctNDY0Yi1hMzgxLWJhZDNlZmY1ZTM0ZAACKlszLCJlYTFjMjVlYy00ZGM4LTQ1MTYtYjkxMi04Y2Y2ZDVlMGE1ZjYiXQAABiDdsASiQjYtq-OL2HxHX009Ppj6wMVNfKToALuM2HM_SA'

# Location of package in PyPI - https://pypi.org/project/Python-Package-Demo/0.2/
