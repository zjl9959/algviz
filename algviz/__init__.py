#!/usr/bin/env python3

"""Algviz is an algorithm visualization tool for your Python code.

Algviz can generate visual animations for
vector, table, linked list, tree, and graph data structures.
You can bring alive animations in your notebook after
inserting a few algviz interfaces into code. 

Author: zjl9959@gmail.com

License: GPLv3

"""

from .visual import Visualizer
from .graph import GraphNode, parseGraph, updateGraphEdge
from .tree import BinaryTreeNode, TreeNode, parseBinaryTree, parseTree
from .linked_list import ForwardLinkedListNode, DoublyLinkedListNode
from .linked_list import parseForwardLinkedList, parseDoublyLinkedList
from .utility import _version, AlgvizParamError, AlgvizRuntimeError, AlgvizFatalError, AlgvizTypeError


# Common colors name to RGB map (see: https://www.w3schools.com/tags/ref_colornames.asp)
color_aqua = (0, 255, 255)
color_black = (0, 0, 0)
color_blue = (0, 0, 255)
color_brown = (165, 42, 42)
color_dark_blue = (0, 0, 139)
color_dark_green = (0, 100, 0)
color_dark_red = (139, 0, 0)
color_gold = (255, 215, 0)
color_gray = (128, 128, 128)
color_green = (0, 128, 0)
color_green_yellow = (173, 255, 47)
color_light_blue = (173, 216, 230)
color_lime = (0, 255, 0)
color_orange = (255, 165, 0)
color_pink = (255, 192, 203)
color_plum = (221, 160, 221)
color_purple = (128, 0, 128)
color_red = (255, 0, 0)
color_silver = (192, 192, 192)
color_slate_blue = (106, 90, 205)
color_spring_green = (0, 255, 127)
color_tan = (210, 180, 140)
color_tomato = (255, 99, 71)
color_violet = (238, 130, 238)
color_wheat = (245, 222, 179)
color_white = (255, 255, 255)
color_yellow = (255, 255, 0)


__all__ = [
    'Visualizer',
    'GraphNode', 'parseGraph', 'updateGraphEdge',
    'BinaryTreeNode', 'TreeNode', 'parseBinaryTree', 'parseTree',
    'ForwardLinkedListNode', 'DoublyLinkedListNode',
    'parseForwardLinkedList', 'parseDoublyLinkedList',
    'AlgvizParamError', 'AlgvizRuntimeError', 'AlgvizFatalError', 'AlgvizTypeError'
]


__title__ = 'algviz'
__version__ = _version
__author__ = 'zjl9959@gmail.com'
__license__ = 'GNU General Public License (GPLv3)'
