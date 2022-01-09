#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

class TestCustomPrintableClass:
    '''
    @class: This class used to test if display objects can display self defined class noramlly.
    '''
    
    def __init__(self, v1, v2) -> None:
        self._v1 = v1
        self._v2 = v2

    def __repr__(self) -> str:
        return '{}->{}'.format(self._v1, self._v2)


def equal(lhs, rhs, type=str):
    '''
    @function: Check if object lhs equal with rhs.
    @param: {lhs,rhs->iterable(printable)}.
    @return: {bool} Wheather lhs equal with rhs or not.
    '''
    if len(lhs) != len(rhs):
        return False
    for i in range(len(lhs)):
        if type(lhs[i]) != type(rhs[i]):
            return False
    return True


def equal_table(lhs, rhs, type=str):
    '''
    @function: Check if object lhs equal with rhs.
    @param: {lhs,rhs->iteratble(iterable(printable))}.
    @return: {bool} Wheather lhs equal with rhs or not.
    '''
    if len(lhs) != len(rhs):
        return False
    for r in range(len(lhs)):
        if len(lhs[r]) != len(rhs[r]):
            return False
        for c in range(len(lhs[r])):
            if type(lhs[r][c]) != type(rhs[r][c]):
                return False
    return True
