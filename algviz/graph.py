#!/usr/bin/env python3

'''
@author:zjl9959@gmail.com
@license:GPLv3
'''

import utility as util


class GraphNeighborIter():
    '''
    @class: Neighbor node iterator for GraphNode class.
    '''
    def __init__(self, node, bind_graphs, neighbors):
        self._node = node
        self._bind_graphs = bind_graphs
        self._neighbors = neighbors
        self._next_index = 0
    
    def __iter__(self):
        self._next_index = 0
        return self
    
    def __next__(self):
        if self._next_index >= len(self._neighbors):
            raise StopIteration
        else:
            neighbor = self._neighbors[self._next_index]
            self._next_index += 1
            for gra in self._bind_graphs:
                gra.markEdge(util._getElemColor, self._node, neighbor[0], hold=False)
            return neighbor


class GraphNode():
    def __init__(self, val):
        '''
        @param: (val->printable) The label to be displayed on the graph node.
        '''
        super().__setattr__('val', val)
        super().__setattr__('_neighbors', list())
        super().__setattr__('_bind_graphs', set())
    

    def __str__(self):
        return str(super().__getattribute__('val'))
    

    def __getattribute__(self, name):
        if name == 'val':
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markNode(util._getElemColor, self, hold=False)
            return super().__getattribute__('val')
        else:
            return super().__getattribute__(name)
    

    def __setattr__(self, name, value):
        if name == 'val':
            super().__setattr__('val', value)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra._updateNodeLabel(self, value)
                gra.markNode(util._setElemColor, self, hold=False)
        else:
            super().__setattr__(name, value)


    def neighbors(self):
        '''
        @function: Return all neighbor nodes of this node.
        @return: (GraphNeighborIter) Neighbor node iterator.
        '''
        iter_neighbors = super().__getattribute__('_neighbors')
        bind_graphs = super().__getattribute__('_bind_graphs')
        return GraphNeighborIter(self, bind_graphs, iter_neighbors)
    

    def append(self, node, weight=None):
        '''
        @function: Add a node after the last neighbor node.
        @param: (node->GraphNode) The node object to be appended.
        @param: (weight->printable) The weight value of the edge between this node and appended node.
        @return: (bool) True if successfully appended node; Flase if node already in neighbors.
        '''
        pos = self._get_node_index_(node)
        if pos == -1:
            neighbors_ = super().__getattribute__('_neighbors')
            neighbors_.append([node, weight])
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.addNode(node)
                gra.markEdge(util._setElemColor, self, node, hold=False)
            return True
        else:
            return False
    

    def insertBefore(self, node, ref_node, weight=None):
        '''
        @function: If ref_node in neighbor list, then insert a node in front of the 'ref_node' neighbor node.
        @param: (node->GraphNode) New node to be inserted into neighbor list.
        @param: (ref_node->GraphNode) Indicate the position to insert new node.
        @param: (weight) The weight value of the edge between this node and inserted node.
        @return: (bool) True if successfully inserted node; Flase if node already in neighbors or can't find ref_node.
        '''
        pos = self._get_node_index_(ref_node)
        pos2 = self._get_node_index_(node)
        if pos != -1 and pos2 == -1:
            neighbors_ = super().__getattribute__('_neighbors')
            neighbors_.insert(pos, [node, weight])
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.addNode(node)
                gra.markEdge(util._setElemColor, self, node, hold=False)
            return True
        else:
            return False
    

    def replace(self, new_node, old_node, weight=None):
        '''
        @funtion: Replace old_node into new_node in neighbors list.
        @param: (new_node->GraphNode) New node to replace.
        @param: (old_node->GraphNode) Old node to be replaced.
        @param: (weight) The weight value of the edge between this node and replaced new node.
        @return: (bool) True if successfully replaced node; Flase if new_node already in neighbors or can't find old_node.
        '''
        pos = self._get_node_index_(old_node)
        pos2 = self._get_node_index_(new_node)
        if pos != -1 and pos2 == -1:
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(util._setElemColor, self, old_node, hold=False)
            neighbors_ = super().__getattribute__('_neighbors')
            neighbors_[pos] = [new_node, weight]
            for gra in bind_graphs:
                gra.addNode(new_node)
                gra.markEdge(util._setElemColor, self, new_node, hold=False)
            return True
        else:
            return False
    

    def remove(self, node):
        '''
        @function: Remove one neighbor node. Do nothing if node not in neighbors list.
        @param: (node->GraphNode) The node to be replaced.
        @return: (bool) True if successfully removed node; Flase if can't find node.
        '''
        pos = self._get_node_index_(node)
        if pos != -1:
            neighbors_ = super().__getattribute__('_neighbors')
            neighbors_.pop(pos)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(util._setElemColor, self, node, hold=False)
            return True
        return False
    

    def _get_node_index_(self, node):
        '''
        @function: Locate the index position of node in neighbors.
        @param: (node->GraphNode) The node object to locate.
        @return: (int) The index of node in neighbors. return -1 if can't find node.
        '''
        neighbors_ = super().__getattribute__('_neighbors')
        for i in range(len(neighbors_)):
            if neighbors_[i][0] == node:
                return i
        return -1
                    

    def _neighbors_(self):
        '''
        @return: (list([neighbor_node, weight]))  All the neighbors nodes and edges.
        '''
        return super().__getattribute__('_neighbors')


    def _add_graph_(self, gra):
        '''
        @function: Bind a new SvgGraph object for this GrapNode object.
        @param: (gra->SvgGraph) New SvgGraph object to track.
        '''
        bind_graphs = super().__getattribute__('_bind_graphs')
        bind_graphs.add(gra)
    

    def _remove_graph_(self, gra):
        '''
        @function: Remove one SvgGraph object from this GrapNode object.
        @param: (gra->SvgGraph) SvgGraph object to remove.
        '''
        bind_graphs = super().__getattribute__('_bind_graphs')
        if gra in bind_graphs:
            bind_graphs.remove(gra)


