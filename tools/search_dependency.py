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
    'ipykernel': ['6.4.0', '6.4.1', '6.4.2', '6.5.0',
                  '6.5.1', '6.6.0', '6.6.1', '6.7.0'],
    # https://pypi.org/project/graphviz/
    'graphviz': ['0.8.4', '0.9', '0.10', '0.10.1', '0.11',
                '0.11.1', '0.12', '0.13', '0.13.1', '0.13.2', '0.14',
                '0.14.1', '0.14.2', '0.15', '0.16', '0.17', '0.18',
                '0.18.1', '0.18.2', '0.19', '0.19.1'],
}

PYTHON_='python'

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
        test_cmd = test_libs.replace("==", '-').replace(',', '--')
        cmd = 'dependency_test.bat {} {} s'.format(PYTHON_, test_cmd)
        print('Call', cmd)
        return os.system(cmd)
    elif platform_type == 1:
        cmd = './dependency_test.sh {} {}'.format(PYTHON_, test_libs)
        print('Call', cmd)
        return os.system('./dependency_test.sh {} {}'.format(PYTHON_, test_libs))
    else:
        raise Exception("Not supported platform!")


def main():
    global PYTHON_
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    earliest = list()
    if len(sys.argv) >= 2:
        PYTHON_=sys.argv[1]
    if len(sys.argv) >= 3:
        search_mode = sys.argv[2]
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
