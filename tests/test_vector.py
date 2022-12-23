#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

import algviz
from utility import TestCustomPrintableClass, equal
from result import TestResult

import xml.dom.minidom as xmldom


def test_create_vector():
    viz = algviz.Visualizer()
    res = TestResult()
    # Test create an empty vector.
    vec = viz.createVector()
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(len(vec_elems) == 0, 'Empty vector', vec_elems)
    # Test create an normal vector.
    vec_data = [1, 2, 3]
    vec = viz.createVector(vec_data)
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_data, vec_elems), 'Normal vector',
                 vec_elems, vec_data)
    # Test create vector with different type in it.
    vec_data = [-3.56, 'hi', (2.4, 7), None, 6, TestCustomPrintableClass(1, 2)]
    vec = viz.createVector(vec_data)
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_data, vec_elems), 'Multi-data type vector',
                 vec_elems, vec_data)
    # Test create a histogram vector.
    vec_data = [0.3, -2, 4, 1.5, 9]
    vec = viz.createVector(vec_data, cell_size=(40, 300), histogram=True)
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_data, vec_elems, float), 'Histogram vector',
                 vec_elems, vec_data)
    return res


def test_visit_elements():
    viz = algviz.Visualizer()
    res = TestResult()
    vec_data = [1, 2, 3, 4, 5, 6]
    vec = viz.createVector(vec_data)
    # Test visit vector elements by index.
    visit_elems = list()
    for i in range(len(vec)):
        visit_elems.append(vec[i])
    res.add_case(equal(vec_data, visit_elems), 'Visit by index',
                 visit_elems, vec_data)
    # Test visit vector elements by iterator.
    visit_elems = list()
    for elem in vec:
        visit_elems.append(elem)
    res.add_case(equal(vec_data, visit_elems), 'Visit by iterator',
                 visit_elems, vec_data)
    # Test random visit elements.
    visit_elems = list()
    index_list = [3, 3, 4, 0, 1, 4]
    expect_results = [4, 4, 5, 1, 2, 5]
    for i in index_list:
        visit_elems.append(vec[i])
    res.add_case(equal(expect_results, visit_elems), 'Random visit',
                 visit_elems, expect_results)
    # Test index out of range.
    case_ok = False
    try:
        vec[-1] = 2
    except RuntimeError:
        case_ok = True
    res.add_case(case_ok, 'Index out of range.')
    # Test invalid index type.
    case_ok = False
    try:
        vec['abc'] = 3
    except RuntimeError:
        case_ok = True
    res.add_case(case_ok, 'Invalid index type.')
    return res


def test_update_elements():
    viz = algviz.Visualizer()
    res = TestResult()
    vec_data = [1, 2, 3, 4, 5, 6]
    vec = viz.createVector(vec_data)
    # Test update elements value.
    new_data = [3, 5, 7, -2, 'str', None]
    for i in range(len(vec)):
        vec[i] = new_data[i]
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_elems, new_data), 'Update elements',
                 vec_elems, new_data)
    # Test repeat update one elements multi-times.
    expect_results = [3, -4, 7, -2, 'str', 3]
    vec[1] = 6
    vec[1] = -4
    vec[len(vec) - 1] = 9
    vec[len(vec) - 1] = 3
    vec[len(vec) - 1] = 3
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_elems, expect_results), 'Repeat update',
                 vec_elems, expect_results)
    return res


def test_modify_vectors():
    res = TestResult()
    viz = algviz.Visualizer()
    vec_data = [1, 2, 3]
    vec = viz.createVector(vec_data)
    # Test insert element.
    vec.insert(1, -2)
    vec._repr_svg_()    # Call this to skip animation frame.
    vec_elems = get_vector_elements(vec._repr_svg_())
    expect_results = [1, -2, 2, 3]
    res.add_case(equal(vec_elems, expect_results), 'Insert element',
                 vec_elems, expect_results)
    # Test pop element.
    vec.pop()
    vec._repr_svg_()
    vec_elems = get_vector_elements(vec._repr_svg_())
    expect_results = [1, -2, 2]
    res.add_case(equal(vec_elems, expect_results), 'Pop element',
                 vec_elems, expect_results)
    # Test append element.
    vec.append(7)
    vec._repr_svg_()
    vec_elems = get_vector_elements(vec._repr_svg_())
    expect_results = [1, -2, 2, 7]
    res.add_case(equal(vec_elems, expect_results), 'Append element',
                 vec_elems, expect_results)
    # Test swap elements.
    vec.swap(1, 3)
    vec._repr_svg_()
    vec_elems = get_vector_elements(vec._repr_svg_())
    expect_results = [1, 7, 2, -2]
    res.add_case(equal(vec_elems, expect_results), 'Swap elements',
                 vec_elems, expect_results)
    # Test clear vector.
    vec.clear()
    vec._repr_svg_()
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_elems, []), 'Clear vector',
                 vec_elems, [])
    # Test combine operations (opearate sequence is important).
    vec.append(4)       # [4]
    vec.append(2)       # [4, 2]
    vec.insert(0, 1)    # [1, 4, 2]
    vec.pop()           # [1, 4]
    vec[0] += 1         # [2, 4]
    vec._repr_svg_()
    vec_elems = get_vector_elements(vec._repr_svg_())
    expect_results = [2, 4]
    res.add_case(equal(vec_elems, expect_results), 'Combine operationst',
                 vec_elems, expect_results)
    return res


