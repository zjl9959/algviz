#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''


import algviz
from algviz.graph import parseGraph, generateRandomGraph, AlgvizRuntimeError
from result import TestResult
from utility import equal, equal_table, get_graph_elements, hack_graph
from utility import TestCustomPrintableClass


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
    graph_nodes = algviz.parseGraph(nodes, edges, {7: 'node_7'})
    graph = viz.createGraph(graph_nodes)
    hack_graph(graph)
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
    graph_nodes = algviz.parseGraph(nodes, edges, {7: 'node_7'}, directed=False)
    graph = viz.createGraph(graph_nodes, directed=False)
    hack_graph(graph)
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
    hack_graph(graph)
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
    nodes = [i + 1 for i in nodes]
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


def test_modify_directed_graph():
    res = TestResult()
    viz = algviz.Visualizer()
    graph_nodes = algviz.parseGraph([0, 1, 2], [[0, 1, None],
                                    [0, 2, 'e0_2'], [2, 1, None]])
    graph = viz.createGraph(graph_nodes)
    hack_graph(graph)
    # Test add nodes into directed graph.
    node3 = algviz.GraphNode(3)
    node2 = graph_nodes[2]
    custom_edge = TestCustomPrintableClass('e2', 'e3')
    node2.add(node3, custom_edge)
    sub_graph_nodes = algviz.parseGraph([4, 5, 6], [[4, 5, None],
                                        [5, 6, 'e5_6'], [6, 4, None]])
    node3.add(sub_graph_nodes[4])
    expect_nodes = [0, 1, 2, 3, 4, 5, 6]
    expect_edges = [
        [0, 1, None], [0, 2, 'e0_2'], [2, 1, None],
        [2, 3, custom_edge], [3, 4, None],
        [4, 5, None], [5, 6, 'e5_6'], [6, 4, None]
    ]
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Add nodes',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    assert graph_nodes[2].neighborCount() == 2
    assert sub_graph_nodes[4].neighborCount() == 1
    # Test neighborIndex interface.
    expect_res = [0, 1, 0]
    actual_res = [
        graph_nodes[2].neighborIndex(graph_nodes[1]),
        graph_nodes[2].neighborIndex(node3),
        node3.neighborIndex(sub_graph_nodes[4]),
    ]
    res.add_case(equal(expect_res, actual_res), 'neighborIndex', actual_res, actual_res)
    # Test neighborAt interface.
    expect_res = [5, 3, 1]
    actual_res = [
        sub_graph_nodes[4].neighborAt(0)[0],
        graph_nodes[2].neighborAt(1)[0],
        graph_nodes[2].neighborAt(0)[0],
    ]
    res.add_case(equal(expect_res, actual_res), 'neighborAt', actual_res, expect_res)
    # Test remove node neighbors.
    node3.remove(sub_graph_nodes[4])
    node2.remove(graph_nodes[1])
    expect_edges = [
        [0, 1, None], [0, 2, 'e0_2'],
        [2, 3, custom_edge],
        [4, 5, None], [5, 6, 'e5_6'], [6, 4, None]
    ]
    graph._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Remove node neighbors',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test remove nodes in graph.
    graph.removeNode(sub_graph_nodes[4], True)  # Remove all the subgraph.
    graph.removeNode(graph_nodes[1])
    expect_nodes = [0, 1, 2, 3]
    expect_edges = [[0, 1, None], [0, 2, 'e0_2'], [2, 3, custom_edge]]
    graph._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Remove nodes(1)',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test remove nodes in graph.
    graph_nodes[0].remove(graph_nodes[1])
    graph.removeNode(graph_nodes[1])
    expect_nodes = [0, 2, 3]
    expect_edges = [[0, 2, 'e0_2'], [2, 3, custom_edge]]
    graph._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Remove nodes(2)',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test update graph edge.
    algviz.updateGraphEdge(node2, node3, -23)
    expect_edges = [[0, 2, 'e0_2'], [2, 3, -23]]
    graph._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Update edge',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test add/removeAt interfaces.
    expect_nodes = [2, 3, 7]
    expect_edges = [[2, 3, -23], [2, 7, 'e2_7']]
    graph_nodes[2].add(algviz.GraphNode(7), 'e2_7', 0)
    graph_nodes[0].removeAt(0)
    graph.removeNode(graph_nodes[0])
    graph._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'add/removeAt',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    return res


def test_modify_undirected_graph():
    res = TestResult()
    viz = algviz.Visualizer()
    nodes = [0, 1, 2, 3]
    edges = [[0, 1, None], [1, 2, None], [2, 3, '2<->3'], [3, 0, '3<->0']]
    graph_nodes = parseGraph(nodes, edges, directed=False)
    graph = viz.createGraph(graph_nodes, directed=False)
    hack_graph(graph)
    # Test add nodes into undirected graph.
    node4 = algviz.GraphNode(4)
    node5 = algviz.GraphNode(5)
    graph_nodes[0].add(node4)
    node4.add(graph_nodes[2])
    graph_nodes[1].add(node5)
    node5.add(graph_nodes[3], '3<->5')
    expect_nodes = [0, 1, 2, 3, 4, 5]
    expect_edges = [
        [0, 1, None], [0, 3, '3<->0'], [0, 4, None],
        [1, 2, None], [1, 5, None],
        [2, 3, '2<->3'], [2, 4, None], [3, 5, '3<->5']]
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Add nodes',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test remove nodes from undirected graph.
    graph_nodes[2].remove(graph_nodes[1])
    graph_nodes[1].remove(graph_nodes[2])
    graph_nodes[2].remove(graph_nodes[3])
    graph_nodes[3].remove(graph_nodes[2])
    node4.remove(graph_nodes[2])
    assert graph.removeNode(graph_nodes[2]) == 1
    expect_nodes = [0, 1, 3, 4, 5]
    expect_edges = [
        [0, 1, None], [0, 3, '3<->0'], [0, 4, None],
        [1, 5, None], [3, 5, '3<->5']]
    graph._repr_svg_()
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Remove nodes',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    return res


def test_generate_random_graph():
    res = TestResult()
    # Test generate an undirected graph.
    try:
        nodes, edges = generateRandomGraph(5, 8, 4)
        assert len(nodes) == 5
        assert len(edges) == 8
        res.add_case(True, 'Generate undirected graph')
    except AlgvizRuntimeError as e:
        # Not ensure must generate a valid graph.
        print('test_generate_random_undirected_graph exception:', e)
        res.add_case(True, 'Generate undirected graph')
    except Exception as e:
        print('test_generate_random_undirected_graph exception:', e)
        res.add_case(False, 'Generate undirected graph')
    # Test generate an directed graph.
    try:
        nodes, edges = generateRandomGraph(5, 10, 5, True)
        assert len(nodes) == 5
        assert len(edges) == 10
        res.add_case(True, 'Generate directed graph')
    except AlgvizRuntimeError as e:
        # Not ensure must generate a valid graph.
        print('test_generate_random_directed_graph exception:', e)
        res.add_case(True, 'Generate directed graph')
    except Exception as e:
        print('test_generate_random_directed_graph exception:', e)
        res.add_case(False, 'Generate directed graph')
    return res
