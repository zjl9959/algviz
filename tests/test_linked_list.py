#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from result import TestResult
import algviz
from utility import equal_table, get_graph_elements, equal


def test_create_forward_list():
    res = TestResult()
    viz = algviz.Visualizer()
    # Test create a normal list.
    head = algviz.parseForwardLinkedList([1, 2, 'tail'])
    graph = viz.createGraph(head)
    nodes, edges = get_graph_elements(graph._repr_svg_())
    expect_nodes = [1, 2, 'tail']
    expect_edges = [(1, 2, None), (2, 'tail', None)]
    res.add_case(equal(nodes, expect_nodes) and equal_table(edges, expect_edges), 'Normal forward list',
                'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test create an empty list.
    head = algviz.parseForwardLinkedList([])
    graph = viz.createGraph(head)
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(nodes, []) and equal(edges, []), 'Empty forward list',
                'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format([], []))
    return res

