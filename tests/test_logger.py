#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

from result import TestResult
import algviz

def test_logger():
    res = TestResult()
    viz = algviz.Visualizer()
    logger = viz.createLogger(3)
    # Test write line.
    logger.write('line 1')
    log_str = logger.__repr__()
    expect_str = 'line 1\n'
    res.add_case(log_str==expect_str, 'Write log',
                log_str, expect_str)
    # Test multi-line logger.
    logger.write('line 2')
    log_str = logger.__repr__()
    expect_str = 'line 1\nline 2\n'
    res.add_case(log_str==expect_str, 'Multi-line logs',
                log_str, expect_str)
    # Test logger buffer refresh.
    logger.write('line 3')
    logger.write('line 4')  # Buffer overflow, remove log: 'line 1'.
    log_str = logger.__repr__()
    expect_str = 'line 2\nline 3\nline 4\n'
    res.add_case(log_str==expect_str, 'Buffer refresh',
                log_str, expect_str)
    # Test clear log.
    logger.clear()
    log_str = logger.__repr__()
    expect_str = ''
    res.add_case(log_str==expect_str, 'Clear log',
                log_str, expect_str)
    return res
