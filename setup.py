#!/usr/bin/env python3

"""

Author: zjl9959@gmail.com

License: GPLv3

"""

from setuptools import setup

setup(
    name="algviz",
    version="0.1.0",
    author="zjl",
    author_email="zjl9959@gmail.com",
    description=("This is a algorithm visualizer lib."),
    license="GPLv3",
    keywords="Algorithm Visualizer Animation",
    url="https://github.com/zjl9959/algviz",
    packages=['algviz'],
    install_requires=[
        'graphviz>=0.5.1',
        'ipykernel>=4.0.1'
    ],
    python_requires='>=3',
    classifiers=[
        "Development Status :: Alpha",
        "Topic :: Visualization Tool",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False
)
