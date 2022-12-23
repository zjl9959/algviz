#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

import xml.dom.minidom as xmldom

from result import TestResult
from utility import equal
import algviz


def test_logger():
    res = TestResult()
    viz = algviz.Visualizer()
    logger = viz.createLogger(3)
    # Test write line.
    logger.write('line 1')
    log_str = get_logs_from_svg(logger._repr_svg_())
    expect_str = ['0. line 1']
    res.add_case(equal(log_str, expect_str), 'Write log',
                 log_str, expect_str)
    # Test multi-line logger.
    logger.write('line 2')
    log_str = get_logs_from_svg(logger._repr_svg_())
    expect_str = ['0. line 1', '1. line 2']
    res.add_case(equal(log_str, expect_str), 'Multi-line logs',
                 log_str, expect_str)
    # Test logger buffer refresh.
    logger.write('line 3')
    logger.write('line 4')  # Buffer overflow, remove log: 'line 1'.
    log_str = get_logs_from_svg(logger._repr_svg_())
    expect_str = ['1. line 2', '2. line 3', '3. line 4']
    res.add_case(equal(log_str, expect_str), 'Buffer refresh',
                 log_str, expect_str)
    # Test clear log.
    logger.clear()
    log_str = get_logs_from_svg(logger._repr_svg_())
    expect_str = []
    res.add_case(equal(log_str, expect_str), 'Clear log',
                 log_str, expect_str)
    # Test buffer overflow much.
    logger.write('line 8')
    logger.write('line 9')
    logger.write('line 10')
    log_str = get_logs_from_svg(logger._repr_svg_())
    expect_str = ['0. line 8', '1. line 9', '2. line 10']
    res.add_case(equal(log_str, expect_str), 'Buffer overflow',
                 log_str, expect_str)
    return res


def get_logs_from_svg(svg_str):
    text_lists = list()
    svg = xmldom.parseString(svg_str)
    text_nodes = svg.getElementsByTagName('text')
    for node in text_nodes:
        text_lists.append(node.firstChild.data)
    return text_lists
