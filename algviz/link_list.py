#!/usr/bin/env python3

'''
@author:zjl9959@gmail.com
@license:GPLv3
'''

from . import utility as util


class ListNode():
    '''
    @class: The node for forward link list.
    '''

    def __init__(self, val):
        '''
        @param: (val->printable) The label to be displayed in link list node.
        '''
        super().__setattr__('val', val)
        super().__setattr__('next', None)
        super().__setattr__('_bind_graphs', set())


    def __getattribute__(self, name):
        if name == 'val':
            # Set value and update node's visit state in list.
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markNode(util._getElemColor, self, hold=False)
            return super().__getattribute__('val')
        elif name == 'next':
            # Visit next node in the link list and update the node's visit state.
            node = super().__getattribute__('next')
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
        elif name == 'next':
            # Mark old edge.
            node = super().__getattribute__(name)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(util._setElemColor, self, node, hold=False)
            # Mark new edge.
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
        @function: Interface for SvgGraph. Get this node's neighbors(next node).
        @return: (list(tuple(next_node, None))) The neighbors list of this node.
        '''
        next_node = super().__getattribute__('next')
        return [(next_node, None)]
    

    def _add_graph_(self, gra):
        '''
        @function: Bind a new SvgGraph object for this ListNode object.
        @param: (gra->SvgGraph) New SvgGraph object to track.
        '''
        bind_graphs = super().__getattribute__('_bind_graphs')
        bind_graphs.add(gra)
    

    def _remove_graph_(self, gra):
        '''
        @function: Remove one SvgGraph object from this ListNode object.
        @param: (gra->SvgGraph) SvgGraph object to remove.
        '''
        bind_graphs = super().__getattribute__('_bind_graphs')
        if gra in bind_graphs:
            bind_graphs.remove(gra)


def parseLinkList(li_vals):
    '''
    @function: Create a new forward link list object and return it's head node.
    @param: (li_str->list) The labels to display in the link list's nodes.
    @return: (head->ListNode) The head ListNode objet for this forward link list.
    '''
    if len(li_vals) == 0:
        return None
    head = ListNode(li_vals[0])
    cur_node = head
    for i in range(1, len(li_vals)):
        cur_node.next = ListNode(li_vals[i])
        cur_node = cur_node.next
    return head
