#!/usr/bin/env python3

"""Define low-level SVG animation refresh related classes for graph.

This module was used by linked_list, tree and graph module.
You can use the addNode, removeNode, markNode, markEdge and removeMark interfaces to update the graph.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.utility import str2rgbcolor, text_font_size, auto_text_color, rgbcolor2str
from algviz.utility import add_animate_appear_into_node, add_animate_move_into_node
from algviz.utility import TraceColorStack, ConsecutiveIdMap, AlgvizFatalError
from algviz.utility import add_desc_into_svg, find_tag_by_id, add_animate_scale_into_text
from algviz.graph import GraphNode
from algviz.tree import BinaryTreeNode, TreeNode
from algviz.linked_list import ForwardLinkedListNode, DoublyLinkedListNode

from graphviz import Digraph as graphviz_Digraph
from graphviz import Graph as graphviz_Graph
from graphviz import __version__ as graphviz_version
from xml.dom.minidom import parseString as mindom_parseString


class _SvgGraphType:
    """This class is used to specific the layout parameter for SvgGraph class.
    """
    def __init__(self, rankdir=None, shape='circle'):
        """
        Args:
            rankdir (str): The layout direction for graph. example: 'LR'
        """
        self.rankdir = rankdir
        self.shape = shape


def _get_graph_type_by_data_(data):
    """Check the input graph nodes data type and create graph layout parameter.

    Returns:
        _SvgGraphType: The layout data parmeter for SvgGraph.
    """
    if not data:
        return _SvgGraphType()
    # Get one node data from different type of data.
    if type(data) == dict:
        data = tuple(data.values())
    if (type(data) == list or type(data) == tuple) and len(data) > 0:
        data = data[0]
    layout = _SvgGraphType()
    # Check the data type and specific the layout parameter.
    if type(data) == GraphNode:
        # For normal graph layout.
        layout = _SvgGraphType('LR')
    elif type(data) == BinaryTreeNode:
        # For binary tree layout.
        layout = _SvgGraphType()
    elif type(data) == TreeNode:
        # For normal tree layout.
        layout = _SvgGraphType()
    elif type(data) == ForwardLinkedListNode:
        # For forward linked list layout.
        layout = _SvgGraphType('LR')
    elif type(data) == DoublyLinkedListNode:
        # For doubly linked list layout.
        layout = _SvgGraphType('LR')
    return layout


class SvgGraph():
    """A SvgGraph object can record all the nodes in it's binded graph.

    It will relayout the graph and generate animation when add/remove/replace node(s) in graph.
    It will also show the mark of graph node(s)&edge(s) visit status.
    Every time `__repr_svg__` function is called, SvgGraph object will return the latest svg string for this graph and prepare for a new frame.

    """

    def __init__(self, data, directed, delay):
        """
        Args:
            data (iterable): The root node(s) of the topology graph, used to initialize auxiliary data for this graph.
            directed (bool): Should this graph be directed graph or undirected.
            delay (float): Animation delay time between two animation frames.
        """
        self._directed = directed       # Whether the graph is a directed graph.
        self._delay = delay             # Delay time of each frame of animation.
        self._node_seq = list()         # The graph node(s) list arranged in a certain order.
        self._add_nodes = list()        # Record the externally added node(s) since last frame.
        self._remove_nodes = list()     # Record the externally deleted node(s) since last frame.
        self._edge_label = dict()       # Label information to be displayed on each edge of the graph.
        self._node_tcs = dict()         # Record the trajectory access information for all nodes in the current graph (node: ColorStack).
        self._edge_tcs = dict()         # Record the trajectory access information of all edges in the current graph ((start_node, end_node): ColorStack).
        self._node_appear = set()       # Record the collection of node(s) that appearing in the next frame of animation.
        self._node_disappear = set()    # Record the collection of node(s) that disappear in the next frame of animation.
        self._edge_appear = set()       # Record the collection of edge(s) that appearing in the next frame of animation.
        self._edge_disappear = set()    # Record the collection of edge(s) that disappear in the next frame of animation.
        self._node_move = set()         # Record the collection of nodes moving in the animation effect.
        self._frame_trace_old = list()  # Cache the node/edge related information that needs to be cleared in the previous frame (node_index/edge_index, ColorStack).
        self._frame_trace = list()      # Cache the node/edge related information to be refreshed in the next frame (node_index/edge_index, ColorStack, persistence).
        self._svg = None                # The svg object of the graph to be displayed.
        self._node_idmap = None         # Map node_index value to the corresponding node index in graphviz's output svg.
        self._edge_idmap = None         # Map edge_index value to the corresponding edge index in graphviz's output svg.
        self._add_history = set()       # Record all the nodes that have been added since graph created. Used to check duplicates when add/remove nodes in the graph.
        self._nodes_label_update = dict()   # Cache all the nodes label in the graph to be update since last frame.
        self._edges_lable_update = dict()   # Cache all the edges label in the graph to be update since last frame.
        self._type = _get_graph_type_by_data_(data)
        # Init graph nodes and svg.
        (self._svg, self._node_idmap, self._edge_idmap) = self._create_svg_()
        self._init_graph_nodes(data)    # Traverse the data and add nodes into this graph.
        add_desc_into_svg(self._svg)

    def addNode(self, node):
        """Add a new node and all it's successor nodes into this graph.

        Args:
            node (subclass of GraphNodeBase): The node object to be added. Can be a graph/tree/linked_list node.

        Returns:
            int: The number of node(s) added into graph.
        """
        if node in self._add_history:
            return 0
        node_stack = [node]
        added_nodes_num = 0
        while len(node_stack) > 0:
            cur_node = node_stack.pop()
            if cur_node is None or cur_node in self._add_history:
                continue
            cur_node._bind_new_graph_(self)
            self._add_history.add(cur_node)
            self._add_nodes.append(cur_node)
            added_nodes_num = added_nodes_num + 1
            for neigh in cur_node._neighbors_()[::-1]:
                node_stack.append(neigh[0])
        return added_nodes_num

    def removeNode(self, node, recursive=False):
        """Remove a node from this graph. Remove this node's all successor nodes if recursive is True.

        If the removed node(s) have input edge(s) from the remains node(s) in this graph, do nothing a return 0.

        Args:
            node (subclass of GraphNodeBase): The node object to be removed. Can be a graph/tree/linked_list node.
            recursive (bool): Wheather to remove all the successor nodes of this node.

        Returns:
            int: The number of node(s) removed from graph.
        """
        subgraph_nodes = set()
        if recursive:
            node_stack = [node]
            while len(node_stack) > 0:
                cur_node = node_stack.pop()
                if cur_node is None or cur_node in subgraph_nodes:
                    continue
                if cur_node in self._remove_nodes or cur_node not in self._add_history:
                    continue
                cur_node._remove_bind_graph_(self)
                self._add_history.remove(cur_node)
                subgraph_nodes.add(cur_node)
                for neighbor in cur_node._neighbors_():
                    node_stack.append(neighbor[0])
        else:
            if node and node in self._add_history:
                subgraph_nodes.add(node)
            else:
                return 0
        # Make sure there is no output edge into the subgraph nodes to be removed.
        node_stack = self._node_seq + self._add_nodes
        visited = set(self._remove_nodes)
        while len(node_stack) > 0:
            cur_node = node_stack.pop()
            if cur_node is None or cur_node in subgraph_nodes or cur_node in visited:
                continue
            visited.add(cur_node)
            for neigh in cur_node._neighbors_():
                if neigh[0] is not None:
                    if neigh[0] in subgraph_nodes:
                        return 0
                    node_stack.append(neigh[0])
        for node in subgraph_nodes:
            self._remove_nodes.append(node)
        return len(subgraph_nodes)

    def markNode(self, color, node, hold=False):
        """Emphasize one node by mark it's background color.

        Args:
            color ((R,G,B)): The background color for the marked node. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
            node (subclass of GraphNodeBase): The node object to be marked. Can be a graph/tree/linked_list node.
            hold (bool): Whether to keep the mark color in future animation frames.
        """
        if node is not None:
            if node not in self._node_tcs.keys():
                self._node_tcs[node] = TraceColorStack()
            self._node_tcs[node].add(color)
            self._frame_trace.append((node, color, hold))

    def markEdge(self, color, node1, node2, hold=False):
        """Emphasize one edge by mark it's stoke color.

        Args:
            color ((R,G,B)): The stroke color for the marked edge. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
            node1, node2 (subclass of GraphNodeBase): The begin and end node in the edge to be marked. Can be a graph/tree/linked_list node.
            hold (bool): Whether to keep the mark color in future animation frames.
        """
        if node1 is not None and node2 is not None:
            edge_key = self._make_edge_tuple_(node1, node2)
            if edge_key not in self._edge_tcs.keys():
                self._edge_tcs[edge_key] = TraceColorStack(bgcolor=(123, 123, 123))
            self._edge_tcs[edge_key].add(color)
            self._frame_trace.append((edge_key, color, hold))

    def removeMark(self, color):
        """Remove the mark color for node(s) and edge(s).

        Args:
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        """
        for k in self._node_seq:
            if self._node_tcs[k].remove(color):
                node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(k))
                node = find_tag_by_id(self._svg, 'g', node_id)
                self._update_node_color_(node, self._node_tcs[k].color())
        for k in self._edge_label.keys():
            if self._edge_tcs[k].remove(color):
                edge_id = 'edge{}'.format(self._edge_idmap.toConsecutiveId(k))
                edge = find_tag_by_id(self._svg, 'g', edge_id)
                self._update_edge_color_(edge, self._edge_tcs[k].color())

    def removeMarks(self, color_list):
        """Remove the mark colors for node(s) and edge(s).

        Args:
            color_list ([(R,G,B), ...]): all the colors to be removed.
        """
        for color in color_list:
            self.removeMark(color)

    def _init_graph_nodes(self, data):
        if not data:
            return
        if type(data) == dict:
            for node in data.values():
                self.addNode(node)
        elif type(data) == list:
            for node in data:
                self.addNode(node)
        else:
            self.addNode(data)

    def _updateNodeLabel(self, node, label):
        """Update the label value of the node in the graph.

        Args:
            node (subclass of GraphNodeBase): The node object to be updated. Can be a graph/tree/linked_list node.
            label (printable): New label content.
        """
        if label is None:
            label = ''
        self._nodes_label_update[node] = label

    def _update_svg_nodes_label(self, svg, node_idmap):
        time0 = (0, self._delay * 0.5)
        time1 = (self._delay * 0.6, self._delay)
        for node, old_label in self._nodes_label_update.items():
            node_id = 'node{}'.format(node_idmap.toConsecutiveId(node))
            svg_node = find_tag_by_id(svg, 'g', node_id)
            if svg_node is None:
                return
            ellipse = svg_node.getElementsByTagName('ellipse')[0]
            cx = float(ellipse.getAttribute('cx'))
            cy = float(ellipse.getAttribute('cy'))
            fill_str = ellipse.getAttribute('fill')
            if fill_str == 'none':
                fc = (255, 255, 255)
            else:
                fc = str2rgbcolor(fill_str)
            # Add animation zoom in for current text node.
            text_nodes = svg_node.getElementsByTagName('text')
            for t in text_nodes:
                font_size = float(t.getAttribute('font-size'))
                animate0 = svg.createElement('animate')
                add_animate_scale_into_text(t, animate0, time0, font_size, False)
            # New text node for animation zoom out.
            t1 = svg.createElement('text')
            t1.setAttribute('alignment-baseline', 'middle')
            t1.setAttribute('text-anchor', 'middle')
            t1.setAttribute('font-family', 'Times,serif')
            t1.setAttribute('x', '{:.2f}'.format(cx))
            t1.setAttribute('y', '{:.2f}'.format(cy))
            font_size = min(14, text_font_size(32, '{}'.format(old_label)))
            t1.setAttribute('font-size', '{:.2f}'.format(0))
            t1.setAttribute('fill', auto_text_color(fc))
            tt = svg.createTextNode('{}'.format(old_label))
            t1.appendChild(tt)
            animate1 = svg.createElement('animate')
            add_animate_scale_into_text(t1, animate1, time1, font_size, True)
            svg_node.appendChild(t1)

    def _updateEdgeLabel(self, node1, node2, label):
        """Update the label value of the node in the graph.

        Args:
            node (subclass of GraphNodeBase): The begin and end node in the edge to be updated. Can be a graph/tree/linked_list node.
            label (printable): New label content.
        """
        edge_key = self._make_edge_tuple_(node1, node2)
        if label is None:
            label = ''
        self._edges_lable_update[edge_key] = label

    def _update_svg_edges_label(self, svg, edge_idmap):
        time0 = (0, self._delay * 0.5)
        time1 = (self._delay * 0.6, self._delay)
        for edge_key, old_label in self._edges_lable_update.items():
            edge_id = 'edge{}'.format(edge_idmap.toConsecutiveId(edge_key))
            svg_node = find_tag_by_id(svg, 'g', edge_id)
            if svg_node is None:
                return
            text_nodes = svg_node.getElementsByTagName('text')
            t0 = None
            for t in text_nodes:
                font_size = float(t.getAttribute('font-size'))
                animate0 = svg.createElement('animate')
                add_animate_scale_into_text(t, animate0, time0, font_size, False)
                t0 = t
            if t0 is not None:
                t1 = t0.cloneNode(deep=False)
                tt = svg.createTextNode('{}'.format(old_label))
                t1.appendChild(tt)
                font_size = float(t1.getAttribute('font-size'))
                t1.setAttribute('font-size', '0')
                animate1 = svg.createElement('animate')
                add_animate_scale_into_text(t1, animate1, time1, font_size, True)
                svg_node.appendChild(t1)

    def _repr_svg_(self):
        """Render the graph into SVG and add animation effects.

        Returns:
            str: SVG string to representation graph nodes and edges with animation.
        """
        # Sequence the graph and add animation effects.
        self._traverse_graph_()
        (new_svg, node_idmap, edge_idmap) = self._create_svg_()
        add_desc_into_svg(new_svg)
        self._update_svg_size_(new_svg)
        self._update_svg_(new_svg, node_idmap, edge_idmap)
        self._update_trace_color_()
        self._compress_svg_()
        res = self._svg.toxml()
        # Update the SVG content and prepare for the next frame.
        self._svg, self._node_idmap, self._edge_idmap = new_svg, node_idmap, edge_idmap
        new_nodes = self._get_node_pos_(self._svg)
        for node_id in new_nodes.keys():
            node = self._node_idmap.toAttributeId(node_id)
            self._update_node_color_(new_nodes[node_id][0], self._node_tcs[node].color())
        new_edges = self._get_svg_edges_(self._svg)
        for edge_id in new_edges.keys():
            edge = self._edge_idmap.toAttributeId(edge_id)
            self._update_edge_color_(new_edges[edge_id], self._edge_tcs[edge].color())
        # Update auxiliary data caches.
        for node in self._node_disappear:
            self._node_tcs.pop(node)
        for edge in self._edge_disappear:
            self._edge_tcs.pop(edge)
        self._node_appear.clear()
        self._node_disappear.clear()
        self._edge_appear.clear()
        self._edge_disappear.clear()
        self._node_move.clear()
        return res.replace('\n', '')

    def _compress_svg_(self):
        graphs = self._svg.getElementsByTagName('g')
        for graph in graphs:
            if graph.getAttribute('class') != 'graph':
                continue
            nodes_to_remove = list()
            for node in graph.childNodes:
                if node.nodeType == node.COMMENT_NODE:
                    nodes_to_remove.append(node)
                elif node.nodeType == node.ELEMENT_NODE:
                    if node.getAttribute('class') == 'node':
                        titles = node.getElementsByTagName('title')
                        for title in titles:
                            node.removeChild(title)
                            pass
                    elif node.getAttribute('class') == 'edge':
                        titles = node.getElementsByTagName('title')
                        for title in titles:
                            title_content = title.firstChild.data
                            if self._directed:
                                title_content = title_content.split('->')
                            else:
                                title_content = title_content.split('--')
                            node.removeChild(title)
                    elif node.tagName == 'title':
                        nodes_to_remove.append(node)
            for node in nodes_to_remove:
                graph.removeChild(node)

    def _traverse_graph_(self):
        """Traverse each node in the graph and update the related data structure.
        """
        # Traverse the nodes in the graph and record the new topology structure of this graph.
        new_node_seq = list()
        new_edge_label = dict()
        visited = set(self._remove_nodes)
        node_stack = self._node_seq + self._add_nodes
        node_stack.reverse()
        while len(node_stack) > 0:
            cur_node = node_stack.pop()
            if cur_node is None or cur_node in visited:
                continue
            visited.add(cur_node)
            new_node_seq.append(cur_node)
            for neigh in cur_node._neighbors_()[::-1]:
                if neigh[0] is not None and neigh[0] not in self._remove_nodes:
                    temp_edge = self._make_edge_tuple_(cur_node, neigh[0])
                    new_edge_label[temp_edge] = neigh[1]
                    node_stack.append(neigh[0])
        # Update the newly added and disappeared edges and nodes.
        old_node_set = set(self._node_seq)
        new_node_set = set(new_node_seq)
        self._node_appear = new_node_set - old_node_set
        self._node_disappear = old_node_set - new_node_set
        self._edge_appear = new_edge_label.keys() - self._edge_label.keys()
        self._edge_disappear = self._edge_label.keys() - new_edge_label.keys()
        # Update the cached track color information.
        for node in self._node_appear:
            if node not in self._node_tcs.keys():
                self._node_tcs[node] = TraceColorStack()
        for edge in self._edge_appear:
            if edge not in self._edge_tcs.keys():
                self._edge_tcs[edge] = TraceColorStack(bgcolor=(123, 123, 123))
        # Update other auxiliary data.
        self._node_seq = new_node_seq
        self._edge_label = new_edge_label
        self._add_nodes.clear()
        self._remove_nodes.clear()

    def _update_node_color_(self, node, color):
        """Update the color attribute of the node in SVG.

        Args:
            node (xmldom.Node): The node to be updated in SVG.
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        """
        if node is not None:
            ellipse = node.getElementsByTagName('ellipse')[0]
            ellipse.setAttribute('fill', rgbcolor2str(color))
            text_list = node.getElementsByTagName('text')
            if text_list and len(text_list) > 0:
                text = text_list[0]
                if text is not None:
                    text.setAttribute('fill', auto_text_color(color))

    def _update_edge_color_(self, edge, color):
        """Update the color attribute of the edge in SVG.

        Args:
            edge (xmldom.Node): The edge to be updated in SVG.
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        """
        if edge is not None:
            path = edge.getElementsByTagName('path')[0]
            path.setAttribute('stroke', rgbcolor2str(color))
            polygons = edge.getElementsByTagName('polygon')
            if len(polygons) > 0:
                polygons[0].setAttribute('fill', rgbcolor2str(color))
                polygons[0].setAttribute('stroke', rgbcolor2str(color))

    def _update_trace_color_(self):
        """Update the color change of the SVG track in the frame.
        """
        for k, color in self._frame_trace_old:
            if type(k) == tuple and k in self._edge_tcs.keys():
                if (k, color, False) not in self._frame_trace and (k, color, True) not in self._frame_trace:
                    self._edge_tcs[k].remove(color)
                edge_id = 'edge{}'.format(self._edge_idmap.toConsecutiveId(k))
                edge = find_tag_by_id(self._svg, 'g', edge_id)
                self._update_edge_color_(edge, self._edge_tcs[k].color())
            elif k in self._node_tcs.keys():
                if (k, color, False) not in self._frame_trace and (k, color, True) not in self._frame_trace:
                    self._node_tcs[k].remove(color)
                node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(k))
                node = find_tag_by_id(self._svg, 'g', node_id)
                self._update_node_color_(node, self._node_tcs[k].color())
        self._frame_trace_old.clear()
        for k, color, hold in self._frame_trace:
            if type(k) == tuple:
                edge_id = 'edge{}'.format(self._edge_idmap.toConsecutiveId(k))
                edge = find_tag_by_id(self._svg, 'g', edge_id)
                self._update_edge_color_(edge, self._edge_tcs[k].color())
            else:
                node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(k))
                node = find_tag_by_id(self._svg, 'g', node_id)
                self._update_node_color_(node, self._node_tcs[k].color())
            if not hold:
                self._frame_trace_old.append((k, color))
        self._frame_trace.clear()

    def _update_svg_size_(self, new_svg):
        """Adjust the view size of self._svg to ensure that all elements can be observed.

        Args:
            new_svg (xmldom.Document): The latest SVG object to be updated.
        """
        old_svg_node = self._svg.getElementsByTagName('svg')[0]
        new_svg_node = new_svg.getElementsByTagName('svg')[0]
        old_svg_width = int(old_svg_node.getAttribute('width')[0:-2])
        old_svg_height = int(old_svg_node.getAttribute('height')[0:-2])
        new_svg_width = int(new_svg_node.getAttribute('width')[0:-2])
        new_svg_height = int(new_svg_node.getAttribute('height')[0:-2])
        width = max(old_svg_width, new_svg_width)
        height = max(old_svg_height, new_svg_height)
        old_svg_node.setAttribute('width', '{}pt'.format(width))
        old_svg_node.setAttribute('height', '{}pt'.format(height))
        old_svg_node.setAttribute('viewBox', '0.00 0.00 {:.2f} {:.2f}'.format(width, height))
        graph = find_tag_by_id(new_svg, 'g', 'graph0')
        clone_graph = graph.cloneNode(deep=False)
        clone_graph.setAttribute('id', 'graph1')
        old_svg_node.appendChild(clone_graph)

    def _update_svg_(self, new_svg, node_idmap, edge_idmap):
        """Add all node and edge related animations into SVG.

        Args:
            new_svg (xmldom.Doucment): The latest SVG object to be updated.
            node_idmap (ConsecutiveIdMap): The two-way mapping relationship between the node ID in the memory and the ID in the SVG.
            edge_idmap (ConsecutiveIdMap): The two-way mapping relationship between the edge ID in the memory and the ID in the SVG.
        """
        old_pos = self._get_node_pos_(self._svg)
        new_pos = self._get_node_pos_(new_svg)
        old_edges = self._get_svg_edges_(self._svg)
        new_edges = self._get_svg_edges_(new_svg)
        has_disappear_animate = False
        disappear_animate_end_time = self._delay * 0.2
        # Add the disappearing animation effect for the graph nodes.
        for old_node_id in old_pos.keys():
            old_node = self._node_idmap.toAttributeId(old_node_id)
            if old_node in self._node_disappear:
                g = old_pos[old_node_id][0]
                animate = self._svg.createElement('animate')
                add_animate_appear_into_node(g, animate, (0, disappear_animate_end_time), False)
                has_disappear_animate = True
        # Update self._node_move because we need to use it when add disappearing animation effor for edges.
        for old_node_id in old_pos.keys():
            old_node = self._node_idmap.toAttributeId(old_node_id)
            if old_node in node_idmap._attr2id.keys():
                new_node_id = node_idmap.toConsecutiveId(old_node)
                delt_x = new_pos[new_node_id][1] - old_pos[old_node_id][1]
                delt_y = new_pos[new_node_id][2] - old_pos[old_node_id][2]
                if abs(delt_x) > 0.001 or abs(delt_y) > 0.001:  # Minimum delt move check.
                    self._node_move.add(old_node)
        # Add the disappearing animation effect for the edge.
        for old_edge_id in old_edges.keys():
            (node1, node2) = self._edge_idmap.toAttributeId(old_edge_id)  # The ID value of the edge (start_node, end_node) in the memory.
            if (node1, node2) in self._edge_disappear or node1 in self._node_move or node2 in self._node_move:
                g = old_edges[old_edge_id]
                animate = self._svg.createElement('animate')
                add_animate_appear_into_node(g, animate, (0, disappear_animate_end_time), False)
                has_disappear_animate = True
        # Add the moving animation effect for the graph nodes.
        has_move_animate = False
        move_animate_start_time = disappear_animate_end_time if has_disappear_animate else 0
        move_animate_end_time = move_animate_start_time + (self._delay - move_animate_start_time) * 0.6
        for old_node_id in old_pos.keys():
            old_node = self._node_idmap.toAttributeId(old_node_id)
            if old_node in node_idmap._attr2id.keys():
                new_node_id = node_idmap.toConsecutiveId(old_node)
                delt_x = new_pos[new_node_id][1] - old_pos[old_node_id][1]
                delt_y = new_pos[new_node_id][2] - old_pos[old_node_id][2]
                if abs(delt_x) > 0.001 or abs(delt_y) > 0.001:  # Minimum delt move check.
                    g = old_pos[old_node_id][0]
                    animate = self._svg.createElement('animateMotion')
                    move = (delt_x, delt_y)
                    add_animate_move_into_node(g, animate, move, (move_animate_start_time, move_animate_end_time), False)
                    has_move_animate = True
        # Add the appearing animation effect for the graph nodes.
        graph = find_tag_by_id(self._svg, 'g', 'graph1')
        appear_animate_start_time = move_animate_end_time if has_move_animate else move_animate_start_time
        for old_node in self._node_appear:
            new_node_id = node_idmap.toConsecutiveId(old_node)
            old_node_id = self._node_idmap.toConsecutiveId(old_node)
            clone_node = new_pos[new_node_id][0].cloneNode(deep=True)
            clone_node.setAttribute('id', 'node{}'.format(old_node_id))
            graph.appendChild(clone_node)
            animate = self._svg.createElement('animate')
            add_animate_appear_into_node(clone_node, animate, (appear_animate_start_time, self._delay), True)
        # Add the appearing animation effect for the graph edges.
        graph = find_tag_by_id(self._svg, 'g', 'graph1')
        for new_edge_id in new_edges.keys():
            (node1, node2) = edge_idmap.toAttributeId(new_edge_id)
            if (node1, node2) in self._edge_appear or node1 in self._node_move or node2 in self._node_move:
                old_edge_id = self._edge_idmap.toConsecutiveId((node1, node2))
                clone_edge = new_edges[new_edge_id].cloneNode(deep=True)
                clone_edge.setAttribute('id', 'edge{}'.format(old_edge_id))
                graph.appendChild(clone_edge)
                animate = self._svg.createElement('animate')
                add_animate_appear_into_node(clone_edge, animate, (appear_animate_start_time, self._delay), True)
        # Add node/edge label text zoom in/out animations.
        self._update_svg_nodes_label(self._svg, self._node_idmap)
        self._nodes_label_update.clear()
        self._update_svg_edges_label(self._svg, self._edge_idmap)
        self._edges_lable_update.clear()

    def _get_node_pos_(self, svg):
        """Get the absolute coordinates of all the graph node(s) in the SVG.

        Args:
            svg (xmldom.Document): The SVG object to be display.

        Returns:
            dict(int:tuple(xmldom.Node,float,float)): The map from SVG_node_id to the SVG_node_object and node position.
                Key is SVG_node_id, value is (SVG_node_object, position_x, position_y).
        """
        graph = find_tag_by_id(svg, 'g', 'graph0')
        transform = graph.getAttribute('transform')
        translate_index = transform.find('translate')
        delt_x, delt_y = 0, 0
        if translate_index != -1:
            st = transform.find('(', translate_index) + 1
            ed = transform.find(')', translate_index)
            translate = transform[st:ed].split(' ')
            delt_x, delt_y = float(translate[0]), float(translate[1])
        positions = dict()
        nodes = svg.getElementsByTagName('g')
        for node in nodes:
            if node.getAttribute('class') == 'node':
                node_id = int(node.getAttribute('id')[4:])
                ellipse = node.getElementsByTagName('ellipse')[0]
                cx = float(ellipse.getAttribute('cx')) + delt_x
                cy = float(ellipse.getAttribute('cy')) + delt_y
                positions[node_id] = (node, cx, cy)
        return positions

    def _get_svg_edges_(self, svg):
        """Get all the edges index and object in the SVG xml tree.

        Args:
            svg (xmldom.Document): The SVG object to be display.

        Returns:
            dict(int:xmldom.Node): Key is the edge index in SVG, Value is the edge node in SVG.
        """
        edges = dict()
        nodes = svg.getElementsByTagName('g')
        for node in nodes:
            if node.getAttribute('class') == 'edge':
                edge_id = int(node.getAttribute('id')[4:])
                edges[edge_id] = node
        return edges

    def _make_edge_tuple_(self, node1, node2):
        """Create an edge tuple according to nodes and the graph's type.

        Args:
            node1, node2 (subclass of GraphNodeBase): The begin and end node in the edge. Can be a graph/tree/linked_list node.
        """
        if self._directed:
            return (node1, node2)
        else:
            if id(node1) < id(node2):
                return (node1, node2)
            else:
                return (node2, node1)

    def _create_svg_(self):
        """Call graphviz lib to create a new SVG object to represent the latest graph.
        The SVG is static and don't include animations.

        Returns:
            xmldom.Document: The xmldom.Document object of the SVG.

        Raises:
            AlgvizFatalError: Unsupported graphviz version xxx.
        """
        dot = None
        node_idmap = ConsecutiveIdMap(1)
        edge_idmap = ConsecutiveIdMap(1)
        if self._directed:
            dot = graphviz_Digraph(format='svg')
        else:
            dot = graphviz_Graph(format='svg', engine='neato')
        if self._type.rankdir == 'LR':
            dot.graph_attr['rankdir'] = 'LR'
        dot.graph_attr['bgcolor'] = '#00000000'
        dot.node_attr.update(shape=self._type.shape, fixedsize='shape', color='#7B7B7B')
        dot.edge_attr.update(arrowhead='vee', color='#7B7B7B')
        for node in self._node_seq:
            node_id = node_idmap.toConsecutiveId(node)
            if node is None:
                dot.node(name='{}'.format(node_id))
            else:
                fs = min(14, text_font_size(32, str(node)))
                dot.node(name='{}'.format(node_id), label='{}'.format(str(node)), fontsize='{:.2f}'.format(fs))
        for (node1, node2) in self._edge_label.keys():
            label = self._edge_label[(node1, node2)]
            node1_id = node_idmap.toConsecutiveId(node1)
            node2_id = node_idmap.toConsecutiveId(node2)
            if label is None:
                dot.edge('{}'.format(node1_id), '{}'.format(node2_id))
            else:
                dot.edge('{}'.format(node1_id), '{}'.format(node2_id), label='{}'.format(label), fontcolor='#C0C0C0', fontsize='12')
            edge_idmap.toConsecutiveId((node1, node2))
        raw_svg_str = ''
        try:
            callable(getattr(dot, '_repr_svg_'))
            raw_svg_str = dot._repr_svg_()
        except Exception:
            try:
                # graphviz replaced interface '_repr_svg_' since version 0.19 (https://graphviz.readthedocs.io/en/stable/changelog.html#version-0-19)
                callable(getattr(dot, '_repr_image_svg_xml'))
                raw_svg_str = dot._repr_image_svg_xml()
            except Exception:
                raise AlgvizFatalError('Unsupported graphviz version {}'.format(graphviz_version))
        return (mindom_parseString(raw_svg_str), node_idmap, edge_idmap)
