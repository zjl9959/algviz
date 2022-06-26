#!/usr/bin/env python3

"""Define the table data structure related classes.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.svg_table import SvgTable
from algviz.cursor import Cursor, _CursorManager
from algviz.utility import AlgvizParamError, TraceColorStack, clamp
from algviz.utility import kMinCellWidth, kMaxCellWidth, kMinCellHeight, kMaxCellHeight


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
            r (int/Cursor): Set which row in the table to iterate over.
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

    def __init__(self, row, col, data, cell_size, show_index):
        """
        Args:
            row (int): The number of rows for this table.
            col (int): The number of columns for this table.
            data (list(list(printable))): The initial data for table cells.
            cell_size tuple(float, float): Table cell size (width, height).
            show_index (bool): Whether to display table row and column labels.
        
        Raises:
            AlgvizParamError: Table row or col number should > 0.
        """
        if row <=0 or col <=0:
            raise AlgvizParamError('Table row or col number should > 0.')
        if type(cell_size) != tuple or len(cell_size) < 2:
            raise AlgvizParamError('Table cell_size parameter should be <tuple(float, float)> type.')
        self._row = row
        self._col = col
        self._cell_tcs = dict()             # Record the trajectory access information (node_index: ColorStack) of all cells.
        self._frame_trace_old = list()      # Cache the cell related information that needs to be cleared in the previous frame.
        self._frame_trace = list()          # Record the relevant information of the cell to be refreshed in the next frame.
        self._delay = 0                     # Animation frame delay time, used to adapt Visualizer class.
        self._next_row = 0                  # Used to mark which row the current iterated is on for the table.
        self._cell_width = clamp(cell_size[0], kMinCellWidth, kMaxCellWidth)    # The rectangle cells width in table.
        self._cell_height = clamp(cell_size[1], kMinCellHeight, kMaxCellHeight) # The rectangle cells width in table.
        self._cell_margin = 3               # The cell margin between cell and SVG side.
        self._show_index = show_index       # Wheather to show subscript of rows and columns index in table.
        self._label_font_size = 0           # The font size of the subscript labels in table.
        self._index2rect = dict()           # Map the row and column index into rectangle's gid in SVG.
        self._data = [[None for _ in range(self._col)] for _ in range(self._row)]
        self._svg = SvgTable(self._cell_margin, self._cell_margin)
        # Copy data into table.
        if data is not None:
            for r in range(self._row):
                for c in range(self._col):
                    try:
                        self._data[r][c] = data[r][c]
                    except:
                        self._data[r][c] = None
        # Add row and column cursor managers for table.
        self._row_cursor_mgr = _CursorManager((self._cell_width, self._cell_height),
            self._svg, 'R', (self._cell_margin, self._cell_margin), 0)
        self._col_cursor_mgr = _CursorManager((self._cell_width, self._cell_height),
            self._svg, 'D', (self._cell_margin, self._cell_margin), 0)
        # Initial rectangle elemenets in SVG.
        for r in range(self._row):
            for c in range(self._col):
                self._new_rect_in_svg_(r, c)
        # Initial the subscript labels in table.
        if self._show_index:
            self._label_font_size = int(min(12, self._cell_width/len(str(max(self._row,self._col)-1))))
            self._row_index2text = dict()       # Map the row index into the row subscript's text gid in SVG.
            self._col_index2text = dict()       # Map the column index into the row subscript's text gid in SVG.
            for r in range(self._row):
                self._new_row_index_text_in_svg_(r)
            for c in range(self._col):
                self._new_col_index_text_in_svg_(c)
        self._update_svg_size_()
    

    def mark(self, color, r, c, hold=False):
        """Emphasize one cell in the table by mark it's background color.
        
        Args:
            color ((R,G,B)): The background color for the marked cell. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
            r, c (int/Cursor): Index the cell's raw, column in the table to be marked.
            hold (bool): Whether to keep the mark color in future animation frames.
        
        Raises:
            RuntimeError: Index:xx type is not int or Cursor.
            RuntimeError: Table index=xxx out of range.
        """
        r = self._check_index_type_and_range_(r, self._row)
        c = self._check_index_type_and_range_(c, self._col)
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
            r, c (int/Cursor): Index the cell's raw, column in the table.
        
        Returns:
            printable: The value in the specific cell.

        Raises:
            RuntimeError: Index:xx type is not int or Cursor.
            RuntimeError: Table index=xxx out of range.
        """
        if type(r) is Cursor:
            self._add_cursor_(r, True)
        if type(c) is Cursor:
            self._add_cursor_(c, False)
        r = self._check_index_type_and_range_(r, self._row)
        c = self._check_index_type_and_range_(c, self._col)
        return self._data[r][c]
    

    def setItem(self, r, c, val):
        """ Get the cell value in the table.
        
        Args:
            r, c (int/Cursor): Index the cell's raw, column in the table to be modified.
            val (printable): New value for the cell.

        Raises:
            RuntimeError: Index:xx type is not int or Cursor.
            RuntimeError: Table index=xxx out of range.
        """
        if type(r) is Cursor:
            self._add_cursor_(r, True)
        if type(c) is Cursor:
            self._add_cursor_(c, False)
        r = self._check_index_type_and_range_(r, self._row)
        c = self._check_index_type_and_range_(c, self._col)
        gid = self._index2rect[(r, c)]
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

        Raises:
            AlgvizParamError: Table row or col number should > 0.
        """
        if row <=0 or col <=0:
            raise AlgvizParamError('Table row or col number should > 0.')
        if row > self._row:
            # Add new rows into table.
            for r in range(self._row, row):
                self._data.append(list())
                self._new_row_index_text_in_svg_(r)
                for c in range(col):
                    self._data[r].append(None)
                    self._new_rect_in_svg_(r, c)
        elif row < self._row:
            # Remove row in table.
            for r in range(row, self._row):
                self._data.pop()
                self._svg.delete_element(self._row_index2text[r])
                self._row_index2text.pop(r)
                for c in range(self._col):
                    self._svg.delete_element(self._index2rect[(r, c)])
                    self._index2rect.pop((r, c))
        if col > self._col:
            # Add new columns into table.
            for r in range(min(self._row, row)):
                for c in range(self._col, col):
                    self._data[r].append(None)
                    self._new_rect_in_svg_(r, c)
            for c in range(self._col, col):
                self._new_col_index_text_in_svg_(c)
        elif col < self._col:
            for r in range(min(self._row, row)):
                for c in range(col, self._col):
                    self._data[r].pop()
                    self._svg.delete_element(self._index2rect[(r, c)])
                    self._index2rect.pop((r, c))
            for c in range(col, self._col):
                self._svg.delete_element(self._col_index2text[c])
        self._row = row
        self._col = col
        self._update_svg_size_()
        self._update_subscripts_position_()


    def _add_cursor_(self, cursor, is_row):
        """Add a cursor into the cursor manager to track it.
        
        Args:
            cursor (Cursor): The cursor object to track.
        
        Returns:
            bool: Wheather add cursor successfully.
        """
        if type(cursor) != Cursor:
            return False
        need_update_svg = False
        if is_row:
            if not self._row_cursor_mgr.contains(cursor):
                self._row_cursor_mgr.add_cursor(cursor)
                self._col_cursor_mgr.on_svg_margin_changed((
                    self._cell_margin+self._row_cursor_mgr.get_cursors_occupy(), self._cell_margin))
                need_update_svg = True
        else:
            if not self._col_cursor_mgr.contains(cursor):
                self._col_cursor_mgr.add_cursor(cursor)
                self._row_cursor_mgr.on_svg_margin_changed((
                    self._cell_margin, self._cell_margin + self._col_cursor_mgr.get_cursors_occupy()))
                need_update_svg = True
        if need_update_svg:
            self._update_svg_size_()
            self._update_rects_position_()
            self._update_subscripts_position_()
            return True
        return False


    def _remove_cursor_(self, cursor):
        """Remove one cursor from Vector and it's SVG representation.

        Args:
            cursor (Cursor): The cursor object to be removed.
        
        Returns:
            bool: Wheather remove cursor successfully.
        """
        if type(cursor) != Cursor:
            return False
        need_update_svg = False
        if self._row_cursor_mgr.contains(cursor):
            self._row_cursor_mgr.remove_cursor(cursor)
            self._col_cursor_mgr.on_svg_margin_changed((
                self._cell_margin+self._row_cursor_mgr.get_cursors_occupy(), self._cell_margin))
            need_update_svg = True
        if self._col_cursor_mgr.contains(cursor):
            self._col_cursor_mgr.remove_cursor(cursor)
            self._row_cursor_mgr.on_svg_margin_changed((
                self._cell_margin, self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()))
            need_update_svg = True
        if need_update_svg:
            self._update_svg_size_()
            self._update_rects_position_()
            self._update_subscripts_position_()
            return True
        return False


    def __getitem__(self, r):
        """
        Args:
            r (int/Cursor): The index of the row to access.
        
        Returns:
            TabRowIter: The iterator object for the row in the table.

        Raises:
            RuntimeError: Index:xx type is not int or Cursor.
            RuntimeError: Table index=xxx out of range.
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
        svg_width = self._col*self._cell_width + self._cell_margin*2
        svg_height = self._row*self._cell_height + self._cell_margin*2
        svg_width += self._row_cursor_mgr.get_cursors_occupy()
        svg_height += self._col_cursor_mgr.get_cursors_occupy()
        if self._show_index:
            svg_width += len(str(self._row-1))*self._label_font_size
            svg_height += self._label_font_size
        self._svg.update_svg_size(svg_width, svg_height)


    def _update_rects_position_(self):
        for r in range(self._row):
            for c in range(self._col):
                rect_pos_x = c*self._cell_width+self._cell_margin+self._row_cursor_mgr.get_cursors_occupy()
                rect_pos_y = r*self._cell_height+self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()
                rect = (rect_pos_x, rect_pos_y, self._cell_width, self._cell_height)
                gid = self._index2rect[(r, c)]
                self._svg.update_rect_element(gid, rect)


    def _update_subscripts_position_(self):
        for r in range(self._row):
            pos_x = self._col*self._cell_width+self._cell_margin*2+self._row_cursor_mgr.get_cursors_occupy()
            pos_y = (r+0.5)*self._cell_height+self._label_font_size*0.5+self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()
            self._svg.update_text_element(self._row_index2text[r], (pos_x, pos_y))
        for c in range(self._col):
            pos_x = (c+0.5)*self._cell_width-self._label_font_size*len(str(c))*0.25+self._cell_margin+self._row_cursor_mgr.get_cursors_occupy()
            pos_y = self._row*self._cell_height+1+self._label_font_size+self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()
            self._svg.update_text_element(self._col_index2text[c], (pos_x, pos_y))

    def _check_index_type_and_range_(self, index, max_val):
        res = None
        if type(index) is int:
            res = index
        elif type(index) is Cursor:
            res = index.index()
        else:
            raise RuntimeError('Index:{} type is not int or Cursor.'.format(index))
        if index < 0 or index >= max_val:
            raise RuntimeError('Table index={} out of range!'.format(index))
        return res

    def _new_rect_in_svg_(self, r, c):
        rect_pos_x = c*self._cell_width+self._cell_margin+self._row_cursor_mgr.get_cursors_occupy()
        rect_pos_y = r*self._cell_height+self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()
        rect = (rect_pos_x, rect_pos_y, self._cell_width, self._cell_height)
        gid = self._svg.add_rect_element(rect, self._data[r][c], angle=False)
        self._index2rect[(r, c)] = gid
        self._cell_tcs[gid] = TraceColorStack()

    def _new_row_index_text_in_svg_(self, r):
        pos_x = self._col*self._cell_width+self._cell_margin*2+self._row_cursor_mgr.get_cursors_occupy()
        pos_y = (r+0.5)*self._cell_height+self._label_font_size*0.5+self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()
        gid = self._svg.add_text_element((pos_x, pos_y), r, self._label_font_size)
        self._row_index2text[r] = gid

    def _new_col_index_text_in_svg_(self, c):
        pos_x = (c+0.5)*self._cell_width-self._label_font_size*len(str(c))*0.25+self._cell_margin+self._row_cursor_mgr.get_cursors_occupy()
        pos_y = self._row*self._cell_height+1+self._label_font_size+self._cell_margin+self._col_cursor_mgr.get_cursors_occupy()
        gid = self._svg.add_text_element((pos_x, pos_y), c, self._label_font_size)
        self._col_index2text[c] = gid
