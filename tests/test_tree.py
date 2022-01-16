#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

import algviz
from result import TestResult
from utility import equal, equal_table, get_graph_elements

def test_binary_tree():
    res = TestResult()
    viz = algviz.Visualizer()
    '''
    # Test create a binary tree like this:
            1
           / \
          2   3
         / \   \
        4   5   6
    '''
    tree_nodes1 = [1, 2, 3, 4, 5, None, 6]
    root1 = algviz.parseBinaryTree(tree_nodes1)
    graph1 = viz.createGraph(root1)
    expect_nodes1 = ['1', '2', '3', '4', '5', '6']
    expect_edges1 = [
        ('1', '2', None), ('1', '3', None),
        ('2', '4', None), ('2', '5', None),
        ('3', '6', 'R')
    ]
    nodes, edges = get_graph_elements(graph1._repr_svg_())
    res.add_case(equal(nodes, expect_nodes1) and equal_table(edges, expect_edges1), 'Create tree_1',
                'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes1, expect_edges1))
    '''
    # Test create a binary tree like this:
           -1
           / \
         -2  -3
          \   /
          -4 -5
    '''
    tree_nodes2 = [-1, -2, -3, None, -4, -5, None]
    root2 = algviz.parseBinaryTree(tree_nodes2)
    graph2 = viz.createGraph(root2)
    expect_nodes2 = ['-1', '-2', '-3', '-4', '-5']
    expect_edges2 = [
        ('-1', '-2', None), ('-1', '-3', None),
        ('-2', '-4', 'R'), ('-3', '-5', 'L'),
    ]
    nodes, edges = get_graph_elements(graph2._repr_svg_())
    res.add_case(equal(nodes, expect_nodes2) and equal_table(edges, expect_edges2), 'Create tree_2',
                'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes2, expect_edges2))
    # Test merge two tree.
    root1.left.right.right = root2
    expect_nodes = sorted(expect_nodes1 + expect_nodes2)
    expect_edges = sorted(expect_edges1 + expect_edges2 + [('5', '-1', 'R')])
    graph1._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(graph1._repr_svg_())
    res.add_case(equal(nodes, expect_nodes) and equal_table(edges, expect_edges), 'Merge two tree',
                'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test traverse tree nodes.
    visit_list = list()
    def traverse_binary_tree(root):
        if root is not None:
            visit_list.append(root.val)
            root.val += 1   # Update the tree node label for the update tree node test case.
            traverse_binary_tree(root.left)
            traverse_binary_tree(root.right)
    traverse_binary_tree(root1)
    expect_visit_list = [1, 2, 4, 5, -1, -2, -4, -3, -5, 3, 6]
    res.add_case(equal(visit_list, expect_visit_list), 'Traverse tree',
                visit_list, expect_visit_list)
    # Test update tree node label value (We did the update before).
    expect_nodes = sorted([str(int(i)+1) for i in expect_nodes])
    nodes, _ = get_graph_elements(graph1._repr_svg_())
    res.add_case(equal(nodes, expect_nodes), 'Update node label',
                nodes, expect_nodes)
    return res


def test_modify_binary_tree():
    res = TestResult()
    viz = algviz.Visualizer()
    # TODO: Add subcases.
    return res


def test_create_tree():
    res = TestResult()
    viz = algviz.Visualizer()
    # TODO: Add subcases.
    return res


def test_traverse_tree():
    res = TestResult()
    viz = algviz.Visualizer()
    # TODO: Add subcases.
    return res


def test_modify_tree():
    res = TestResult()
    viz = algviz.Visualizer()
    # TODO: Add subcases.
    return res
