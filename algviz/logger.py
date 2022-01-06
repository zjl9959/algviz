#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''


class Logger():
    '''
    @class: A log class to display strings into the screen.
    '''

    def __init__(self, buffer_lines):
        '''
        @param: {buffer_lines->int} Max buffer lines for cached logs. Override the oldest line if overflow.
        '''
        self._buffer_lines = max(buffer_lines, 1)
        self._logs = list()
    

    def write(self, data):
        '''
        @function: Write log data. Use '\n' to split multi-lines.
        @param: {data->str} The log data string.
        '''
        data_lines = data.split('\n')
        for line in data_lines:
            if len(self._logs) >= self._buffer_lines:
                self._logs.pop(0)
            self._logs.append(line)
    

    def clear(self):
        '''
        function: Clear all cached logs.
        '''
        self._logs.clear()
    
    def __repr__(self):
        res = str()
        for s in self._logs:
            res += s + '\n'
        return res
