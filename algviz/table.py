#!/usr/bin/env python3

"""Define the table data structure related classes.

Author: zjl9959@gmail.com

License: GPLv3

"""

from . import svg_table
from . import utility


class TableRowIter():
    """An iterator that iterate on one specifies row in Table object.
    """

    def __init__(self, r, tab):
        """
        Args:
            r (int): Set which row in the table to iterate over.
            tab (Table): Bounded Table object for this Iterator.
        """
        self._r = r
        self._c = 0
        self._tab = tab
        
    def __iter__(self):
        self._c = 0
        return self
    
    def __next__(self):
        if self._c >= self._tab._col:
            raise StopIteration
        else:
            res = self._tab.getItem(self._r, self._c)
            self._c += 1
            return res


class TableRowOperator():
    """A manipulator to get/set the elements of the specified row in the table.
    """

    def __init__(self, r, tab):
        """
        Args:
            r (int): Set which row in the table to iterate over.
            tab (Table): Bounded Table object for this Iterator.
        """
        self._r = r
        self._tab = tab
        
    def __getitem__(self, c):
        return self._tab.getItem(self._r, c)
        
    def __setitem__(self, c, val):
        self._tab.setItem(self._r, c, val)


class Table():
    """A static table with label text in table cells.
    
    [WARNING] Don't create this class directly, use algviz.Visualizer.createTable instead.
    """

    def __init__(self, row, col, data, cell_size, show_index=True):
        """
        Args:
            row (int): The number of rows for this table.
            col (int): The number of columns for this table.
            data (list(list(printable))): The initial data for table cells.
            cell_size (float): Table cell size.
            show_index (bool): Whether to display table row and column labels.
        
        Raises:
            Exception: Table row or col error!
        """
        if row <=0 or col <=0:
            raise Exception('Table row or col error!')
        self._row = row
        self._col = col
        self._cell_tcs = dict()           # Record the trajectory access information (node_index: ColorStack) of all cells.
        self._frame_trace_old = list()    # Cache the cell related information that needs to be cleared in the previous frame.
        self._frame_trace = list()        # Record the relevant information of the cell to be refreshed in the next frame.
        self._delay = 0                   # Animation frame delay time, used to adapt Visualizer class.
        self._next_row = 0                # Used to mark which row the current iterated is on for the table.
        self._data = [[None for _ in range(col)] for _ in range(row)]
        label_font_size = int(min(12, cell_size/len(str(max(row,col)-1))))
        table_margin = 3
        svg_width = col*cell_size + table_margin*2
        svg_height = row*cell_size + table_margin*2
        if show_index:
            svg_width += len(str(row-1))*label_font_size
            svg_height += label_font_size
        self._svg = svg_table.SvgTable(svg_width, svg_height)
        # Copy data into table.
        if data is not None:
            for r in range(self._row):
                for c in range(self._col):
                    try:
                        self._data[r][c] = data[r][c]
                    except:
                        self._data[r][c] = None
        # initialization SVG contain.
        for r in range(self._row):
            for c in range(self._col):
                rect = (c*cell_size+table_margin, r*cell_size+table_margin, cell_size, cell_size)
                self._svg.add_rect_element(rect, self._data[r][c], angle=False)
                self._cell_tcs[r*col+c] = utility.TraceColorStack()
        if show_index:
            for r in range(row):
                pos = (col*cell_size+table_margin*2, (r+0.5)*cell_size+label_font_size*0.5+table_margin)
                self._svg.add_text_element(pos, r, font_size=label_font_size)
            for c in range(col):
                pos = ((c+0.5)*cell_size-label_font_size*len(str(c))*0.25+table_margin, row*cell_size+1+label_font_size+table_margin)
                self._svg.add_text_element(pos, c, font_size=label_font_size)
    

    def mark(self, color, r, c, hold=True):
        """Emphasize one cell in the table by mark it's background color.
        
        Args:
            color ((R,G,B)): The background color for the marked cell. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
            r, c (int): Index the cell's raw, column in the table to be marked.
            hold (bool): Whether to keep the mark color in future animation frames.
        
        Raises:
            Exception: Table index out of range!
        """
        if r < 0 or r >= self._row or c < 0 or c >= self._col:
            raise Exception("Table index out of range!")
        gid = r*self._col + c
        self._cell_tcs[gid].add(color)
        self._frame_trace.append((gid, color, hold))
    

    def removeMark(self, color):
        """Remove the mark color for cell(s).

        Args:
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        """
        for gid in range(self._row*self._col):
            if self._cell_tcs[gid].remove(color):
                self._svg.update_rect_element(gid, fill=self._cell_tcs[gid].color())
    

    def getItem(self, r, c):
        """Get the cell value in the table.
        
        Args:
            r, c (int): Index the cell's raw, column in the table.
        
        Returns:
            printable: The value in the specific cell.

        Raises:
            Exception: Table index out of range!
        """
        if r < 0 or r >= self._row or c < 0 or c >= self._col:
            raise Exception("Table index out of range!")
        gid = r*self._col + c
        self._cell_tcs[gid].add(utility._getElemColor)
        self._frame_trace.append((gid, utility._getElemColor, False))
        return self._data[r][c]
    

    def setItem(self, r, c, val):
        """ Get the cell value in the table.
        
        Args:
            r, c (int): Index the cell's raw, column in the table to be modified.
            val (printable): New value for the cell.

        Raises:
            Exception: Table index out of range!
        """
        if r < 0 or r >= self._row or c < 0 or c >= self._col:
            raise Exception("Table index out of range!")
        gid = r*self._col + c
        self._cell_tcs[gid].add(utility._setElemColor)
        self._frame_trace.append((gid, utility._setElemColor, False))
        label = val
        if val is None:
            label = ''
        self._svg.update_rect_element(gid, text=label)
        self._data[r][c] = val
    

    def shape(self):
        """
        Returns:
            tuple(int, int): Return the rows and columns of this table.
        """
        return (self._row, self._col)


    def __getitem__(self, r):
        """
        Args:
            r (int): The index of the row to access.
        
        Returns:
            TabRowIter: The iterator object for the row in the table.
        """
        return TableRowOperator(r, self)

    
    def __iter__(self):
        self._next_row = 0
        return self
    

    def __next__(self):
        if self._next_row >= self._row:
            raise StopIteration
        else:
            res = TableRowIter(self._next_row, self)
            self._next_row += 1
            return res
    

    def _repr_svg_(self):
        """
        Returns:
            str: The SVG representation of current table.
        """
        for (gid, color) in self._frame_trace_old:
            if (gid, color, True) not in self._frame_trace and (gid, color, False) not in self._frame_trace:
                self._cell_tcs[gid].remove(color)
            self._svg.update_rect_element(gid, fill=self._cell_tcs[gid].color())
        self._frame_trace_old.clear()
        for (gid, color, hold) in self._frame_trace:
            self._svg.update_rect_element(gid, fill=self._cell_tcs[gid].color())
            if not hold:
                self._frame_trace_old.append((gid, color))
        self._frame_trace.clear()
        return self._svg._repr_svg_()
