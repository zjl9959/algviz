#!/usr/bin/env python3

"""Define the map class and related functions.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.utility import AlgvizRuntimeError, AlgvizParamError
from algviz.graph import GraphNode
from algviz.svg_graph import SvgGraph, _SvgGraphType


class Map():
    """Map contains keys and values, each key corresponding to a value.

    Map is relational container. You can get the value of a given key and update value.
    You can also add or remove a (key, value) pair and iterate on existing keys, values or items.
    [WARNING] Don't create this class directly, use algviz.Visualizer.createMap instead.
    """
    def __init__(self, data, delay):
        """
        Args:
            data (dict): The initial key and values of this map.
            delay (float): The delay time between two animation frames.
        """
        if data is None:
            self._data = dict()
        elif not isinstance(data, dict):
            raise AlgvizParamError("Map.init input data's type should be a dict")
        else:
            self._data = data
        self._delay = delay
        self._graph_nodes = dict()
        self._graph = SvgGraph([], True, self._delay)
        self._graph._type = _SvgGraphType(None, 'ellipse')
        for k, v in self._data.items():
            node_key = GraphNode(str(k))
            node_val = GraphNode(str(v))
            node_key.add(node_val)
            if self._graph.addNode(node_key) != 2:
                raise AlgvizRuntimeError('Map.init svgGraph add node error!')
            self._graph_nodes[k] = (node_key, node_val)

    def get(self, k, default=None):
        """Returns the value of the item with the specified key.

        Returns the default value set by default if the key is not in the map.

        Args:
            k (printable): the specified key.
            default (printable): the default value.

        Returns:
            printable: the value of the item with the specified key
        """
        return self._data.get(k, default)

    def clear(self):
        """Removes all the elements from the map.
        """
        for k in self._graph_nodes.keys():
            node_key = self._graph_nodes[k][0]
            if self._graph.removeNode(node_key, True) != 2:
                raise AlgvizRuntimeError('Map.clear svgGraph remove node error!')
        self._graph_nodes.clear()
        self._data.clear()

    def pop(self, k, default=None):
        """Removes the element with the specified key.

        Args:
            k (printable): the specified key.
            default (printable): the default value.

        Returns:
            printable: the value of the item to be removed or the default value.
        """
        if k in self._graph_nodes:
            node_key = self._graph_nodes[k][0]
            if self._graph.removeNode(node_key, True) != 2:
                raise AlgvizRuntimeError('Map.pop svgGraph remove node error!')
            self._graph_nodes.pop(k)
        return self._data.pop(k, default)

    def keys(self):
        """Returns a list containing the map's keys.

        Returns:
            iterable(printable): a list containing the map's keys.
        """
        return self._data.keys()

    def values(self):
        """Returns a list of all the values in the map.

        Returns:
            iterable(printable): a list of all the values in the map.
        """
        return self._data.values()

    def items(self):
        """Returns a list containing a tuple for each key value pair.

        Returns:
            iterable((printable, printable)): a list containing a tuple for each key value pair.
        """
        return self._data.items()

    def mark(self, color, keys, hold=False):
        """Emphasize the key and value nodes by mark it's background color.

        Args:
            color ((R,G,B)): The background color for the marked node. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
            keys (iterable(printable)): The list of keys to be marked.
            hold (bool): Whether to keep the mark color in future animation frames.
        """
        for k in keys:
            if k in self._graph_nodes:
                (node_key, node_val) = self._graph_nodes[k]
                self._graph.markNode(color, node_key, hold)
                self._graph.markNode(color, node_val, hold)

    def removeMark(self, color):
        """Remove the mark color.

        Args:
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        """
        self._graph.removeMark(color)

    def removeMarks(self, color_list):
        """Remove the mark colors.

        Args:
            color_list ([(R,G,B), ...]): all the colors to be removed.
        """
        self._graph.removeMarks(color_list)

    def __getitem__(self, k):
        return self.get(k)

    def __setitem__(self, k, v):
        if k in self._graph_nodes:
            self._graph_nodes[k][1].val = v
        else:
            node_key = GraphNode(str(k))
            node_val = GraphNode(str(v))
            node_key.add(node_val)
            if self._graph.addNode(node_key) != 2:
                raise AlgvizRuntimeError('Map.__setitem__ svgGraph add node error!')
            self._graph_nodes[k] = (node_key, node_val)
        self._data[k] = v

    def __len__(self):
        return len(self._data)

    def __contains__(self, k):
        """Check if the specified key in this map.

        Returns:
            boolean: True if key in this map, else return False.
        """
        if k in self._data:
            return True
        else:
            return False

    def _repr_svg_(self):
        self._graph._delay = self._delay
        return self._graph._repr_svg_()
