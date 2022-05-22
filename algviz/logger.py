#!/usr/bin/env python3

"""Define the Logger related classes.

Author: zjl9959@gmail.com

License: GPLv3

"""

class Logger():
    """A log class to display strings into the screen.

    You can write string into this logger object, it will separate lines by \\n.
    And if the buffer lines overflow, the oldest lines in the buffer will be discard.
    """

    def __init__(self, buffer_lines):
        """
        Args:
            buffer_lines (int): Set the max buffer lines for cached logs. Override the oldest line if overflow.
        """
        self._buffer_lines = max(buffer_lines, 1)
        self._logs = list()
    

    def write(self, data):
        """Write log data. Use \\n to split multi-lines.
        
        Args:
            data (str): The log data string.
        """
        data_lines = data.split('\n')
        for line in data_lines:
            if len(self._logs) >= self._buffer_lines:
                self._logs.pop(0)
            self._logs.append(line)
    

    def clear(self):
        """Clear all cached log string.
        """
        self._logs.clear()
    

    def __repr__(self):
        res = str()
        for s in self._logs:
            res += s + '\n'
        return res
