#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from utility import equal, equal_table, get_graph_elements, hack_graph
from result import TestResult
import algviz


def test_create_map():
    res = TestResult()
    viz = algviz.Visualizer()
    # Test create an empty map object.
    map1 = viz.createMap(name='map1')
    svg_nodes, svg_edges = get_graph_elements(map1._repr_svg_())
    expect_nodes = []
    expect_edges = []
    res.add_case(equal(expect_nodes, svg_nodes) and equal_table(expect_edges, svg_edges), 'Create an empty map',
                 'nodes:{};edges:{}'.format(svg_nodes, svg_edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test create a normal map object.
    map2 = viz.createMap({1: 'a', 2: 'b', 3: 'def'}, 'map')
    hack_graph(map2._graph)
    svg_nodes, svg_edges = get_graph_elements(map2._repr_svg_())
    expect_nodes = [1, 2, 3, 'a', 'b', 'def']
    expect_edges = [[1, 'a', None], [2, 'b', None], [3, 'def', None]]
    res.add_case(equal(expect_nodes, svg_nodes) and equal_table(expect_edges, svg_edges), 'Create a normal map',
                 'nodes:{};edges:{}'.format(svg_nodes, svg_edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    return res


def test_iterate_on_map():
    res = TestResult()
    viz = algviz.Visualizer()
    map = viz.createMap({1: 'a', 2: 'b', 3: 'def'})
    # Test iterate on keys.
    except_values = [1, 2, 3]
    iter_values = []
    for k in map.keys():
        iter_values.append(k)
    res.add_case(equal(except_values, iter_values), 'Iterate on keys', iter_values, except_values)
    # Test iterate on values.
    except_values = ['a', 'b', 'def']
    iter_values = []
    for v in map.values():
        iter_values.append(v)
    res.add_case(equal(except_values, iter_values), 'Iterate on values', iter_values, except_values)
    # Test iterate on items.
    except_values = [(1, 'a'), (2, 'b'), (3, 'def')]
    iter_values = []
    for k, v in map.items():
        iter_values.append((k, v))
    res.add_case(equal(except_values, iter_values), 'Iterate on items', iter_values, except_values)
    # Test contains operation.
    assert 1 in map
    assert 4 not in map
    return res


def test_modify_items():
    res = TestResult()
    viz = algviz.Visualizer()
    map = viz.createMap({1: 'a', 2: 'b', 3: 'def'})
    # Test get item.
    assert map.get(1) == 'a'
    assert map[2] == 'b'
    # Test set item.
    map[3] = 'c'
    map[4] = 'd'
    expect_nodes = [1, 2, 3, 4, 'a', 'b', 'c', 'd']
    expect_edges = [[1, 'a', None], [2, 'b', None], [3, 'c', None], [4, 'd', None]]
    hack_graph(map._graph)
    svg_nodes, svg_edges = get_graph_elements(map._repr_svg_())
    res.add_case(equal(expect_nodes, svg_nodes) and equal_table(expect_edges, svg_edges), 'Set item',
                 'nodes:{};edges:{}'.format(svg_nodes, svg_edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test pop item.
    assert map.pop(3) == 'c'
    assert map.pop(5) is None
    assert map.pop(6, 'error') == 'error'
    expect_nodes = [1, 2, 4, 'a', 'b', 'd']
    expect_edges = [[1, 'a', None], [2, 'b', None], [4, 'd', None]]
    hack_graph(map._graph)
    map._repr_svg_()    # Refresh the animation.
    svg_nodes, svg_edges = get_graph_elements(map._repr_svg_())
    res.add_case(equal(expect_nodes, svg_nodes) and equal_table(expect_edges, svg_edges), 'Pop item',
                 'nodes:{};edges:{}'.format(svg_nodes, svg_edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test clear items.
    map.clear()
    expect_nodes = []
    expect_edges = []
    hack_graph(map._graph)
    map._repr_svg_()    # Refresh the animation.
    svg_nodes, svg_edges = get_graph_elements(map._repr_svg_())
    res.add_case(equal(expect_nodes, svg_nodes) and equal_table(expect_edges, svg_edges), 'Clear map',
                 'nodes:{};edges:{}'.format(svg_nodes, svg_edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    return res
