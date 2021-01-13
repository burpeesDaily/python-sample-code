"""Setup file for the Sphinx example."""

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="sphinx-example",
    version="0.1.1",
    description="An example for Sphinx",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/shunsvineyard/sphinx-example",
    author="Shun Huang",
    author_email="zsh@shunsvineyard.info",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python"
    ],
    keywords="sphinx",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "sample-cli=trees.bin.tree_cli:main"
        ]
    },
    python_requires=">=3.7"
)
