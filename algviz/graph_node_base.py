#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from . import utility as util


class GraphNodeBase:
    '''
    @class: This is the base class for GraphNode, BinaryTreeNode,
            ForwardLinkedListNode and DoublyLinkedListNode.
    '''
    def __init__(self, val):
        '''
        @param: {val->printable} The label to be print in the graph node.
        '''
        object.__setattr__(self, 'val', val)
        object.__setattr__(self, '_bind_graph', None)

    
    def __getattribute__(self, name):
        if name == 'val':
            self._on_visit_value_()
            return object.__getattribute__(self, 'val')
        else:
            return object.__getattribute__(self, name)


    def __setattr__(self, name, value):
        if name == 'val':
            object.__setattr__(self, 'val', value)
            self._on_update_value_(value)
        else:
            object.__setattr__(self, name, value)


    def __str__(self):
        return str(object.__getattribute__(self, 'val'))


    def _on_visit_value_(self):
        '''
        @function: Notify the bind graph to update the displayed node mark.
        '''
        bind_graph = object.__getattribute__(self, '_bind_graph')
        if bind_graph:
            bind_graph.markNode(util._getElemColor, self, hold=False)


    def _on_update_value_(self, value):
        '''
        @function: Notify the bind graph to update the displayed node mark and value.
        @param: {value->printable} The value to be displayed in this node.
        '''
        bind_graph = object.__getattribute__(self, '_bind_graph')
        if bind_graph:
            bind_graph._updateNodeLabel(self, value)
            bind_graph.markNode(util._setElemColor, self, hold=False)


    def _on_visit_neighbor_(self, neighbor):
        '''
        @function: Notify the bind graph to update the displayed edge color between this node and it's neighbor.
        '''
        bind_graph = object.__getattribute__(self, '_bind_graph')
        if bind_graph:
            bind_graph.markEdge(util._getElemColor, self, neighbor, hold=False)

    
    def _on_update_neighbor_(self, old_neighbor, new_neighbor):
        '''
        @function: Notify the bind graph to update the displayed edge color between this node and it's neighbor.
        @param: (old_neighbor,new_neighbor->GraphNodeBase) The subclasses of GraphNodeBase.
        '''
        # Mark edge between this node and it's old_neighbor.
        bind_graph = object.__getattribute__(self, '_bind_graph')
        if not bind_graph:
            return
        if old_neighbor:
            bind_graph.markEdge(util._setElemColor, self, old_neighbor, hold=False)
        # Mark edge between this node and it's new_neighbor.
        if new_neighbor:
            bind_graph.addNode(new_neighbor)
            bind_graph.markEdge(util._setElemColor, self, new_neighbor, hold=False)


    def bind_graph(self):
        '''
        @return: {SvgGraph} Return the bind graph of this node.
        '''
        return object.__getattribute__(self, '_bind_graph')


    def _bind_graph_(self, graph):
        '''
        @function: Bind a new SvgGraph object for this graph node object.
        @param: {graph->SvgGraph} New SvgGraph object to track.
        '''
        object.__setattr__(self, '_bind_graph', graph)
