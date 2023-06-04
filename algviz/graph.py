#!/usr/bin/env python3

"""Define graph related classes and functions.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.utility import AlgvizRuntimeError, AlgvizParamError
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
            return neighbor[0], neighbor[1]


class GraphNode(NodeBase):
    """This class defined the type of typology graph node.

    Attributes:
        val (printable): The label to be displayed in the graph node.
    """
    def __init__(self, val):
        super().__init__(val)
        super().__setattr__('_neighbors', list())   # tuple(Neighbor Node, Edge Label).

    def neighbors(self):
        """Return an iterator to iter over all the neighbor nodes of this node.

        Returns:
            GraphNeighborIter: Neighbor node iterator.
        """
        iter_neighbors = super().__getattribute__('_neighbors')
        return GraphNeighborIter(self, tuple(iter_neighbors))

    def neighborCount(self):
        """Return the neighbors count of this node.

        Returns:
            int: neighbors count.
        """
        neighbors_ = super().__getattribute__('_neighbors')
        return len(neighbors_)

    def neighborAt(self, index):
        """Return the neighbor node, edge at the index position of the neighbors list.

        Args:
            index (int): The position of the neighbor node.

        Returns:
            GraphNode: neighbor node.
            printable: the edge between this node and the neighbor node.

        Raises:
            AlgvizParamError: GraphNode neighbor index type error or out of range.
        """
        neighbors_ = super().__getattribute__('_neighbors')
        if type(index) != int or index < 0 or index >= len(neighbors_):
            raise AlgvizParamError('GraphNode neighbor index type error or out of range.')
        return neighbors_[index][0], neighbors_[index][1]

    def neighborIndex(self, node):
        """Return the neighbor node index in the neighbors list.

        Args:
            node (GraphNode): The neighbor node object to be located.

        Returns:
            int: the index position of the neighbor node. If node not found, then return -1.
        """
        res = -1
        neighbors_ = super().__getattribute__('_neighbors')
        for i in range(len(neighbors_)):
            if node == neighbors_[i][0]:
                res = i
        return res

    def add(self, node, edge=None, index=None):
        """Add a neighbor node for this node.

        Args:
            node (GraphNode): The neighbor node object to be added.
            edge (printable): The weight value of the edge between this node and neighbor node.

        Raises:
            AlgvizParamError: GraphNode neighbor index should be a positive integer!
        """
        if (type(index) != int and index is not None) or (type(index) == int and index < 0):
            raise AlgvizParamError('GraphNode neighbor index should be a positive integer!')
        neighbors_ = super().__getattribute__('_neighbors')
        for (n, _) in neighbors_:
            if node == n:
                return
        if index is None or index >= len(neighbors_):
            neighbors_.append((node, edge))
        else:
            neighbors_.insert(index, (node, edge))
        self._on_update_neighbor_(node)

    def remove(self, node):
        """Remove one neighbor node. Do nothing if node not in neighbors collection.

        Args:
            node (GraphNode): The neighbor node to be removed.
        """
        neighbors_ = super().__getattribute__('_neighbors')
        for i in range(len(neighbors_)):
            if neighbors_[i][0] == node:
                neighbors_.pop(i)
                self._on_update_neighbor_(None)
                return

    def removeAt(self, index):
        """Remove one neighbor node. Do nothing if node not in neighbors collection.

        Args:
            index (int): The neighbor node index to be removed.

        Raises:
            AlgvizParamError: GraphNode neighbor index type error or out of range.
        """
        neighbors_ = super().__getattribute__('_neighbors')
        if type(index) != int or index < 0 or index >= len(neighbors_):
            raise AlgvizParamError('GraphNode neighbor index type error or out of range.')
        neighbors_.pop(index)
        self._on_update_neighbor_(None)

    def _neighbors_(self):
        """

        Returns:
            list[(neighbor_node, edge)]: All the neighbors nodes and edges.
        """
        neighbors_ = super().__getattribute__('_neighbors')
        return neighbors_


def updateGraphEdge(node1, node2, edge):
    """Update the graph's edge between node1 and node2.

    Args:
        node1,node2 (GraphNode): The node related to the updated edge.
        edge (printable): New weight value for this edge.
    """
    node1_neighbors = node1._neighbors
    pos_1 = node1.neighborIndex(node2)
    if pos_1 != -1:
        node1_neighbors[pos_1] = (node2, edge)
        node1_bind_graphs = node1.bind_graphs()
        for graph in node1_bind_graphs:
            graph._updateEdgeLabel(node1, node2, edge)
    node2_neighbors = node2._neighbors
    pos_2 = node2.neighborIndex(node1)
    if pos_2 != -1:
        node2_neighbors[pos_2] = (node1, edge)
        node2_bind_graphs = node2.bind_graphs()
        for graph in node2_bind_graphs:
            graph._updateEdgeLabel(node2, node1, edge)


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
            if directed is False:
                nodes_dict[node2].add(nodes_dict[node1], edge_val)
        else:
            raise AlgvizRuntimeError('(paraseGraph) can not find node object for edge {}.'.format(edge))
    return nodes_dict


def generateRandomGraph(nb_nodes, nb_edges, max_degree=None, directed=False):
    """Generate a random graph with the given constraint.

    Args:
        nb_nodes (int): the nodes number of this graph, the node id start from 0.
        nb_edges (int): the edges number of this graph.
        max_degree (max_degree): the maximum degree for graph nodes(minimum degree is 1).
        directed (boolean): is this a directed graph or not.

    Returns:
        nodes (set(printable)), edges (list(tuple(node1, node2, edge))): all the nodes in this graph and all the edges in this graph.

    Raises:
        AlgvizParamError: generateRandomGraph: input nodes number should be greater than 0.
        AlgvizParamError: generateRandomGraph: input edges number should be greater or equal than nodes number.
        AlgvizParamError: generateRandomGraph: max_degree is not enough to generate such edges.
        AlgvizRuntimeError: generateRandomGraph: can not pick a suitable node.
    """
    def random_pick_nodes(nodes_list, nodes_degree, exclude=list()):
        pick_list = []
        for n in nodes_list:
            if nodes_degree[n] < max_degree and n not in exclude:
                pick_list.append(n)
        if len(pick_list) == 0:
            return None
        index = randint(0, len(pick_list) - 1)
        return pick_list[index]

    if max_degree is None:
        max_degree = nb_nodes
    if directed:
        max_degree = min(max_degree, 2 * (nb_nodes - 1))
    else:
        max_degree = min(max_degree, nb_nodes - 1)

    if nb_nodes < 0:
        raise AlgvizParamError('generateRandomGraph: input nodes number should be greater than 0.')
    if nb_edges < nb_nodes:
        raise AlgvizParamError('generateRandomGraph: input edges number should be greater or equal than nodes number.')
    if nb_nodes * max_degree < nb_edges * 2:
        raise AlgvizParamError('generateRandomGraph: max_degree is not enough to generate such edges.')
    from random import randint
    # Create nodes for this graph.
    nodes_not_in_graph = list()
    nodes_degree = dict()
    for i in range(nb_nodes):
        nodes_not_in_graph.append(i)
        nodes_degree[i] = 0
    # Random pick nodes and generate edges.
    edges = list()
    # Make sure none node is isolate.
    nodes_in_graph = list()
    while len(nodes_not_in_graph) > 0:
        index1 = randint(0, len(nodes_not_in_graph) - 1)
        n1 = nodes_not_in_graph[index1]
        if len(nodes_in_graph) > 0:
            n2 = random_pick_nodes(nodes_in_graph, nodes_degree)
            if n2 is None:
                raise AlgvizRuntimeError('generateRandomGraph: can not pick a suitable node.')
            edges.append((n1, n2))
            nodes_degree[n2] += 1
            nodes_degree[n1] += 1
        nodes_in_graph.append(n1)
        nodes_not_in_graph.pop(index1)
    # Generate the rest edges randomly.
    while len(edges) < nb_edges:
        n1 = random_pick_nodes(nodes_in_graph, nodes_degree)
        n2 = random_pick_nodes(nodes_in_graph, nodes_degree, [n1])
        if n1 is None or n2 is None:
            raise AlgvizRuntimeError('generateRandomGraph: can not pick a suitable node.')
        if randint(0, 1) == 1:
            n1, n2 = n2, n1
        if directed:
            if (n1, n2) in edges:
                continue
        else:
            if (n1, n2) in edges or (n2, n1) in edges:
                continue
        edges.append((n1, n2))
        nodes_degree[n1] += 1
        nodes_degree[n2] += 1
    return sorted(nodes_in_graph), edges
