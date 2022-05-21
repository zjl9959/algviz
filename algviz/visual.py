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


class _NoDisplay():
    def _repr_svg_(self):
        return ''


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
        if type(self._wait) == bool and self._wait == False:
            self._wait = 0.5
        if type(self._wait) != bool and self._wait < 0:
            self._wait = 0
        
        # The mapping relationship between the display object and the display id.
        self._element2display = WeakKeyDictionary()
        
        # Record the displayed id. If object is not displayed, call the display interface, otherwise call the update interface.
        self._displayed = set()
        
        # The mapping relationship between the display object and the object's name.
        self._displayid2name = dict()


    def display(self, delay=None):
        """Refresh all created display objects.
        
        Args:
            delay (float): Specific the delay time for this animation frame (in seconds).
        """
        if delay == None:
            delay = self._delay
        if type(self._wait) == float or type(self._wait) == int:
            for elem in self._element2display.keyrefs():
                did = self._element2display[elem()]
                if did not in self._displayed:
                    if did in self._displayid2name:
                        svg_title = SvgTable(400, 17)
                        title_name = '{}:'.format(self._displayid2name[did])
                        svg_title.add_text_element((4, 14), title_name, font_size=14, fill=(0,0,0))
                        display.display(svg_title, display_id='algviz_{}'.format(did))
                    elem()._delay = delay
                    display.display(elem(), display_id='algviz{}'.format(did))
                    self._displayed.add(did)
                else:
                    if did in self._displayid2name:
                        svg_title = SvgTable(400, 17)
                        title_name = '{}:'.format(self._displayid2name[did])
                        svg_title.add_text_element((4, 14), title_name, font_size=14, fill=(0,0,0))
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
                    svg_title.add_text_element((4, 14), title_name, font_size=14, fill=(0,0,0))
                    display.display(svg_title, display_id='algviz_{}'.format(did))
                elem()._delay = delay
                display.display(elem(), display_id='algviz{}'.format(did))
                self._displayed.add(did)
            return input('Input `Enter` to continue:')


    def createTable(self, row, col, data=None, name=None, cell_size=40, show_index=True):
        """
        Args:
            row, col (int): The number of rows, columns for this table.
            data (list(list(printable))): The initial data for table cells.
            name (str): The name of this table object.
            cell_size (float): Table cell size.
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


    def createVector(self, data=None, name=None, cell_size=40, bar=-1, show_index=True):
        """
        Args:
            data (list(printable)): The initial data for vector cells.
            name (str): The name of this Vector object.
            cell_size (float): Vector cell size.
            bar (float): If bar < 0, ignore it. otherwise display the data in the form of a histogram, and bar is histogram's maximum height.
            show_index (bool): Whether to display the vector index label.
        
        Returns:
            Vector: New created Vector object.
        """
        global _next_display_id
        vec = Vector(data, self._delay, cell_size, bar, show_index)
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


    def createLogger(self, buffer_lines=10, name=None):
        """
        Args:
            buffer_lines (int): Maximum buffer line of this logger.
            name (str): The name of this Vector object.
        
        Returns:
            Logger: Created Logger object.
        """
        global _next_display_id
        logg = Logger(buffer_lines)
        self._element2display[logg] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return logg
