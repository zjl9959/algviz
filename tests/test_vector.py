#!/usr/bin/env python3

import algviz
from result import TestResult

import xml.dom.minidom as xmldom

class TestVectorClass:
    '''
    @class: This class used to test if Vector can display self defined class noramlly.
    '''
    
    def __init__(self, v1, v2) -> None:
        self._v1 = v1
        self._v2 = v2

    def __repr__(self) -> str:
        return '{}->{}'.format(self._v1, self._v2)


def test_create_vector():
    viz = algviz.Visualizer()
    res = TestResult()
    
    # Test create an empty vector.
    vec = viz.createVector()
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(len(vec_elems)==0, 'Empty vector', vec_elems)

    # Test create an normal vector.
    vec_data = [1, 2, 3]
    vec = viz.createVector(vec_data)
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_data, vec_elems), 'Normal vector', vec_elems, vec_data)

    # Test create vector with different type in it.
    vec_data = [-3.56, 'hi', (2.4, 7), None, 6, TestVectorClass(1,2)]
    vec = viz.createVector(vec_data)
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_data, vec_elems), 'Multi-data type vector', vec_elems, vec_data)

    # Test create a histogram vector.
    vec_data = [0.3, -2, 4, 1.5, 9]
    vec = viz.createVector(vec_data, bar=300)
    vec_elems = get_vector_elements(vec._repr_svg_())
    res.add_case(equal(vec_data, vec_elems), 'Histogram vector', vec_elems, vec_data)
    return res


def test_visit_elements():
    viz = algviz.Visualizer()
    res = TestResult()
    vec_data = [1, 2, 3, 4, 5, 6]
    vec = viz.createVector(vec_data)

    # Test visit vector elements by index.
    vec_elems = list()
    for i in range(len(vec)):
        vec_elems.append(vec[i])
    res.add_case(equal(vec_data, vec_elems), 'Visit by index', vec_elems, vec_data)

    # Test visit vector elements.
    vec_elems = list()
    for elem in vec:
        vec_elems.append(elem)
    res.add_case(equal(vec_data, vec_elems), 'Visit by iterator', vec_elems, vec_data)
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
    res.add_case(equal(vec_elems, new_data), 'Update elements', vec_elems, new_data)

    return res


def test_modify_vectors():
    res = TestResult()

    # TODO: add subcases.

    return res


def test_mark_elements():
    res = TestResult()

    # TODO: add subcases.

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
            if text.getAttribute('text-anchor') == 'middle' and text.firstChild:
                element = text.firstChild.data
        elements_pos.append((pos, element))
    # Sort elements by positon and get elements string.
    elements_pos = sorted(elements_pos)
    result = list()
    for _, elem in elements_pos:
        result.append(elem)
    return result


def equal(lhs, rhs):
    '''
    @function: Check if lhs equal with rhs (lhs and rhs should be iterable).
    @return: {bool} Wheather lhs equal with rhs or not.
    '''
    if len(lhs) != len(rhs):
        return False
    for i in range(len(lhs)):
        if str(lhs[i]) != str(rhs[i]):
            return False
    return True
