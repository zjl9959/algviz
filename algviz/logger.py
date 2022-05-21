#!/usr/bin/env python3

"""Define the Logger related classes.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.utility import get_text_width

from xml.dom.minidom import Document


class Logger():
    """A log class to display strings into the screen.

    You can write string into this logger object, it will separate lines by \\n.
    And if the buffer lines overflow, the oldest lines in the buffer will be discard.
    """

    def __init__(self, buffer_lines, font_size=12):
        """
        Args:
            buffer_lines (int): Set the max buffer lines for cached logs. Override the oldest line if overflow.
        """
        self._buffer_lines = max(buffer_lines, 1)
        font_size = int(font_size)
        self._font_size = font_size if font_size > 0 else 16
        self._logs = list()
        self._log_text_nodes = list()
        self._log_text_width = list()
        self._dom = Document()
        self._svg = self._dom.createElement('svg')
        self._svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self._dom.appendChild(self._svg)
    

    def write(self, data):
        """Write log data. Use \\n to split multi-lines.
        
        Args:
            data (str): The log data string.
        """
        data_lines = data.split('\n')
        for line in data_lines:
            if len(self._logs) >= self._buffer_lines:
                self._logs.pop(0)
                if len(self._log_text_width):
                    self._log_text_width.pop(0)
                if len(self._log_text_nodes):
                    txt_node = self._log_text_nodes.pop(0)
                    self._svg.removeChild(txt_node)
            self._logs.append(line)
    

    def clear(self):
        """Clear all cached log string.
        """
        self._logs.clear()
        self._log_text_width.clear()
        for node in self._log_text_nodes:
            self._svg.removeChild(node)
        self._log_text_nodes.clear()


    def _repr_svg_(self):
        for i in range(len(self._log_text_nodes), len(self._logs)):
            log = self._logs[i]
            txt = self._dom.createElement('text')
            txt.setAttribute('x', '10')
            txt.setAttribute('y', '{:.2f}'.format(self._font_size*(i*1.2+1)))
            txt.setAttribute('font-size', '{:.2f}'.format(self._font_size))
            txt.setAttribute('font-family', 'Times,serif')
            text = self._dom.createTextNode('{}'.format(log))
            txt.appendChild(text)
            self._svg.appendChild(txt)
            self._log_text_width.append(get_text_width(log, self._font_size))
            self._log_text_nodes.append(txt)
        # Update svg width and height.
        svg_width = max(self._log_text_width+[0])*0.6 + 10
        svg_height = len(self._logs)*self._font_size*1.2
        self._svg.setAttribute('width', '{:.0f}pt'.format(svg_width))
        self._svg.setAttribute('height', '{:.0f}pt'.format(svg_height))
        self._svg.setAttribute('viewBox', '0.00 0.00 {:.2f} {:.2f}'.format(svg_width, svg_height))
        return self._dom.toxml()
