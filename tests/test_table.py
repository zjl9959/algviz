#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from utility import TestCustomPrintableClass, equal, equal_table
from result import TestResult
import algviz

import xml.dom.minidom as xmldom


def test_create_table():
    res = TestResult()
    viz = algviz.Visualizer()
    # Test create an empty table(2x2).
    table = viz.createTable(2, 2)
    tab_elems = get_table_elements(table._repr_svg_(), 2)
    expect_res = [[None, None], [None, None]]
    res.add_case(equal_table(tab_elems, expect_res), 'Empty table',
                 tab_elems, expect_res)
    # Test create table with different type.
    table_data = [[3.21, 'hi', 0], [-2, None, True],
                 [(-7, 8), (3), TestCustomPrintableClass(3.6, 'Test')]]
    table = viz.createTable(3, 3, table_data, show_index=False)
    tab_elems = get_table_elements(table._repr_svg_(), 3)
    res.add_case(equal_table(tab_elems, table_data), 'Multi-data type',
                 tab_elems, table_data)
    return res


def test_visit_element():
    res = TestResult()
    viz = algviz.Visualizer()
    # Test random access index.
    table_data = [[3.21, 'hi', 0], [-2, None, True],
                 [(-7, 8), (3), 5]]
    table = viz.createTable(3, 3, table_data)
    index_list = [(0, 0), (2, 2), (1, 0), (2, 1)]
    expect_res = [3.21, 5, -2, (3)]
    visit_elems = list()
    for r, c in index_list:
        visit_elems.append(table[r][c])
    res.add_case(equal(visit_elems, expect_res), 'Vist elements',
                 visit_elems, expect_res)
    return res


def test_update_element():
    res = TestResult()
    # TODO: add subcases.
    return res


def test_mark_element():
    res = TestResult()
    # TODO: add subcases.
    return res


def get_table_elements(svg_str, col):
    '''
    @function: Parse table elements from it's display SVG string.
        Then sort the elements by their relative positions (top,left -> down,right).
    @param: {svg_str->str} The table display string.
    @param: {col->int} The column number of table.
    @return: {list(list(str))} Return the elements string representation. 
    '''
    svg = xmldom.parseString(svg_str)
    grids = svg.getElementsByTagName('g')
    elements_pos = list()   # list contains tuple(str, float), which means element string and it's position number.
    for g in grids:
        rects = g.getElementsByTagName('rect')
        if len(rects) != 1:
            continue
        pos_x = float(rects[0].getAttribute('x'))
        pos_y = float(rects[0].getAttribute('y'))
        texts = g.getElementsByTagName('text')
        element = None
        for text in texts:
            if text.getAttribute('text-anchor') == 'middle' and text.firstChild:
                element = text.firstChild.data
        elements_pos.append((pos_y, pos_x, element))
    # Sort elements by positon and get elements string.
    elements_pos = sorted(elements_pos)
    result = list()
    for i in range(len(elements_pos)):
        r = i // col
        if r >= len(result):
            result.append(list())
        result[r].append(elements_pos[i][2])
    return result
