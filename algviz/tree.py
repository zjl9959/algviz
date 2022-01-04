#!/usr/bin/env python3

'''
@author:zjl9959@gmail.com
@license:GPLv3
'''

from . import utility as util


class TreeNode:
    '''
    @class: The definition of a binary tree node.
    '''

    def __init__(self, val):
        '''
        @param: (val->printable) The label value for binary node(should be printable object).
        '''
        super().__setattr__('val', val)
        super().__setattr__('left', None)
        super().__setattr__('right', None)
        super().__setattr__('_bind_graphs', set())
    

    def __getattribute__(self, name):
        if name == 'val':
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markNode(util._getElemColor, self, hold=False)
            return super().__getattribute__('val')
        elif name == 'left' or name == 'right':
            node = super().__getattribute__(name)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(util._getElemColor, self, node, hold=False)
            return node
        else:
            return super().__getattribute__(name)
    

    def __setattr__(self, name, value):
        if name == 'val':
            super().__setattr__('val', value)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra._updateNodeLabel(self, value)
                gra.markNode(util._setElemColor, self, hold=False)
        elif name == 'left' or name == 'right':
            # Mark old edge(s).
            node = super().__getattribute__(name)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(util._setElemColor, self, node, hold=False)
            # Mark new edge(s).
            super().__setattr__(name, value)
            for gra in bind_graphs:
                gra.addNode(value)
                gra.markEdge(util._setElemColor, self, value, hold=False)
        else:
            super().__setattr__(name, value)
    

    def __str__(self):
        return str(super().__getattribute__('val'))
    

    def _neighbors_(self):
        '''
        @function: Return all children nodes of this node.
        @return: (list(tuple(TreeNode, None))) Return left child node and right child node.
        '''
        left_node = super().__getattribute__('left')
        right_node = super().__getattribute__('right')
        return ((left_node, None), (right_node, None))
    

    def _add_graph_(self, gra):
        '''
        @function: Bind a new SvgGraph object for this TreeNode object.
        @param: (gra->SvgGraph) New SvgGraph object to track.
        '''
        bind_graphs = super().__getattribute__('_bind_graphs')
        bind_graphs.add(gra)
    

    def _remove_graph_(self, gra):
        '''
        @function: Remove one SvgGraph object from this TreeNode object.
        @param: (gra->SvgGraph) SvgGraph object to remove.
        '''
        bind_graphs = super().__getattribute__('_bind_graphs')
        if gra in bind_graphs:
            bind_graphs.remove(gra)


def parseTree(node_vals):
    '''
    @function: Create a new Tree from given node values.
    @param: (node_vals->list(printable)) The label of each node in the tree must be given.
            Empty node is represented by None. eg:([1, None, 2, None, None, 3, 4])
    @return: (TreeNode) Root node object of this tree.
    '''
    if len(node_vals) == 0:
        return None
    root = TreeNode(node_vals[0])
    node_queue = [root]
    index = 1
    while len(node_queue) > 0:
        cur_node = node_queue.pop(0)
        if index >= len(node_vals):
            break
        left_node = None
        if node_vals[index] is not None:
            left_node = TreeNode(node_vals[index])
        node_queue.append(left_node)
        if index+1 >= len(node_vals):
            break
        left_right = None
        if node_vals[index+1] is not None:
            right_node = TreeNode(node_vals[index+1])
        node_queue.append(right_node)
        if cur_node is not None:
            cur_node.left = left_node
            cur_node.right = right_node
        index += 2
    return root
