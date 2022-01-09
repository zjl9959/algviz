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