def test_mark_elements():
    res = TestResult()
    viz = algviz.Visualizer()
    vec_data = [1, 2, 3, 4, 5]
    vec = viz.createVector(vec_data)
    # Add some hold and no hold marks into vector.
    vec.mark((255, 0, 0), 0, hold=True)
    vec.mark((0, 255, 0), 1, hold=False)
    vec.mark((0, 0, 255), 2, 4, hold=True)
    # Test if all the marks color right.
    vec_bgcolors = get_vector_bgcolors(vec._repr_svg_())
    expect_bgcolors = ['#ff0000', '#00ff00', '#0000ff', '#0000ff', '#ffffff']
    res.add_case(equal(vec_bgcolors, expect_bgcolors), 'Mark',
                 vec_bgcolors, expect_bgcolors)
    # Test if no hold color auto disappered.
    vec_bgcolors = get_vector_bgcolors(vec._repr_svg_())
    expect_bgcolors = ['#ff0000', '#ffffff', '#0000ff', '#0000ff', '#ffffff']
    res.add_case(equal(vec_bgcolors, expect_bgcolors), 'Mark no hold',
                 vec_bgcolors, expect_bgcolors)
    # Test remove mark.
    vec.removeMark((255, 0, 0))
    vec.removeMark((0, 0, 255))
    vec_bgcolors = get_vector_bgcolors(vec._repr_svg_())
    expect_bgcolors = ['#ffffff', '#ffffff', '#ffffff', '#ffffff', '#ffffff']
    res.add_case(equal(vec_bgcolors, expect_bgcolors), 'Remove mark',
                 vec_bgcolors, expect_bgcolors)
    return res


def test_vector_cursor():
    res = TestResult()
    viz = algviz.Visualizer()
    vec_data = [1, 2, 3, 4, 5]
    vec = viz.createVector(vec_data)
    # Test access elements by vector cursor.
    results, expect_results = list(), [2, 1, 4, 5]
    i = viz.createCursor(1, 'i')
    results.append(vec[i])
    i *= 5
    i -= 1
    i //= 5
    results.append(vec[i])
    i += 3
    i += i
    i -= 3
    i << i + 3 + 1
    i %= 4
    results.append(vec[i])
    i << 4
    results.append(vec[i])
    res.add_case(equal(results, expect_results), 'Access elements', results, expect_results)
    # Test modify elements by vector cursor.
    j = viz.createCursor(i, 'j')
    j -= 1
    expect_results = [2, 3, 4, 7, -5]
    if j < i:
        j << i
        if j == 4:
            vec[j] = -5
        if j != i.index() - 1:
            vec.insert(j, 7)
        if j <= 4:
            j -= 4
            vec.pop(j)
    vec._repr_svg_()        # Call this to skip animation frame.
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_elems, expect_results), 'Modify vector',
                 vec_elems, expect_results)
    # Test index out of range.
    case_ok = False
    try:
        j -= 1
        vec[j] = 2
    except RuntimeError:
        case_ok = True
    res.add_case(case_ok, 'Index out of range.')
    return res


def get_vector_elements(svg_str):
    '''
    @function: Parse vector elements from it's display SVG string.
        Then sort the elements by their relative positions.
    @param: {svg_str->str} The vector display string.
    @return: {list(str)} Return the elements string representation.
    '''
    svg = xmldom.parseString(svg_str)
    grids = svg.getElementsByTagName('g')
    elements_pos = list()   # list contains tuple(str, float), which means element string and it's position number.
    for g in grids:
        rects = g.getElementsByTagName('rect')
        if len(rects) != 1:
            continue
        pos = float(rects[0].getAttribute('x'))
        texts = g.getElementsByTagName('text')
        element = None
        for text in texts:
            animates = text.getElementsByTagName('animate')
            skip = False
            for animate in animates:
                if animate.getAttribute('to') == '0':
                    skip = True
                    break
            if not skip and text.getAttribute('class') == 'txt':
                for child in text.childNodes:
                    if child.nodeType == xmldom.Node.TEXT_NODE:
                        element = child.data
        elements_pos.append((pos, element))
    # Sort elements by positon and get elements string.
    elements_pos = sorted(elements_pos)
    result = list()
    for _, elem in elements_pos:
        result.append(elem)
    return result


def get_vector_bgcolors(svg_str):
    '''
    @function: Parse vector rect's background color from it's display SVG string.
        Then sort the colors by their relative positions.
    @param: {svg_str->str} The vector display string.
    @return: {list(str)} Return the bgcolors list.
    '''
    svg = xmldom.parseString(svg_str)
    grids = svg.getElementsByTagName('g')
    colors_pos = list()   # list contains tuple(str, float), which means element string and it's position number.
    for g in grids:
        rects = g.getElementsByTagName('rect')
        if len(rects) != 1:
            continue
        pos = float(rects[0].getAttribute('x'))
        color = rects[0].getAttribute('fill')
        colors_pos.append((pos, color))
    colors_pos = sorted(colors_pos)
    result = list()
    for _, color in colors_pos:
        result.append(color)
    return result
