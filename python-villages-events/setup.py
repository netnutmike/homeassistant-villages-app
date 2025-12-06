"""Setup configuration for python-villages-events."""
from setuptools import setup, find_packages

setup(
    name="python-villages-events",
    version="1.1.0",
    author="Mike Myers",
    description="Python library to fetch entertainment events from The Villages, Florida",
    long_description="A simple Python library for fetching entertainment event data from The Villages calendar API.",
    long_description_content_type="text/plain",
    url="https://github.com/netnutmike/python-villages-events",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        "requests>=2.31.0",
    ],
)
