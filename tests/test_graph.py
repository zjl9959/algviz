#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''


import algviz
from result import TestResult
from utility import equal, equal_table, get_graph_elements


def test_create_graph():
    res = TestResult()
    viz = algviz.Visualizer()
    # Test create directed graph.
    nodes = [0, 1, 2, 3, 4, 5, 6, 7]
    edges = [
        [0, 3, None], [1, 0, 'e1_0'], [2, 0, None],
        [3, 5, 'e3_5'], [4, 1, None], [4, 6, None],
        [5, 2, 'e5_2'], [5, 4, None],
    ]
    graph_nodes = algviz.parseGraph(nodes, edges, {7:'node_7'})
    graph = viz.createGraph(graph_nodes)
    svg_nodes, svg_edges = get_graph_elements(graph._repr_svg_())
    expect_nodes = [0, 1, 2, 3, 4, 5, 6, 'node_7']
    res.add_case(equal(expect_nodes, svg_nodes) and equal_table(edges, svg_edges), 'Create directed graph',
                'nodes:{};edges:{}'.format(svg_nodes, svg_edges), 'nodes:{};edges:{}'.format(expect_nodes, edges))
    # Test create undirected graph.
    nodes = [0, 1, 2, 3, 4, 5, 6, 7]
    edges = [
        [0, 1, 'e1_0'], [0, 2, None], [0, 3, None],
        [1, 4, None], [2, 5, 'e5_2'], [3, 5, 'e3_5'],
        [4, 5, None], [4, 6, None],
    ]
    graph_nodes = algviz.parseGraph(nodes, edges, {7:'node_7'}, directed=False)
    graph = viz.createGraph(graph_nodes, directed=False)
    svg_nodes, svg_edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(expect_nodes, svg_nodes) and equal_table(edges, svg_edges), 'Create undirected graph',
                'nodes:{};edges:{}'.format(svg_nodes, svg_edges), 'nodes:{};edges:{}'.format(expect_nodes, edges))
    return res


def test_traverse_graph():
    res = TestResult()
    viz = algviz.Visualizer()
    # Test traverse graph directed graph.
    nodes = [0, 1, 2, 3, 4, 5, 6]
    edges = [[0, 3], [1, 0], [2, 0], [3, 5], [4, 6], [4, 1], [5, 4], [5, 2]]
    graph_nodes = algviz.parseGraph(nodes, edges)
    graph = viz.createGraph(graph_nodes)
    visit_res, visited_nodes = list(), set()
    def traverse_graph(root):
        if root and root not in visited_nodes:
            visit_res.append(root.val)
            root.val += 1
            visited_nodes.add(root)
            for ne, _ in root.neighbors():
                traverse_graph(ne)
    traverse_graph(graph_nodes[0])
    visit_res = sorted(visit_res)
    res.add_case(equal(nodes, visit_res), 'Traverse directed graph', visit_res, nodes)
    # Test update graph node value.
    svg_nodes, _ = get_graph_elements(graph._repr_svg_())
    nodes = [i+1 for i in nodes]
    res.add_case(equal(nodes, svg_nodes), 'Update node value', svg_nodes, nodes)
    # Test traverse undirected graph.
    nodes = [0, 1, 2, 3, 4, 5, 6]
    edges = [[0, 3], [1, 0], [2, 0], [3, 5], [4, 6], [4, 1], [5, 4], [5, 2]]
    graph_nodes = algviz.parseGraph(nodes, edges, directed=False)
    visit_res, visited_nodes = list(), set()
    traverse_graph(graph_nodes[2])
    visit_res = sorted(visit_res)
    res.add_case(equal(nodes, visit_res), 'Traverse undirected graph', visit_res, nodes)
    return res


def test_modify_graph():
    res = TestResult()
    # TODO: add subcases.
    return res


def test_mark_graph():
    res = TestResult()
    # TODO: add subcases.
    return res
