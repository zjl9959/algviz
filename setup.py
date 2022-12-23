#!/usr/bin/env python3

"""

Author: zjl9959@gmail.com

License: GPLv3

"""

from os import path
from setuptools import setup

script_path = path.split(path.realpath(__file__))[0]
readme_filepath = path.join(script_path, 'README.md')
long_description_data = ''
with open(readme_filepath, encoding='utf-8') as f:
    long_description_data = f.read()

setup(
    name="algviz",
    version="0.2.2",
    author="zjl9959",
    author_email="zjl9959@gmail.com",
    description=("An algorithm visualization tool for jupyter notebook to show animation for vector, table, linked list, tree and graph data structures."),
    long_description=long_description_data,
    long_description_content_type="text/markdown",
    license="GPLv3",
    keywords="Algorithm Visualizer Animation Jupyter-notebook Graph",
    url="https://algviz.com/",
    project_urls={
        "Documentation": "https://algviz.readthedocs.io/en/latest/index.html",
        "Issue Tracker": "https://github.com/zjl9959/algviz/issues",
    },
    packages=['algviz'],
    install_requires=[
        'graphviz >= 0.8.4, != 0.18, <= 0.19.1',
        'ipykernel >= 6.4.0, <= 6.7.0'
    ],
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: Visualization",
        'Programming Language :: Python :: 3'
    ],
    zip_safe=False
)
