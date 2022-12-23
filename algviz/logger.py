#!/usr/bin/env python3

"""Define the Logger related classes.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.utility import get_text_width

from xml.dom.minidom import Document


LOG_OFFSET_X = 5


class Logger():
    """A log class to display strings into the screen.

    You can write string into this logger object, it will separate lines by \\n.
    And if the buffer lines overflow, the oldest lines in the buffer will be discard.
    """

    def __init__(self, buffer_lines, font_size, show_line_num):
        """
        Args:
            buffer_lines (int): Set the max buffer lines for cached logs. Override the oldest line if overflow.
        """
        self._buffer_lines = max(buffer_lines, 1)
        font_size = int(font_size)
        self._font_size = 12
        if font_size > 1 and font_size <= 16:
            self._font_size = font_size
        self._logs = list()
        self._dom = Document()
        self._svg = self._dom.createElement('svg')
        self._svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self._dom.appendChild(self._svg)
        self._next_node_id = 0
        self._log_lines = 0
        self._show_line_num = show_line_num

    def write(self, data):
        """Write log data. Use \\n to split multi-lines.

        Args:
            data (str): The log data string.
        """
        data_lines = data.split('\n')
        if len(data_lines) > self._buffer_lines:
            data_lines = data_lines[len(data_lines) - self._buffer_lines:]
        if len(data_lines) + len(self._logs) > self._buffer_lines:
            self._logs = self._logs[len(data_lines) + len(self._logs) - self._buffer_lines:]
        for line in data_lines:
            if self._show_line_num:
                self._logs.append('{}. {}'.format(self._log_lines, line))
            else:
                self._logs.append(line)
            self._log_lines += 1

    def clear(self):
        """Clear all cached log string.
        """
        self._log_lines = 0
        for child in self._svg.childNodes:
            self._svg.removeChild(child)
        self._logs.clear()

    def _repr_svg_(self):
        svg_width = 0
        for child in self._svg.childNodes:
            self._svg.removeChild(child)
        g = self._dom.createElement('g')
        g.setAttribute('id', str(self._next_node_id))
        self._next_node_id += 1
        for i in range(len(self._logs)):
            log = self._logs[i]
            txt = self._dom.createElement('text')
            txt.setAttribute('x', '{}'.format(LOG_OFFSET_X))
            txt.setAttribute('y', '{:.2f}'.format(self._font_size * (i * 1.2 + 1)))
            txt.setAttribute('font-size', '{:.2f}'.format(self._font_size))
            txt.setAttribute('font-family', 'cursive')
            text = self._dom.createTextNode('{}'.format(log))
            txt.appendChild(text)
            g.appendChild(txt)
            svg_width = max(svg_width, get_text_width(log, self._font_size) + LOG_OFFSET_X)
        self._svg.appendChild(g)
        # Update svg width and height.
        svg_height = len(self._logs) * self._font_size * 1.3
        self._svg.setAttribute('width', '{:.0f}pt'.format(svg_width))
        self._svg.setAttribute('height', '{:.0f}pt'.format(svg_height))
        self._svg.setAttribute('viewBox', '0.00 0.00 {:.2f} {:.2f}'.format(svg_width, svg_height))
        return self._dom.toxml()
