#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from result import TestResult
import algviz
from utility import equal_table, get_graph_elements, equal


def test_create_forward_linked_list():
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


def test_traverse_forward_linked_list():
    res = TestResult()
    viz = algviz.Visualizer()
    # Test visit list nodes.
    head = algviz.parseForwardLinkedList([1, 2, 3, 4, 5, 6])
    graph = viz.createGraph(head)
    cur, visit_list = head, list()
    while cur:
        visit_list.append(cur.val)
        cur.val += 1
        cur = cur.next
    expect_list = [1, 2, 3, 4, 5, 6]
    res.add_case(equal(visit_list, expect_list), 'Visit list',
                visit_list, expect_list)
    # Test update list node value.
    nodes, _ = get_graph_elements(graph._repr_svg_())
    expect_list = [2, 3, 4, 5, 6, 7]
    res.add_case(equal(nodes, expect_list), 'Update node value',
                nodes, expect_list)
    return res


def test_modify_forward_linked_list():
    res = TestResult()
    viz = algviz.Visualizer()
    head = algviz.parseForwardLinkedList([1, 2, 3, 4, 5, 6])
    graph = viz.createGraph(head)
    # Test remove nodes from forward linked list.
    remove_positons = [0, 2, 5] # Remove nodes [1, 3, 6] from list.
    last, cur, pos = None, head, 0
    head = head.next    # Record the head node for next sub test case, because we will remove the head node in this test case.
    while cur:
        if pos in remove_positons:
            if last:
                last.next = cur.next
            last = cur
            # The unlinked nodes was not removed from graph until graph.removeNode() was called explicitly.
            graph.removeNode(cur)
            cur = cur.next
        else:
            last = cur
            cur = cur.next
        pos += 1
    expect_nodes = [2, 4, 5]
    expect_edges = [(2, 4, None), (4, 5, None)]   # 2->4->5
    graph._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(nodes, expect_nodes) and equal_table(edges, expect_edges), 'Remove nodes',
                'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test add nodes into forward linked list.
    node1 = algviz.ForwardLinkedListNode(1)
    node3 = algviz.ForwardLinkedListNode(3)
    node6 = algviz.ForwardLinkedListNode(6)
    # We need to add the head node into graph explicitly, because the graph can not find it from the reference chain.
    graph.addNode(node1); node1.next = head
    node4 = head.next; head.next = node3
    node3.next = node4; node5 = node4.next
    node5.next = node6
    expect_nodes = [1, 2, 3, 4, 5, 6]
    expect_edges = [(1, 2, None), (2, 3, None), (3, 4, None),
                    (4, 5, None), (5, 6, None)]
    graph._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(nodes, expect_nodes) and equal_table(edges, expect_edges), 'Add nodes',
                'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    # Test reverse forward linked list.
    tr1 = None;tr2 = node1
    while tr2 is not None:
        temp = tr2.next
        tr2.next = tr1
        tr1 = tr2
        tr2 = temp
    expect_nodes = [1, 2, 3, 4, 5, 6]
    expect_edges = [(2, 1, None), (3, 2, None), (4, 3, None),
                    (5, 4, None), (6, 5, None)]   # 6->5->4->3->2->1
    graph._repr_svg_()  # Skip the animation frame.
    nodes, edges = get_graph_elements(graph._repr_svg_())
    res.add_case(equal(nodes, expect_nodes) and equal_table(edges, expect_edges), 'Reverse list',
                'nodes:{};edges:{}'.format(nodes, edges), 'nodes:{};edges:{}'.format(expect_nodes, expect_edges))
    res.add_case(False, 'dsds')
    return res


def test_create_doubly_linked_list():
    res = TestResult()
    # TODO: Add subcases.
    return res


def test_traverse_doubly_linked_list():
    res = TestResult()
    # TODO: Add subcases.
    return res


def test_modify_doubly_linked_list():
    res = TestResult()
    # TODO: Add subcases.
    return res
