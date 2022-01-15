#!/usr/bin/env python3

'''
@author:zjl9959@gmail.com
@license:GPLv3
'''


import time


def main():
    nb_failed = 0
    import test_logger
    nb_failed += run_test_module(test_logger)
    import test_vector
    nb_failed += run_test_module(test_vector)
    import test_table
    nb_failed += run_test_module(test_table)
    import test_linked_list
    nb_failed += run_test_module(test_linked_list)
    import test_tree
    nb_failed += run_test_module(test_tree)
    import test_graph
    nb_failed += run_test_module(test_graph)
    print("*"*45)
    if nb_failed == 0:
        print('Congratulations, everything is OK !!!')
    else:
        print('Oops, {} test function(s) failed !!!'.format(nb_failed))
    print("*"*45)
    return nb_failed


def run_test_module(test_module):
    # Filter test_xxx functions in test_module and call test.
    num_pass, num_failed = 0, 0
    test_funcs = [o for o in dir(test_module) if o.startswith('test')]
    print("-"*45, "\r\n>>>> Begin <{0}>.".format(test_module.__name__))
    results = dict()
    start_time = time.time()
    for func in test_funcs:
        try:
            res = getattr(test_module, func)()
            results[func] = res
        except Exception as e:  # Catch the test exception and print it.
            print("[ERROR] When running {0}.{1}, exception: <{2}> was thrown.".format(test_module.__name__, func, e))
            num_failed += 1
    end_time = time.time()
    # Statistic the number of pass and failed cases.
    for result in results.values():
        if result.ok():
            num_pass = num_pass + 1
        else:
            num_failed = num_failed + 1
    # Print the test results.
    if num_failed > 0:
        print(">>>> {0} function(s) failed:".format(num_failed))
    else:
        print(">>>> OK!")
    for func, result in results.items():
        if not result.ok():
            print(" - [ERROR] {0}".format(func))
            print(result, end='')
    print(">>>> End <{0}> ({1:.2f} ms).".format(test_module.__name__, (end_time-start_time)*1000))
    return num_failed


if __name__ == '__main__':
    main()
