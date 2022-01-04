#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from .visual import Visualizer
from .graph import GraphNode, parseGraph, updateEdgeWeight
from .tree import TreeNode, parseTree
from .link_list import ListNode, parseLinkList

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
    'GraphNode', 'parseGraph', 'updateEdgeWeight',
    'TreeNode', 'parseTree',
    'ListNode', 'parseLinkList',
    'colors', 'colorsInfo',
]

__title__ = 'algviz'
__version__ = '1.0.0'
__author__ = 'zjl9959@gmail.com'
__license__ = 'GNU General Public License (GPLv3)'
