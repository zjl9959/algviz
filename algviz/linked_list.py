#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from . import graph_node_base
NodeBase = graph_node_base.GraphNodeBase


class ForwardLinkedListNode(NodeBase):
    '''
    @class: The node for forward linked list.
    '''

    def __init__(self, val):
        '''
        @param: {val->printable} The label to be displayed in forward linked list node.
        '''
        super().__init__(val)
        super().__setattr__('next', None)


    def __getattribute__(self, name):
        if name == 'next':
            # Visit next node in the forward linked list and update the node's visit state.
            node = super().__getattribute__('next')
            self._on_visit_neighbor_(node)
            return node
        else:
            return super().__getattribute__(name)
    

    def __setattr__(self, name, value):
        if name == 'next':
            old_node = super().__getattribute__(name)
            super().__setattr__('next', value)
            self._on_update_neighbor_(old_node, value)
        else:
            super().__setattr__(name, value)
    

    def _neighbors_(self):
        '''
        @function: Interface for SvgGraph. Get this node's neighbors(next node).
        @return: {list(tuple(next_node, None))} The neighbors list of this node.
        '''
        next_node = super().__getattribute__('next')
        return [(next_node, None)]


class DoublyLinkedListNode(NodeBase):
    '''
    @class: The node for doubly linked list.
    '''

    def __init__(self, val):
        '''
        @param: {val->printable} The label to be displayed in doubly linked list node.
        '''
        super().__init__(val)
        super().__setattr__('next', None)
        super().__setattr__('prev', None)


    def __getattribute__(self, name):
        if name == 'next' or name == 'prev':
            # Visit next node in the doubly linked list and update the node's visit state.
            node = super().__getattribute__(name)
            self._on_visit_neighbor_(node)
            return node
        else:
            return super().__getattribute__(name)


    def __setattr__(self, name, value):
        if name == 'next' or name == 'prev':
            old_node = super().__getattribute__(name)
            super().__setattr__(name, value)
            self._on_update_neighbor_(old_node, value)
        else:
            super().__setattr__(name, value)


    def _neighbors_(self):
        '''
        @function: Interface for SvgGraph. Get this node's neighbors(next node).
        @return: {list(tuple(next_node, None))} The neighbors list of this node.
        '''
        next_node = super().__getattribute__('next')
        prev_node = super().__getattribute__('prev')
        return [(next_node, None), (prev_node, None)]


def parseForwardLinkedList(list_info):
    '''
    @function: Create a new forward linked list object and return it's head node.
    @param: {list_info->list} The labels to display in the forward linked list's nodes.
    @return: {head->ForwardLinkedListNode} The head node objet for this forward linked list.
    '''
    if len(list_info) == 0:
        return None
    head = ForwardLinkedListNode(list_info[0])
    cur_node = head
    for i in range(1, len(list_info)):
        cur_node.next = ForwardLinkedListNode(list_info[i])
        cur_node = cur_node.next
    return head


def parseDoublyLinkedList(list_info):
    '''
    @function: Create a new doubly linked list object and return it's head and tail node.
    @param: {list_info->list} The labels to display in the doubly linked list's nodes.
    @return: {(head,tail)->DoublyLinkedListNode} The head and tail node objects for this doubly linked list.
    '''
    if len(list_info) == 0:
        return (None, None)
    head = DoublyLinkedListNode(list_info[0])
    cur_node, next_node = head, head
    for i in range(1, len(list_info)):
        next_node = DoublyLinkedListNode(list_info[i])
        cur_node.next = next_node
        next_node.prev = cur_node
        cur_node = cur_node.next
    return (head, next_node)
