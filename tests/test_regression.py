#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from result import TestResult
import algviz


def test_regression_5():
    """https://github.com/zjl9959/algviz/issues/5
    """
    res = TestResult()
    try:
        viz = algviz.Visualizer(1)
        grid = viz.createTable(1, 1, [[1]], show_index=False)
        r = viz.createCursor(0, 'r')
        c = viz.createCursor(0, 'c')
        grid[r][c]
        res.add_case(True, 'cursor')
    except Exception as e:
        print('test_regression_5 cursor exception:', e)
        res.add_case(False, 'cursor')
    try:
        viz = algviz.Visualizer(1)
        grid = viz.createTable(3, 3, show_index=False)
        grid.reshape(2, 2)
        res.add_case(True, 'reshape')
    except Exception as e:
        print('test_regression_5 reshape exception:', e)
        res.add_case(False, 'reshape')
    return res
