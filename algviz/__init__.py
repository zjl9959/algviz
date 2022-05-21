#!/usr/bin/env python3

"""Algorithm visualization animation library.

algviz is an algorithm visualization library for jupyter notebook.
This module can automatic generate visualize animations for
vector, table, list, tree and graph data structures in your code.

Author: zjl9959@gmail.com

License: GPLv3

"""

from .visual import Visualizer
from .graph import GraphNode, parseGraph, updateGraphEdge
from .tree import BinaryTreeNode, TreeNode, parseBinaryTree, parseTree
from .linked_list import ForwardLinkedListNode, DoublyLinkedListNode
from .linked_list import parseForwardLinkedList, parseDoublyLinkedList
from .utility import _version, AlgvizParamError, AlgvizRuntimeError, AlgvizFatalError


colors = {
    0: (221, 160, 221), # Plum
    1: (0, 255, 255),   # Aqua
    2: (210, 180, 140), # Tan
    3: (135, 206, 250), # LightSkyBlue
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'green': (0, 128, 0),
    'lime': (0, 255, 0),
    'gold': (255, 215, 0),
    'pink': (255, 192, 203),
    'orchild': (218, 112, 214),
    'tomato': (255, 99, 71),
    'wheat': (245, 222, 179),
    'gray': (128, 128, 128),
    'silver': (192, 192, 192),
    'black': (0, 0, 0),
    'white': (255, 255, 255)
}


def colorsInfo():
    """Display all the default colors name and background color in a vector.
    """
    viz = Visualizer()
    c = 6
    r = len(colors) // c
    tab = viz.createTable(r, c, cell_size=50, name='ColorsInfo', show_index=False)
    count = 0
    for k in colors.keys():
        tab[(count//c, count%c)] = k
        tab.mark((count//c, count%c), colors[k])
        count += 1
    viz.display()


__all__ = [
    'Visualizer',
    'GraphNode', 'parseGraph', 'updateGraphEdge',
    'BinaryTreeNode', 'TreeNode', 'parseBinaryTree', 'parseTree',
    'ForwardLinkedListNode', 'DoublyLinkedListNode',
    'parseForwardLinkedList', 'parseDoublyLinkedList',
    'colors', 'colorsInfo', 'AlgvizParamError', 'AlgvizRuntimeError', 'AlgvizFatalError'
]


__title__ = 'algviz'
__version__ = _version
__author__ = 'zjl9959@gmail.com'
__license__ = 'GNU General Public License (GPLv3)'
