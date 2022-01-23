#!/usr/bin/env python3

"""

Author: zjl9959@gmail.com

License: GPLv3

"""

from setuptools import setup

setup(
    name="algviz",
    version="0.1.0",
    author="zjl9959",
    author_email="zjl9959@gmail.com",
    description=("An algorithm visualization tool for jupyter notebook to show animation for vector, table, linked list, tree and graph data structures."),
    license="GPLv3",
    keywords="Algorithm Visualizer Animation Jupyter-notebook Graph",
    url="https://github.com/zjl9959/algviz",
    packages=['algviz'],
    install_requires=[
        'graphviz >= 0.8.4, != 0.18, <= 0.19.1',
        'ipykernel >= 6.4.0, <= 6.7.0'
    ],
    python_requires='>=3.7, <=3.10',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: Visualization",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    zip_safe=False
)
