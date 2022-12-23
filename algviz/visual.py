#!/usr/bin/env python3

"""Define visual class in jupyter notebook.

Author: zjl9959@gmail.com

License: GPLv3

"""

from weakref import WeakKeyDictionary
from time import sleep
from IPython import display

from algviz.table import Table
from algviz.vector import Vector
from algviz.svg_graph import SvgGraph
from algviz.svg_table import SvgTable
from algviz.logger import Logger
from algviz.cursor import Cursor, _CursorRange
from algviz.map import Map
from algviz.utility import AlgvizParamError, AlgvizTypeError, kMaxNameChars


class _NoDisplay():
    def _repr_svg_(self):
        return ''


class _NameDisplay():
    def __init__(self, name):
        if type(name) != str or len(name) > kMaxNameChars:
            raise AlgvizParamError('name "{}" not str or exceed {} characters.'.format(name, kMaxNameChars))
        self._name = name + ':'

    def __repr__(self):
        return self._name


_next_display_id = 0


class Visualizer():

    def __init__(self, delay=2.0, wait=0.5):
        """
        Args:
            delay (float): Animation delay time (in seconds).
            wait (True/float/int): (True) wait for the key input to continue execute the code.
                                   (float/int) the wait time before start the next frame of animation.
        """
        self._delay = 2.0               # Set default delay time for animation as 3.0 seconds.
        if delay > 0:
            self._delay = delay
        self._wait = wait
        if type(self._wait) != bool and type(self._wait) != float and type(self._wait) != int:
            self._wait = 0.5
        if type(self._wait) == bool and self._wait is False:
            self._wait = 0.5
        if type(self._wait) != bool and self._wait < 0:
            self._wait = 0

        # The mapping relationship between the display object and the display id.
        self._element2display = WeakKeyDictionary()
        # Record the displayed id. If object is not displayed, call the display interface, otherwise call the update interface.
        self._displayed = set()
        # The mapping relationship between the display object and the object's name.
        self._displayid2name = dict()
        # The next unique cursor id created by this visualizer.
        self._next_cursor_id = -1

    def display(self, delay=None):
        """Refresh all created display objects.

        Args:
            delay (float): Specific the delay time for this animation frame (in seconds).
        """
        if delay is None or delay < 0:
            delay = self._delay
        if type(self._wait) == float or type(self._wait) == int:
            for elem in self._element2display.keyrefs():
                did = self._element2display[elem()]
                if did not in self._displayed:
                    if did in self._displayid2name:
                        svg_title = _NameDisplay(self._displayid2name[did])
                        display.display(svg_title, display_id='algviz_{}'.format(did))
                    elem()._delay = delay
                    display.display(elem(), display_id='algviz{}'.format(did))
                    self._displayed.add(did)
                else:
                    if did in self._displayid2name:
                        svg_title = _NameDisplay(self._displayid2name[did])
                        display.update_display(svg_title, display_id='algviz_{}'.format(did))
                    elem()._delay = delay
                    display.update_display(elem(), display_id='algviz{}'.format(did))
            temp_displayed = list(self._displayed)
            for did in temp_displayed:
                if did not in self._element2display.values():
                    if did in self._displayid2name:
                        display.update_display(_NoDisplay(), display_id='algviz_{}'.format(did))
                    display.update_display(_NoDisplay(), display_id='algviz{}'.format(did))
                    self._displayed.remove(did)
            sleep(delay + self._wait)
            return None
        else:
            display.clear_output(wait=True)
            for elem in self._element2display.keyrefs():
                did = self._element2display[elem()]
                if did in self._displayid2name:
                    svg_title = SvgTable(400, 17)
                    title_name = '{}:'.format(self._displayid2name[did])
                    svg_title.add_text_element((4, 14), title_name, font_size=14, fill=(0, 0, 0))
                    display.display(svg_title, display_id='algviz_{}'.format(did))
                elem()._delay = delay
                display.display(elem(), display_id='algviz{}'.format(did))
                self._displayed.add(did)
            return input('Input `Enter` to continue:')

    def createTable(self, row, col, data=None, name=None, cell_size=(40, 40), show_index=True):
        """
        Args:
            row, col (int): The number of rows, columns for this table.
            data (list(list(printable))): The initial data for table cells.
            name (str): The name of this table object.
            cell_size tuple(float, float): Table cell size (width, height).
            show_index (bool): Whether to display table row and column labels.

        Returns:
            Table: New created Table object.
        """
        global _next_display_id
        tab = Table(row, col, data, cell_size, show_index)
        self._element2display[tab] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return tab

    def createVector(self, data=None, name=None, cell_size=(40, 40), histogram=False, show_index=True):
        """
        Args:
            data (list(printable)): The initial data for vector cells.
            name (str): The name of this Vector object.
            cell_size tuple(float, float): Vector cell size (width, height).
            histogram (bool): Display the data in the form of a histogram or not.
            show_index (bool): Whether to display the vector index label.

        Returns:
            Vector: New created Vector object.
        """
        global _next_display_id
        vec = Vector(data, self._delay, cell_size, histogram, show_index)
        self._element2display[vec] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return vec

    def createGraph(self, data=None, name=None, directed=True):
        """
        Args:
            data (iterable): The root node(s) to initialize the topology graph.
            name (str): The name of this Vector object.
            directed (bool): Should this graph be directed graph or undirected.

        Returns:
            SvgGraph: Created SvgGraph object.
        """
        global _next_display_id
        gra = SvgGraph(data, directed, self._delay)
        self._element2display[gra] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return gra

    def createMap(self, data=None, name=None):
        """
        Args:
            data (dict): The initial key and values of this map.
            name (str): The name of this Map object.

        Returns:
            Map: Created Map object.
        """
        global _next_display_id
        map = Map(data, self._delay)
        self._element2display[map] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return map

    def createLogger(self, buffer_lines=10, name=None, font_size=12, show_line_num=True):
        """
        Args:
            buffer_lines (int): Maximum buffer line of this logger.
            name (str): The name of this Vector object.

        Returns:
            Logger: Created Logger object.
        """
        global _next_display_id
        logg = Logger(buffer_lines, font_size, show_line_num)
        self._element2display[logg] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return logg

    def createCursor(self, offset=0, name=None):
        """
        Args:
            offset (int/Cursor): The cursor's index position offset.
            name (str): The name of this Cursor object.

        Returns:
            Cursor: Created Cursor object.
        """
        if type(offset) is Cursor:
            offset = offset.index()
        self._next_cursor_id += 1
        return Cursor(name, offset, self._next_cursor_id)

    def removeCursor(self, cursor):
        """
        Args:
            cursor (Cursor): The cursor object to be removed from this visualizer.
        """
        if type(cursor) != Cursor:
            raise AlgvizTypeError('removeCursor object is not a Cursor type.')
        for elem in self._element2display.keyrefs():
            element = elem()
            if not element or (type(element) != Vector and type(element) != Table):
                continue
            element._remove_cursor_(cursor)

    def cursorRange(self, st, ed, step=1, name=None):
        """
        Args:
            st/ed (int/Cursor): The start/end of cursor index.
            step (int/Cursor): The change step of this cursor's index(default->1).
            name (str): The display name of this cursor(default->None).

        Returns:
            _CursorRange: the iterator of Cursor objects.
        """
        if type(st) is Cursor:
            st = st.index()
        if type(ed) is Cursor:
            ed = ed.index()
        self._next_cursor_id += 1
        return _CursorRange(self._next_cursor_id, name, st, ed, step)
