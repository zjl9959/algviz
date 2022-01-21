#!/usr/bin/env python3

"""Search for the earliest version of each dependency library. 

The search Algorithm is: Search the library one by one.
For the searching library, binary/linear search from the latest version to earlier version on it.
And fix the not searching libraries into the latest version.

Author: zjl9959@gmail.com

License: GPLv3

"""


import platform
import os
import sys


# The test libraries below should be indepent with each other.
dep_libs = {
    # https://pypi.org/project/ipykernel/
    'ipykernel': ['4.0.1', '4.0.2', '4.0.3', '4.1.0', '4.1.1', '4.2.0',
                '4.2.1', '4.2.2', '4.3.0', '4.3.1', '4.4.0', '4.4.1',
                '4.5.0', '4.5.1', '4.5.2', '4.6.0', '4.6.1', '4.7.0',
                '4.8.0', '4.8.1', '4.8.2', '4.9.0', '4.10.0', '4.10.1',
                '5.0.0', '5.1.0', '5.1.1', '5.1.2', '5.1.3', '5.1.4',
                '5.2.0', '5.2.1', '5.3.0', '5.3.1', '5.3.2', '5.3.3',
                '5.3.4', '5.4.0', '5.4.1', '5.4.2', '5.4.3', '5.5.0',
                '5.5.3', '5.5.4', '5.5.5', '5.5.6', '6.0.0', '6.0.1',
                '6.0.2', '6.0.3', '6.1.0', '6.2.0', '6.3.0', '6.3.1',
                '6.4.0', '6.4.1', '6.4.2', '6.5.0', '6.5.1', '6.6.0',
                '6.6.1', '6.7.0'],
    # https://pypi.org/project/graphviz/
    'graphviz': ['0.1', '0.1.1', '0.2', '0.2.1', '0.2.2', '0.3',
                '0.3.1', '0.3.2', '0.3.3', '0.3.4', '0.3.5', '0.4',
                '0.4.1', '0.4.2', '0.4.3', '0.4.4', '0.4.5', '0.4.6',
                '0.4.7', '0.4.8', '0.4.9', '0.4.10', '0.5', '0.5.1',
                '0.5.2', '0.6', '0.7', '0.7.1', '0.8', '0.8.1', '0.8.2',
                '0.8.3', '0.8.4', '0.9', '0.10', '0.10.1', '0.11',
                '0.11.1', '0.12', '0.13', '0.13.1', '0.13.2', '0.14',
                '0.14.1', '0.14.2', '0.15', '0.16', '0.17', '0.18',
                '0.18.1', '0.18.2', '0.19', '0.19.1'],
}


def binary_search():
    earliest = list()
    for lib, versions in dep_libs.items():
        last_sucess_version = None
        st, ed = 0, len(versions)
        other_libs_cmd = ''
        for other_lib, other_versions in dep_libs.items():
            if other_lib != lib:
                other_libs_cmd += '{}=={},'.format(other_lib, other_versions[-1])
        while st < ed:
            mid = st + (ed-st)//2
            libs_cmd = other_libs_cmd + '{}=={}'.format(lib, versions[mid])
            print("Test {}:{}".format(lib, versions[mid]))
            res = call_dependency_test(libs_cmd)
            if res < 0:
                raise Exception('Environment error when running test.')
            elif res > 0:
                st = mid+1
            else:
                last_sucess_version = versions[mid]
                ed = mid
        earliest.append(('{}={}'.format(lib, last_sucess_version), other_libs_cmd))
    return earliest


def linear_search():
    earliest = list()
    for lib, versions in dep_libs.items():
        last_sucess_version = None
        other_libs_cmd = ''
        for other_lib, other_versions in dep_libs.items():
            if other_lib != lib:
                other_libs_cmd += '{}=={},'.format(other_lib, other_versions[-1])
        for version in versions[::-1]:
            libs_cmd = other_libs_cmd + '{}=={}'.format(lib,version)
            print("Test {}:{}".format(lib, version))
            res = call_dependency_test(libs_cmd)
            if res < 0:
                raise Exception('Environment error when running test.')
            elif res > 0:
                earliest.append(('{}={}'.format(lib, last_sucess_version), other_libs_cmd))
                break
            else:
                last_sucess_version = version
    return earliest


platform_type = None    # 0:Windows;1:Linux;-1:Unknow
def call_dependency_test(test_libs):
    global platform_type
    if not platform_type:
        platform_name = platform.platform()
        if platform_name.find('Windows') != -1:
            platform_type = 0
        elif platform_name.find('Linux') != -1:
            platform_type = 1
        else:
            platform_type = -1
    if platform_type == 0:
        raise Exception("Not implement error!")
    elif platform_type == 1:
        return os.system('./dependency_test.sh {}'.format(test_libs))
    else:
        raise Exception("Not supported platform!")


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    earliest = list()
    if len(sys.argv) == 2:
        search_mode = sys.argv[1]
        if search_mode == 'B':
            earliest = binary_search()
        elif search_mode == 'L':
            earliest = linear_search()
        else:
            print("Search mode should be B(binary search) or L(linear search).")
    else:
        earliest = binary_search()
    if len(earliest):
        print('*'*45)
        print('These librarie(s) earliest version can be supported.')
        for test in earliest:
            print('Lib:{}, ENV:{}'.format(test[0], test[1]))
        print('*'*45)


if __name__ == "__main__":
    main()