def updateEdgeWeight(node1, node2, weight):
    '''
    @function: Update the edge's weight value between node1 and node2.
    @param: (node1/node2->GraphNode) The node related to the updated edge.
    @param: (weight->printable) New weight value for this edge.
    @retrun: (success->bool) True if successfull update the edge's weight, otherwise return False.
    '''
    pos1 = node1._get_node_index_(node2)
    pos2 = node2._get_node_index_(node1)
    if pos1 != -1 and pos2 != -1:
        node1._neighbors[pos1][1] = weight
        for gra in node1._bind_graphs:
            gra._updateEdgeLabel(node1, node2, weight)
            gra.markEdge(util._setElemColor, node1, node2, hold=False)
        node2._neighbors[pos2][1] = weight
        for gra in node2._bind_graphs:
            gra._updateEdgeLabel(node2, node1, weight)
            gra.markEdge(util._setElemColor, node2, node1, hold=False)
        return True
    else:
        return False
    

def parseGraph(edges_, nodes_=None, directed=True):
    '''
    @function: Create a new graph from edges and nodes information.
    @param: (edges->list(iterable)) All the edges in this graph. One edge is a iterable object with two element(node id).（eg:[[0, 1], [1, 2], [2, 0]]）。
    @param: (nodes->list(iterable)) The correspondence between node_id in this graph and it's node lable.（eg:[[0, node1], [1, node2], [2, node3]]）。
    @param: (directed->bool) Should this graph be directed graph or undirected.
    @return: (dict(node_id:GraphNode object)) All the graph nodes set in this graph.
    '''
    res = dict()
    # Create nodes for this graph.
    if nodes_ is not None:
        for nid, val in nodes_:
            res[nid] = GraphNode(val)
    else:
        for edge in edges_:
            if edge[0] not in res.keys():
                res[edge[0]] = GraphNode(edge[0])
            if edge[1] not in res.keys():
                res[edge[1]] = GraphNode(edge[1])
    # Add edges for this graph.
    for edge in edges_:
        n1id, n2id, weight = None, None, None
        if len(edge) == 3:
            n1id, n2id, weight = edge
        elif len(edge) == 2:
            n1id, n2id = edge
        if n1id in res.keys() and n2id in res.keys():
            res[n1id].append(res[n2id], weight)
            if directed == False:
                res[n2id].append(res[n1id], weight)
    return res
