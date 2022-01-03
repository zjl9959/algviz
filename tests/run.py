#!/usr/bin/env python3

'''
@author:zjl9959@gmail.com
@license:GPLv3
'''

import sys
import os
sys.path.append(os.path.join(sys.path[0], "../algviz"))


def main():
    raise('not implement error.')


def print_test_results(results):
    num_pass, num_failed = 0, 0
    for result in results.values():
        if result.ok():
            num_pass = num_pass + 1
        else:
            num_failed = num_failed + 1
    print("- Total functions:{0:>9}\r\n- Passed functions:{1:>8}\r\n- Failed functions:{2:>8}".format(
            len(results), num_pass, num_failed))
    for func, result in results.items():
        if not result.ok():
            print(" - {0}".format(func))
            print(result)


if __name__ == '__main__':
    main()
