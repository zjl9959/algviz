#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''


import xml.dom.minidom as xmldom


class TestCustomPrintableClass:
    '''
    @class: This class used to test if display objects can display self defined class noramlly.
    '''
    
    def __init__(self, v1, v2) -> None:
        self._v1 = v1
        self._v2 = v2

    def __repr__(self) -> str:
        return '{}->{}'.format(self._v1, self._v2)


def equal(lhs, rhs, type=str):
    '''
    @function: Check if object lhs equal with rhs.
    @param: {lhs,rhs->iterable(printable)}.
    @return: {bool} Wheather lhs equal with rhs or not.
    '''
    if len(lhs) != len(rhs):
        return False
    for i in range(len(lhs)):
        if type(lhs[i]) != type(rhs[i]):
            return False
    return True


def equal_table(lhs, rhs, type=str):
    '''
    @function: Check if object lhs equal with rhs.
    @param: {lhs,rhs->iteratble(iterable(printable))}.
    @return: {bool} Wheather lhs equal with rhs or not.
    '''
    if len(lhs) != len(rhs):
        return False
    for r in range(len(lhs)):
        if len(lhs[r]) != len(rhs[r]):
            return False
        for c in range(len(lhs[r])):
            if type(lhs[r][c]) != type(rhs[r][c]):
                return False
    return True


def get_graph_elements(svg_str):
    '''
    @function: Parse graph nodes and edges from it's display SVG string.
    @param: {svg_str->str} The graph SVG display string.
    @return: {list(str), list(tuple(str))} List of graph nodes and graph edges.
    '''
    def get_node_title_and_label(node):
        # Get node title.
        titles = node.getElementsByTagName('title')
        if not titles or len(titles) != 1:
            return None, None
        node_title = titles[0].firstChild.data
        # Get node label.
        label = None
        texts = node.getElementsByTagName('text')
        for text in texts:
            if text.getAttribute('text-anchor') == 'middle' and text.firstChild:
                label = text.firstChild.data
        return node_title, label

    node_id2label, res_edges = dict(), list()
    svg = xmldom.parseString(svg_str)
    svg_nodes = svg.getElementsByTagName('g')
    # Parse all the nodes in graph.
    for node in svg_nodes:
        if node.getAttribute('class') == 'node':
            node_id, node_val = get_node_title_and_label(node)
            if not node_id:
                continue
            node_id2label[node_id] = node_val
    # Parse all the edges in graph.
    for node in svg_nodes:
        if node.getAttribute('class') == 'edge':
            title, edge_val = get_node_title_and_label(node)
            if not node_id:
                continue
            title = title.split('->')
            if len(title) != 2:
                continue
            start_node, end_node = title[0], title[1]
            start_node_val = node_id2label[start_node]
            end_node_val = node_id2label[end_node]
            res_edges.append((start_node_val, end_node_val, edge_val))
    return sorted(list(node_id2label.values())), sorted(res_edges)
