#!/usr/bin/env python3

"""Define the base class for all the graph nodes.

Do not create GraphNodeBase class directly,
create one of it's subclass instead.

Author: zjl9959@gmail.com

License: GPLv3

"""


class GraphNodeBase:
    """Base class for all the graph nodes.

    GraphNodeBase's subclasses contain:
    GraphNode, BinaryTreeNode, ForwardLinkedListNode and DoublyLinkedListNode.
    If you want to get/set attribute in subclass, don't use dot operation like 'self.attr'.
    Please use these interfaces instead:

        super().__getattribute__(attr)

        super().__setattr__(attr, new_value)

    Attributes:
        val (printable): The label to be displayed in the graph node.
    """

    def __init__(self, val):
        """
        Args:
            val (printable): The initial label for the graph node.
        """
        object.__setattr__(self, 'val', val)
        object.__setattr__(self, '_bind_graphs', set())

    def __getattribute__(self, name):
        if name == 'val':
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
        value = object.__getattribute__(self, 'val')
        if value is None:
            value = ''
        return str(value)

    def _on_update_value_(self, value):
        """Notify the bind graph to update the displayed node mark and value.

        Args:
            value (printable): The value to be displayed in this node.
        """
        bind_graphs = object.__getattribute__(self, '_bind_graphs')
        for graph in bind_graphs:
            graph._updateNodeLabel(self, value)

    def _on_update_neighbor_(self, new_neighbor):
        """
        Notify the bind graph to update the displayed edge color between this node and it's neighbor.
        old_neighbor and new_neighbor can be None.

        Args:
            new_neighbor: The new neighbor node to replace the old neighbor nodes.
        """
        # Mark edge between this node and it's old_neighbor.
        bind_graphs = object.__getattribute__(self, '_bind_graphs')
        if len(bind_graphs) == 0:
            return
        # Mark edge between this node and it's new_neighbor.
        if new_neighbor:
            for graph in bind_graphs:
                graph.addNode(new_neighbor)

    def bind_graphs(self):
        """
        Returns:
            set(SvgGraph): The bind graphs collection of this node.
        """
        return object.__getattribute__(self, '_bind_graphs')

    def _bind_new_graph_(self, graph):
        """Bind a new SvgGraph object for this graph node object.

        Args:
            graph (SvgGraph): New SvgGraph object to track this node.
        """
        bind_graphs = object.__getattribute__(self, '_bind_graphs')
        if graph not in bind_graphs:
            bind_graphs.add(graph)

    def _remove_bind_graph_(self, graph):
        """Remove the SvgGraph object binded to this graph node object.

        The graph object will not track the change of this node, if it is successfully removed from bind_graphs.

        Args:
            graph (SvgGraph): SvgGraph object to be removed.
        """
        bind_graphs = object.__getattribute__(self, '_bind_graphs')
        if graph in bind_graphs:
            bind_graphs.remove(graph)
