#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from . import graph_node_base
NodeBase = graph_node_base.GraphNodeBase


class BinaryTreeNode(NodeBase):
    '''
    @class: The definition of a binary tree node.
    '''

    def __init__(self, val):
        '''
        @param: {val->printable} The label value for binary node(should be printable object).
        '''
        super().__init__(val)
        super().__setattr__('left', None)
        super().__setattr__('right', None)
    

    def __getattribute__(self, name):
        if name == 'left' or name == 'right':
            node = super().__getattribute__(name)
            self._on_visit_neighbor_(node)
            return node
        else:
            return super().__getattribute__(name)
    

    def __setattr__(self, name, value):
        if name == 'left' or name == 'right':
            old_node = super().__getattribute__(name)
            super().__setattr__(name, value)
            self._on_update_neighbor_(old_node, value)
        else:
            super().__setattr__(name, value)


    def _neighbors_(self):
        '''
        @function: Return all children nodes of this tree node.
        @return: {list(tuple(BinaryTreeNode, None))} Return left child node and right child node.
        '''
        left_node = super().__getattribute__('left')
        right_node = super().__getattribute__('right')
        return [(left_node, None), (right_node, None)]


def parseBinaryTree(node_vals):
    '''
    @function: Create a new Tree from given node values.
    @param: {node_vals->list(printable)} The label of each node in the tree must be given.
            Empty node is represented by None. eg:([1, None, 2, None, None, 3, 4])
    @return: {TreeNode} Root node object of this tree.
    '''
    if len(node_vals) == 0:
        return None
    root = BinaryTreeNode(node_vals[0])
    node_queue = [root]
    index = 1
    while len(node_queue) > 0:
        cur_node = node_queue.pop(0)
        if index >= len(node_vals):
            break
        left_node = None
        if node_vals[index] is not None:
            left_node = BinaryTreeNode(node_vals[index])
        node_queue.append(left_node)
        if index + 1 >= len(node_vals):
            break
        right_node = None
        if node_vals[index + 1] is not None:
            right_node = BinaryTreeNode(node_vals[index+1])
        node_queue.append(right_node)
        if cur_node is not None:
            cur_node.left = left_node
            cur_node.right = right_node
        index += 2
    return root

#TODO: add tree valid check for parseTree function.
