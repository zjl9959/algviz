#!/usr/bin/env python3

"""Define the table data structure related classes.

Author: zjl9959@gmail.com

License: GPLv3

"""

from . import svg_table
from . import cursor
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
        self._cell_tcs = dict()             # Record the trajectory access information (node_index: ColorStack) of all cells.
        self._frame_trace_old = list()      # Cache the cell related information that needs to be cleared in the previous frame.
        self._frame_trace = list()          # Record the relevant information of the cell to be refreshed in the next frame.
        self._delay = 0                     # Animation frame delay time, used to adapt Visualizer class.
        self._next_row = 0                  # Used to mark which row the current iterated is on for the table.
        self._cell_size = cell_size         # The rectangle cells size(width and height) in table.
        self._cell_margin = 3               # The cell margin between the elements in table.
        self._show_index = show_index       # Wheather to show subscript of rows and columns index in table.
        self._label_font_size = 0           # The font size of the subscript labels in table.
        self._index2rect = dict()           # Map the row and column index into rectangle's gid in SVG.
        self._data = [[None for _ in range(self._col)] for _ in range(self._row)]
        self._svg = svg_table.SvgTable(self._cell_margin, self._cell_margin)
        # Copy data into table.
        if data is not None:
            for r in range(self._row):
                for c in range(self._col):
                    try:
                        self._data[r][c] = data[r][c]
                    except:
                        self._data[r][c] = None
        # Initial rectangle elemenets in SVG.
        for r in range(self._row):
            for c in range(self._col):
                rect_pos_x = c*self._cell_size+self._cell_margin
                rect_pos_y = r*self._cell_size+self._cell_margin
                rect = (rect_pos_x, rect_pos_y, self._cell_size, self._cell_size)
                gid = self._svg.add_rect_element(rect, self._data[r][c], angle=False)
                self._index2rect[(r, c)] = gid
                self._cell_tcs[gid] = utility.TraceColorStack()
        # Initial the subscript labels in table.
        if self._show_index:
            self._label_font_size = int(min(12, self._cell_size/len(str(max(self._row,self._col)-1))))
            self._row_index2text = dict()       # Map the row index into the row subscript's text gid in SVG.
            self._col_index2text = dict()       # Map the column index into the row subscript's text gid in SVG.
            for r in range(self._row):
                pos_x = self._col*self._cell_size+self._cell_margin*2
                pos_y = (r+0.5)*self._cell_size+self._label_font_size*0.5+self._cell_margin
                gid = self._svg.add_text_element((pos_x, pos_y), r, self._label_font_size)
                self._row_index2text[r] = gid
            for c in range(self._col):
                pos_x = (c+0.5)*self._cell_size-self._label_font_size*len(str(c))*0.25+self._cell_margin
                pos_y = self._row*self._cell_size+1+self._label_font_size+self._cell_margin
                gid = self._svg.add_text_element((pos_x, pos_y), c, self._label_font_size)
                self._col_index2text[c] = gid
        # Add row and column cursor managers for table.
        self._row_cursor_mgr = cursor._CursorManager(self._cell_size,
            self._svg, 'R', (self._cell_margin, 0))
        self._col_cursor_mgr = cursor._CursorManager(self._cell_size,
            self._svg, 'D', (self._cell_margin, 0))
        self._update_svg_size_()
    

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
        gid = self._index2rect[(r, c)]
        self._cell_tcs[gid].add(color)
        self._frame_trace.append((gid, color, hold))
    

    def removeMark(self, color):
        """Remove the mark color for cell(s).

        Args:
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        """
        for gid in self._index2rect.values():
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
        gid = self._index2rect[(r, c)]
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
        gid = self._index2rect[(r, c)]
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

    
    def reshape(self, row, col):
        """Reshape the row and column size of this table.
        row, col (int): The new row and column number of the table.
        """
        raise Exception("[ERROR]Not implement!")


    def new_row_cursor(self, name=None, offset=0):
        """Create a new cursor to track the rows in table.
        
        Args:
            name (str): The cursor's name to be displayed.
            offset (int): The cursor's initital index offset.
        
        Returns:
            Cursor: Return the new created Cursor object.
        """
        res_cursor = None
        res_cursor = self._row_cursor_mgr.new_cursor(name, offset)
        res_cursor._dir = 'R'
        self._update_svg_size_()
        self._update_rects_position_()
        self._update_subscripts_position_()
        return res_cursor


    def new_col_cursor(self, name=None, offset=0):
        """Create a new cursor to track the columns in table.
        
        Args:
            name (str): The cursor's name to be displayed.
            offset (int): The cursor's initital index offset.
        
        Returns:
            Cursor: Return the new created Cursor object.
        """
        res_cursor = None
        res_cursor = self._col_cursor_mgr.new_cursor(name, offset)
        res_cursor._dir = 'U'
        self._update_svg_size_()
        self._update_rects_position_()
        self._update_subscripts_position_()
        return res_cursor


    def remove_cursor(self, cursor_obj):
        """Remove one cursor from Vector and it's SVG representation.

        Args:
            cursor_obj (Cursor): The cursor object to be removed.
        """
        if type(cursor_obj) != cursor.Cursor:
            return
        if cursor_obj._dir == 'R':
            self._row_cursor_mgr.remove_cursor(cursor_obj._id)
        elif cursor_obj._dir == 'U':
            self._col_cursor_mgr.remove_cursor(cursor_obj._id)
        else:
            return
        self._update_svg_size_()
        self._update_rects_position_()
        self._update_subscripts_position_()


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
        self._row_cursor_mgr.refresh_cursors_animation(self._row, (0, self._delay))
        self._col_cursor_mgr.refresh_cursors_animation(self._col, (0, self._delay))
        res_svg = self._svg._repr_svg_()
        self._frame_trace.clear()
        self._row_cursor_mgr.update_cursors_position()
        self._col_cursor_mgr.update_cursors_position()
        return res_svg


    def _update_svg_size_(self):
        svg_width = self._col*self._cell_size + self._cell_margin*2
        svg_height = self._row*self._cell_size + self._cell_margin*2
        svg_width += self._row_cursor_mgr.get_cursors_occupy()
        svg_height += self._col_cursor_mgr.get_cursors_occupy()
        if self._show_index:
            svg_width += len(str(self._row-1))*self._label_font_size
            svg_height += self._label_font_size
        self._svg.update_svg_size(svg_width, svg_height)


    def _update_rects_position_(self):
        for r in range(self._row):
            for c in range(self._col):
                rect_pos_x = c*self._cell_size+self._cell_margin+self._row_cursor_mgr.get_cursors_occupy()
                rect_pos_y = r*self._cell_size+self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()
                rect = (rect_pos_x, rect_pos_y, self._cell_size, self._cell_size)
                gid = self._index2rect[(r, c)]
                self._svg.update_rect_element(gid, rect)


    def _update_subscripts_position_(self):
        for r in range(self._row):
            pos_x = self._col*self._cell_size+self._cell_margin*2+self._row_cursor_mgr.get_cursors_occupy()
            pos_y = (r+0.5)*self._cell_size+self._label_font_size*0.5+self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()
            self._svg.update_text_element(self._row_index2text[r], (pos_x, pos_y))
        for c in range(self._col):
            pos_x = (c+0.5)*self._cell_size-self._label_font_size*len(str(c))*0.25+self._cell_margin+self._row_cursor_mgr.get_cursors_occupy()
            pos_y = self._row*self._cell_size+1+self._label_font_size+self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()
            self._svg.update_text_element(self._col_index2text[c], (pos_x, pos_y))
