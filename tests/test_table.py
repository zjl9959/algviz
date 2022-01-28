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
    tab_elems = get_table_elements(table._repr_svg_())
    expect_res = [[None, None], [None, None]]
    res.add_case(equal_table(tab_elems, expect_res), 'Empty table',
                 tab_elems, expect_res)
    # Test create table with different type.
    table_data = [[3.21, 'hi', 0], [-2, None, True],
                 [(-7, 8), (3), TestCustomPrintableClass(3.6, 'Test')]]
    table = viz.createTable(3, 3, table_data, show_index=False)
    tab_elems = get_table_elements(table._repr_svg_())
    res.add_case(equal_table(tab_elems, table_data), 'Multi-data type',
                 tab_elems, table_data)
    # Test the shape interface of table.
    row, col = table.shape()
    res.add_case(row==3 and col==3, 'Table shape', (row, col), (3, 3))
    # Test invalid input row/col. (Throw exception if input row, col is invalid)
    case_ok = False
    try:
        table = viz.createTable(-1, 3, table_data)
        table = viz.createTable(1, 0, table_data)
    except:
        case_ok = True
    res.add_case(case_ok, 'Invalid input row/col')
    # Test invalid input table_data.
    case_ok = True
    try:
        table = viz.createTable(3, 2, [[1, 2], [2]])
    except:
        case_ok = False
    res.add_case(case_ok, 'Invalid input table_data')
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
    res.add_case(equal(visit_elems, expect_res), 'Visit element by index',
                 visit_elems, expect_res)
    # Test visit elements by iterator.
    visit_elems = list()
    for tab_row in table:
        for elem in tab_row:
            visit_elems.append(elem)
    expect_res =  [3.21, 'hi', 0, -2, None, True, (-7, 8), (3), 5]
    res.add_case(equal(visit_elems, expect_res), 'Visit element by iterator',
                 visit_elems, expect_res)
    # Test invalid row/col index.
    case_ok = False
    try:
        table[-1][3]
    except:
        case_ok = True
    res.add_case(case_ok, 'Invalid visit index')
    return res


def test_update_element():
    res = TestResult()
    viz = algviz.Visualizer()
    table_data = [
                    [1, 2, 3],
                    [-4, 5.67989, 4.32],
                    [5, 0, 3829]
                ]
    table = viz.createTable(3, 3, table_data)
    # Test update element by random index.
    index_list = [(0, 0), (1, 1), (2, 2)]
    expect_res = [
                    [2, 2, 3],
                    [-4, 6.67989, 4.32],
                    [5, 0, 3830]
                ]
    for r, c in index_list:
        table[r][c] += 1
    table_elems = get_table_elements(table._repr_svg_())
    res.add_case(equal_table(table_elems, expect_res), 'Random update',
                 table_elems, expect_res)
    # Test invalid update index.
    case_ok = False
    try:
        table[1][9] = 3
    except:
        case_ok = True
    res.add_case(case_ok, 'Invalid update index')
    return res


def test_mark_element():
    res = TestResult()
    viz = algviz.Visualizer()
    table = viz.createTable(2, 2)
    # Test not presistent mark (check 2 frames).
    mark_list = [(0, 1, (0, 255, 1)), (1, 0, (0, 3, 0)), (1, 0, (0, 1, 0))]
    expect_colors = [['#ffffff', '#00ff01'],
                     ['#000100', '#ffffff']]
    for r, c, color in mark_list:
        table.mark(color, r, c, hold=False)
    table_bgcolors_frame1 = get_table_bgcolors(table._repr_svg_())
    if not equal_table(table_bgcolors_frame1, expect_colors):
        res.add_case(False, 'No presistent mark frame1', table_bgcolors_frame1, expect_colors)
    else:
        table_bgcolors_frame2 = get_table_bgcolors(table._repr_svg_())
        expect_colors = [['#ffffff', '#ffffff'],
                         ['#ffffff', '#ffffff']]
        if not equal_table(table_bgcolors_frame2, expect_colors):
            res.add_case(False, 'No presistent mark frame2', table_bgcolors_frame2, expect_colors)
        else:
            res.add_case(True, 'No presistent mark')
    # Test presistent mark (check 3 frames).
    mark_list = [(0, 1, (0, 255, 1)), (1, 1, (0, 255, 1)), (1, 0, (0, 1, 0))]
    expect_colors = [['#ffffff', '#00ff01'],
                     ['#000100', '#00ff01']]
    for r, c, color in mark_list:
        table.mark(color, r, c)
    table_bgcolors_frame1 = get_table_bgcolors(table._repr_svg_())
    if not equal_table(table_bgcolors_frame1, expect_colors):
        res.add_case(False, 'Presistent mark frame1', table_bgcolors_frame1, expect_colors)
    else:
        table_bgcolors_frame2 = get_table_bgcolors(table._repr_svg_())
        if not equal_table(table_bgcolors_frame2, expect_colors):
            res.add_case(False, 'Presistent mark frame2', table_bgcolors_frame2, expect_colors)
        else:
            table_bgcolors_frame3 = get_table_bgcolors(table._repr_svg_())
            if not equal_table(table_bgcolors_frame3, expect_colors):
                res.add_case(False, 'Presistent mark frame3', table_bgcolors_frame3, expect_colors)
            else:
                res.add_case(True, 'Presistent mark')
    # Test remove mark.
    table.removeMark((0, 255, 1))
    expect_colors = [['#ffffff', '#ffffff'],
                     ['#000100', '#ffffff']]
    table_bgcolors = get_table_bgcolors(table._repr_svg_())
    res.add_case(equal_table(table_bgcolors, expect_colors), 'Remove mark',
                 table_bgcolors, expect_colors)
    return res


def get_table_elements(svg_str):
    '''
    @function: Parse table elements from it's display SVG string.
        Then sort the elements by their relative positions (top,left -> down,right).
    @param: {svg_str->str} The table display string.
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
            if text.getAttribute('class') == 'txt' and text.firstChild:
                element = text.firstChild.data
        elements_pos.append((pos_y, pos_x, element))
    # Sort elements by positon and get elements string.
    elements_pos = sorted(elements_pos)
    result = list()
    last_pos_y, cur_row = -1, -1
    for i in range(len(elements_pos)):
        if elements_pos[i][0] != last_pos_y:
            result.append(list())
            cur_row +=1
        result[cur_row].append(elements_pos[i][2])
        last_pos_y = elements_pos[i][0]
    return result


def get_table_bgcolors(svg_str):
    '''
    @function: Parse table rect's background color from it's display SVG string.
        Then sort the colors by their relative positions (top,left -> down,right).
    @param: {svg_str->str} The table display string.
    @return: {list(list(str))} Return the bgcolors list. 
    '''
    svg = xmldom.parseString(svg_str)
    grids = svg.getElementsByTagName('g')
    colors_pos = list()   # list contains tuple(str, float), which means element string and it's position number.
    for g in grids:
        rects = g.getElementsByTagName('rect')
        if len(rects) != 1:
            continue
        pos_x = float(rects[0].getAttribute('x'))
        pos_y = float(rects[0].getAttribute('y'))
        color = rects[0].getAttribute('fill')
        colors_pos.append((pos_y, pos_x, color))
    colors_pos = sorted(colors_pos)
    result = list()
    last_pos_y, cur_row = -1, -1
    for i in range(len(colors_pos)):
        if colors_pos[i][0] != last_pos_y:
            result.append(list())
            cur_row +=1
        result[cur_row].append(colors_pos[i][2])
        last_pos_y = colors_pos[i][0]
    return result
