#!/usr/bin/env python3

"""Define graph related classes and functions.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.utility import AlgvizRuntimeError, _setElemColor
from algviz.graph_node_base import GraphNodeBase as NodeBase


class GraphNeighborIter():
    """Neighbor nodes iterator for GraphNode class.

    """
    def __init__(self, node, neighbors):
        self._node = node
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
            self._node._on_visit_neighbor_(neighbor[0])
            return neighbor[0], neighbor[1]


class GraphNode(NodeBase):
    """This class defined the type of typology graph node.

    """
    def __init__(self, val):
        super().__init__(val)
        super().__setattr__('_neighbors', dict())   # Key: Neighbor Node, Value: Edge Label.


    def neighbors(self):
        """Return an iterator to iter over all the neighbor nodes of this node.
        
        Returns:
            GraphNeighborIter: Neighbor node iterator.
        """
        iter_neighbors = super().__getattribute__('_neighbors')
        return GraphNeighborIter(self, tuple(iter_neighbors.items()))
    

    def add(self, node, edge=None):
        """Add a neighbor node for this node.
        
        Args:
            node (GraphNode): The neighbor node object to be added.
            edge (printable): The weight value of the edge between this node and neighbor node.
        """
        neighbors_ = super().__getattribute__('_neighbors')
        if node not in neighbors_:
            neighbors_[node] = edge
            self._on_update_neighbor_(None, node)


    def remove(self, node):
        """Remove one neighbor node. Do nothing if node not in neighbors collection.
        
        Args:
            node (GraphNode): The node to be removed.
        """
        neighbors_ = super().__getattribute__('_neighbors')
        if node in neighbors_:
            neighbors_.pop(node)
            self._on_update_neighbor_(node, None)


    def _neighbors_(self):
        """

        Returns:
            list([neighbor_node, edge]): All the neighbors nodes and edges.
        """
        neighbors_ = super().__getattribute__('_neighbors')
        return tuple(neighbors_.items())


def updateGraphEdge(node1, node2, edge):
    """Update the graph's edge between node1 and node2.
    
    Args:
        node1,node2 (GraphNode): The node related to the updated edge.
        edge (printable): New weight value for this edge.
    """
    node1_neighbors = node1._neighbors
    if node2 in node1_neighbors:
        node1_neighbors[node2] = edge
        node1_bind_graphs = node1.bind_graphs()
        for graph in node1_bind_graphs:
            graph._updateEdgeLabel(node1, node2, edge)
            graph.markEdge(_setElemColor, node1, node2, hold=False)
    node2_neighbors = node2._neighbors
    if node1 in node2_neighbors:
        node2_neighbors[node1] = edge
        node2_bind_graphs = node2.bind_graphs()
        for graph in node2_bind_graphs:
            graph._updateEdgeLabel(node2, node1, edge)
            graph.markEdge(_setElemColor, node2, node1, hold=False)


def parseGraph(nodes, edges, nodes_label=None, directed=True):
    """Create a new graph from edges and nodes information.
    
    All the input edges's start and edge node should be found in nodes parameter.
    
    Example: parseGraph({0, 1, 2}, [(0, 1), (1, 2), (2, 0)], nodes_label={0:'node_0'})

    Args:
        nodes (set(printable)): All the nodes in this graph.
        edges (list(tuple(node1, node2, edge))): All the edges in this graph.
        nodes_label (dict(printable:printable)): Map the node id into it's display label.
        directed (bool): Should this graph be directed graph or undirected.

    Returns:
        dict(printable): All the graph nodes in this graph. Key is node label in nodes parameter, Value is GraphNode object.
    
    Raises:
        AlgvizRuntimeError: (paraseGraph) can not find node object for edge xxx.

    """
    # Create nodes for this graph.
    nodes_dict = dict()
    for node in nodes:
        if node in nodes_dict:
            continue
        node_val = node
        if nodes_label and node in nodes_label:
            node_val = nodes_label[node]
        nodes_dict[node] = GraphNode(node_val)
    # Add edges for this graph.
    for edge in edges:
        node1, node2, edge_val = edge[0], edge[1], None
        if node1 in nodes_dict and node2 in nodes_dict:
            if len(edge) == 3:
                edge_val = edge[2]
            nodes_dict[node1].add(nodes_dict[node2], edge_val)
            if directed == False:
                nodes_dict[node2].add(nodes_dict[node1], edge_val)
        else:
            raise AlgvizRuntimeError('(paraseGraph) can not find node object for edge {}.'.format(edge))
    return nodes_dict
