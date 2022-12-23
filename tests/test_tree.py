#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

import algviz
from result import TestResult
from utility import equal, equal_table, get_graph_elements, hack_graph
from algviz.utility import AlgvizParamError


def test_binary_tree():
    res = TestResult()
    viz = algviz.Visualizer()
    '''
    # Test create a binary tree like this:
            1
           / \\
          2    3
         / \\   \\
        4   5    6
    '''
    tree_nodes1 = [1, 2, 3, 4, 5, None, 6]
    root1 = algviz.parseBinaryTree(tree_nodes1)
    graph1 = viz.createGraph(root1)
    hack_graph(graph1)
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
           / \\
         -2  -3
          \\   /
          -4 -5
    '''
    tree_nodes2 = [-1, -2, -3, None, -4, -5, None]
    root2 = algviz.parseBinaryTree(tree_nodes2)
    graph2 = viz.createGraph(root2)
    hack_graph(graph2)
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
    expect_nodes = sorted([str(int(i) + 1) for i in expect_nodes])
    nodes, _ = get_graph_elements(graph1._repr_svg_())
    res.add_case(equal(nodes, expect_nodes), 'Update node label',
                 nodes, expect_nodes)
    return res


def test_modify_binary_tree():
    res = TestResult()
    viz = algviz.Visualizer()
    root = algviz.BinaryTreeNode('root')
    # Test add nodes into binary tree.
    tree = viz.createGraph(root)
    hack_graph(tree)
    tree2 = viz.createGraph(root)
    hack_graph(tree2)
    root.left = algviz.BinaryTreeNode('left')
    root.right = algviz.BinaryTreeNode('right')
    expect_nodes = ['left', 'right', 'root']
    expect_edges = [('root', 'left', None), ('root', 'right', None)]
    nodes, edges = get_graph_elements(tree._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Add nodes',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test multiply graph refresh.
    nodes, edges = get_graph_elements(tree2._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Add nodes(multiply graph)',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test remove nodes from binray tree.
    right_node = root.right
    root.right = None
    tree.removeNode(right_node)
    expect_nodes = ['left', 'root']
    expect_edges = [('root', 'left', 'L')]
    tree._repr_svg_()   # Skip the animation frame.
    nodes, edges = get_graph_elements(tree._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Remove nodes',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test multiply graph refresh.
    tree2._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(tree2._repr_svg_())
    expect_nodes = ['left', 'right', 'root']
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Remove nodes(multiply graph)',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    return res


def test_traverse_tree():
    res = TestResult()
    viz = algviz.Visualizer()
    # Test create a tree.
    tree_info = {
        0: [1, 2, 3],
        1: [4, 5],
        2: [8],
        5: [9, 10]
    }
    root = algviz.parseTree(tree_info, {10: 'n10'})
    tree = viz.createGraph(root)
    hack_graph(tree)
    expect_nodes = [0, 1, 2, 3, 4, 5, 8, 9, 'n10']
    expect_edges = [
        (0, 1, None), (0, 2, None), (0, 3, None),
        (1, 4, None), (1, 5, None),
        (2, 8, None),
        (5, 9, None), (5, 'n10', None)
    ]
    nodes, edges = get_graph_elements(tree._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Create tree',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test traverse tree.
    visit_list = list()

    def traverse_tree(root):
        if root is not None:
            visit_list.append(str(root.val))
            root.val = str(root.val) + 'v'   # Update the tree node label for the update tree node test case.
            for child in root.children():
                traverse_tree(child)
    traverse_tree(root)
    expect_visit_list = sorted(['0', '1', '4', '5', '9', 'n10', '2', '8', '3'])
    visit_list = sorted(visit_list)
    res.add_case(equal(visit_list, expect_visit_list), 'Traverse tree',
                 visit_list, expect_visit_list)
    # Test update tree node label value (We did the update before).
    expect_nodes = sorted([str(i) + 'v' for i in expect_nodes])
    nodes, edges = get_graph_elements(tree._repr_svg_())
    res.add_case(equal(nodes, expect_nodes), 'Update node label', nodes, expect_nodes)
    return res


def test_modify_tree():
    res = TestResult()
    viz = algviz.Visualizer()
    tree_info = {0: [1, 2]}
    root = algviz.parseTree(tree_info)
    tree = viz.createGraph(root)
    hack_graph(tree)
    # Test nodes into tree.
    sub_tree = algviz.parseTree({3: [4, 5, 6], 4: [7, 9]})
    root.add(sub_tree)
    root.add(algviz.TreeNode(8))
    expect_nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    expect_edges = [
        (0, 1, None), (0, 2, None), (0, 3, None), (0, 8, None),
        (3, 4, None), (3, 5, None), (3, 6, None),
        (4, 7, None), (4, 9, None)
    ]
    tree._repr_svg_()   # Skip the animation frame.
    nodes, edges = get_graph_elements(tree._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Add nodes',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    assert root.childCount() == 4
    # Test childIndex interface.
    expect_res = [0, 1, 2, 3]
    actual_res = []
    for child in root.children():
        actual_res.append(root.childIndex(child))
    res.add_case(equal(expect_res, actual_res), 'childIndex', expect_res, actual_res)
    # Test childAt interface.
    expect_res = [8, 2, 3, 1]
    actual_res = [root.childAt(3), root.childAt(1), root.childAt(2), root.childAt(0)]
    res.add_case(equal(expect_res, actual_res), 'childAt', expect_res, actual_res)
    # Test remove nodes from tree.
    for child in root.children():
        if child.val <= 3:
            root.remove(child)
            tree.removeNode(child, recursive=True)
    expect_nodes = [0, 8]
    expect_edges = [(0, 8, None)]
    tree._repr_svg_()   # Skip the animation frame.
    nodes, edges = get_graph_elements(tree._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'Remove nodes',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test add/removeAt interface.
    root.add(sub_tree)
    root.add(algviz.TreeNode(10), 1)
    root.childAt(2).removeAt(0)
    expect_nodes = [0, 10, 3, 4, 5, 6, 7, 8, 9]
    expect_edges = [(0, 10, None), (0, 3, None), (0, 8, None), (3, 5, None), (3, 6, None), (4, 7, None), (4, 9, None)]
    tree._repr_svg_()   # Skip the animation frame.
    nodes, edges = get_graph_elements(tree._repr_svg_())
    res.add_case(equal(expect_nodes, nodes) and equal_table(expect_edges, edges), 'add/removeAt',
                 'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    return res


def test_regression_issue_4():
    # case1: regression from https://github.com/zjl9959/algviz/issues/4
    res = TestResult()
    nodes = [1, 2, 2, 3, 4, 4, 3, 5, 6, 7, 8, 8, 7, 5]
    root = algviz.parseBinaryTree(nodes)
    index = 0
    queue = [root]
    while len(queue) > 0:
        root = queue.pop(0)
        if root is not None:
            assert nodes[index] == root.val
            index += 1
            queue.append(root.left)
            queue.append(root.right)
    res.add_case(index == len(nodes), 'parseBinaryTree', index, len(nodes))
    # case2: invalid input parmeter check.
    nodes = [0, None, 2, 3, 4]
    try:
        root = algviz.parseBinaryTree(nodes)
        res.add_case(False, 'invalidInputCheck')
    except AlgvizParamError:
        res.add_case(True, 'invalidInputCheck')
    return res
