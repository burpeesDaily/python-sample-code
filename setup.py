"""Setup file for the Sphinx example."""

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="python-sample-code",
    version="0.0.1",
    description="The Python sample project is a Binary Tree Library",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/shunsvineyard/python-sample-code",
    author="Shun Huang",
    author_email="zsh@shunsvineyard.info",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
    keywords="sphinx",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["tree-cli=trees.bin.tree_cli:main"]},
    python_requires=">=3.7",
)
