#!/usr/bin/env python3


"""Define the table data structure.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.svg_table import SvgTable
from algviz.cursor import Cursor, _CursorManager
from algviz.utility import TraceColorStack, AlgvizParamError, clamp
from algviz.utility import kMinAnimDelay, kMaxAnimDelay, kMinCellWidth
from algviz.utility import kMaxCellWidth, kMaxBarHight, kMinCellHeight, kMaxCellHeight


class Vector():
    """
    A vector is an expandable list, you can add or remove cell for vector.
    When the cell position changed, the vector display SVG will show the related animation.
    
    [WARNING] Don't create this class directly, use algviz.Visualizer.createTable instead.
    """

    def __init__(self, data, delay, cell_size, histogram, show_index):
        """
        Args:
            data (list(printable)): The initialize data for vector.
            delay (float): Animation delay time between two animation frames.
            cell_size tuple(float, float): Vector cell size (width, height).
            histogram (bool): Display the data in the form of a histogram or not.
            show_index (bool): Whether to display the vector index label.
        """
        if type(cell_size) != tuple or len(cell_size) < 2:
            raise AlgvizParamError('Vector cell_size parameter should be <tuple(float, float)> type.')
        self._data = list()             # Store the data in vector list.
        if data is not None:
            for i in range(len(data)):
                self._data.append(data[i])
        self._delay = clamp(delay, kMinAnimDelay, kMaxAnimDelay)                 # Animation delay time.
        self._cell_width = clamp(cell_size[0], kMinCellWidth, kMaxCellWidth)
        if histogram:
            self._cell_height = clamp(cell_size[1], kMinCellHeight, kMaxBarHight)
        else:
            self._cell_height = clamp(cell_size[1], kMinCellHeight, kMaxCellHeight)
        self._show_histogram = histogram          
        self._show_index = show_index   # Whether to display the vector index label.
        self._cell_margin = 3           # Margin between two adjacent cells.
        self._cell_tcs = dict()         # Record the trajectory access information (node_index: ColorStack) of all cells.
        self._frame_trace_old = list()  # Cache the cell related information that needs to be cleared in the previous frame.
        self._frame_trace = list()      # Record the relevant information of the cell to be refreshed in the next frame.
        self._rect_move = dict()        # Record the index of moving cells and it's relative moving distance in the next frame.
        self._rect_disappear = list()   # Record the index of disappearing cells in the next frame.
        self._rect_appear = list()      # Record the index of appearing cells in the next frame.
        self._index2rect = dict()       # The mapping relationship from vector index to the cell object.
        self._index2text = dict()       # The mapping relationship from vector index to the text object.
        self._label_font_size = int(min(12, self._cell_width*0.5))   # The font size of the vector's subscript index.
        self._next_iter = 0             # Mark the positon of current iteration.
        self._svg = SvgTable(self._cell_margin, self._cell_margin)
        # Initial cursor manager.
        self._cursor_manager = _CursorManager((self._cell_width, self._cell_width), self._svg, 'D',
            (self._cell_margin, self._cell_margin), self._cell_margin)
        # Create rect elements for initial data.
        for i in range(len(self._data)):
            rect_pos_x = self._cell_width*i + self._cell_margin*(i+1)
            rect_pos_y = self._cell_margin + self._cursor_manager.get_cursors_occupy()
            rect = (rect_pos_x, rect_pos_y, self._cell_width, self._cell_height)
            rid = self._svg.add_rect_element(rect, text=self._data[i])
            self._cell_tcs[rid] = TraceColorStack()
            self._index2rect[i] = rid
        # Update SVG and rects size.
        self._update_svg_size_(len(self._data))
        if self._show_histogram:
            self._update_bar_height_()
        if self._show_index:
            self._create_new_subscripts_(0, len(self._data))


    def insert(self, index, val):
        """Insert a new value into vector. If index < 0 or index >= length of Vector, then set index = index % vector length.
        
        Args:
            index (int/Cursor): The subscript index to insert value. (Insert before index)
            val (printable): The value to insert into vector.

        Raises:
            RuntimeError: Index:xxx type is not int or Cursor.
            RuntimeError:  Vector index=xxx out of range!
        """
        index = self._check_index_type_and_range_(index)
        # Add a new rectangle node and animation to SVG.
        rect_pos_x = self._cell_width*index+self._cell_margin*(index+1)
        rect_pos_y = self._cell_margin + self._cursor_manager.get_cursors_occupy()
        rect = (rect_pos_x, rect_pos_y, self._cell_width, self._cell_height)
        rid = self._svg.add_rect_element(rect, text=val)
        # Record the cells need to be move after the insert postion.
        for i in range(len(self._data), index, -1):
            rrid = self._index2rect[i-1]
            self._index2rect[i] = rrid
            if rrid in self._rect_move:
                self._rect_move[rrid] += 1
            else:
                self._rect_move[rrid] = 1
        self._index2rect[index] = rid
        self._cell_tcs[rid] = TraceColorStack()
        self._rect_appear.append(rid)
        self._data.insert(index, val)
    

    def append(self, val):
        """Append a new value into vector's tail.
        
        Args:
            val (printable): The value to appended into vector's tail.
        """
        index = len(self._data)
        rect_pos_x = self._cell_width*index+self._cell_margin*(index+1)
        rect_pos_y = self._cell_margin + self._cursor_manager.get_cursors_occupy()
        rect = (rect_pos_x, rect_pos_y, self._cell_width, self._cell_height)
        rid = self._svg.add_rect_element(rect, text=val)
        self._index2rect[index] = rid
        self._cell_tcs[rid] = TraceColorStack()
        self._rect_appear.append(rid)
        self._data.append(val)
    

    def pop(self, index=None):
        """Pop a value from vector. Pop vector's tail value as default. 
        
        Args:
            index (int/Cursor): The index position of value to pop out.

        Raises:
            RuntimeError: Index:xxx type is not int or Cursor.
            RuntimeError:  Vector index=xxx out of range!
        """
        if index == None:
            index = len(self._data) - 1
        else:
            index = self._check_index_type_and_range_(index)
        rid = self._index2rect[index]
        for i in range(index, len(self._data)-1):
            rrid = self._index2rect[i+1]
            self._index2rect[i] = rrid
            if rrid in self._rect_move:
                self._rect_move[rrid] -= 1
            else:
                self._rect_move[rrid] = -1
        self._index2rect.pop(len(self._data)-1)
        self._rect_disappear.append(rid)
        return self._data.pop(index)


    def clear(self):
        """Clear all the values in vector.
        """
        for i in range(len(self._data)):
            rid = self._index2rect[i]
            self._rect_disappear.append(rid)
        self._index2rect.clear()
        self._rect_move.clear()
        self._rect_appear.clear()
        self._data.clear()
    

    def swap(self, index1, index2):
        """Swap the two cells positon in Vector.
        Args:
            index1, index2 (int/Cursor): The two index positions to be swapped.
        
        Raises:
            RuntimeError: Index:xxx type is not int or Cursor.
            RuntimeError:  Vector index=xxx out of range!
        """
        index1 = self._check_index_type_and_range_(index1)
        index2 = self._check_index_type_and_range_(index2)
        rid1 = self._index2rect[index1]
        rid2 = self._index2rect[index2]
        self._index2rect[index1] = rid2
        self._index2rect[index2] = rid1
        if rid1 in self._rect_move.keys():
            self._rect_move[rid1] += index2 - index1
        else:
            self._rect_move[rid1] = index2 - index1
        if rid2 in self._rect_move.keys():
            self._rect_move[rid2] += index1 - index2
        else:
            self._rect_move[rid2] = index1 - index2
        temp_data = self._data[index2]
        self._data[index2] = self._data[index1]
        self._data[index1] = temp_data


    def mark(self, color, st, ed=None, hold=False):
        """Emphasize one cell in the Vector by mark it's background color.
            
        Args:
            color ((R,G,B)): The background color for the marked cell. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
            st, ed (int/Cursor): The mark range's index in Vector.
            hold (bool): Whether to keep the mark color in future animation frames.
        """
        st = self._check_index_type_and_range_(st)
        if ed is None:
            ed = st + 1
        if type(ed) is Cursor:
            ed = ed.index()
        for i in range(st, ed):
            if i < 0 or i >= len(self._data):
                i %= len(self._data)
            rid = self._index2rect[i]
            self._cell_tcs[rid].add(color)
            self._frame_trace.append((rid, color, hold))
    

    def removeMark(self, color):
        """Remove the mark color for cell(s).
        
        Args:
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        """
        for rid in self._index2rect.values():
            if self._cell_tcs[rid].remove(color):
                self._svg.update_rect_element(rid, fill=self._cell_tcs[rid].color())
    

    def _add_cursor_(self, cursor):
        """Create a new cursor to track the element's index.
        
        Args:
            cursor (Cursor): The cursor object to track.
        
        Returns:
            bool: Wheather add cursor successfully.
        """
        if type(cursor) != Cursor:
            return False
        if not self._cursor_manager.contains(cursor):
            self._cursor_manager.add_cursor(cursor)
            self._update_svg_size_(len(self._data))
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
        if self._cursor_manager.contains(cursor):
            self._cursor_manager.remove_cursor(cursor)
            self._update_svg_size_(len(self._data))
            self._update_rects_position_()
            self._update_subscripts_position_()
            return True
        return False


    def __getitem__(self, index):
        """
        Args:
            index (int/Cursor): The index position of the cell to be accessed.

        Raises:
            RuntimeError: Index:xxx type is not int or Cursor.
            RuntimeError:  Vector index=xxx out of range!
        """
        if type(index) is Cursor:
            self._add_cursor_(index)
        index = self._check_index_type_and_range_(index)
        return self._data[index]
    

    def __setitem__(self, index, val):
        """
        Args:
            index (int/Cursor): The index position of the cell to be updated.
            val (printable): New value for the cell.
        
        Raises:
            RuntimeError: Index:xxx type is not int or Cursor.
            RuntimeError:  Vector index=xxx out of range!
        """
        if type(index) is Cursor:
            self._add_cursor_(index)
        index = self._check_index_type_and_range_(index)
        rid = self._index2rect[index]
        label = val
        if val is None:
            label = ''
        self._svg.update_rect_element(rid, text=label)
        self._data[index] = val
    

    def __len__(self):
        """
        Returns:
            int: Length of Vector.
        """
        return len(self._data)
    
    def __iter__(self):
        self._next_iter = 0
        return self
    
    def __next__(self):
        if self._next_iter >= len(self._data):
            raise StopIteration
        else:
            res = self[self._next_iter]
            self._next_iter += 1
            return res
    

    def _repr_svg_(self):
        """
        Returns:
            str: The SVG representation of current Vector.
        """
        # Update the color of the cell tracker.
        all_data_num = len(self._data) + len(self._rect_disappear)
        self._update_svg_size_(all_data_num)
        for (rid, color) in self._frame_trace_old:
            if rid not in self._cell_tcs.keys():
                continue
            if (rid, color, False) not in self._frame_trace and (rid, color, True) not in self._frame_trace:
                self._cell_tcs[rid].remove(color)
            self._svg.update_rect_element(rid, fill=self._cell_tcs[rid].color())
        self._frame_trace_old.clear()
        for (rid, color, hold) in self._frame_trace:
            self._svg.update_rect_element(rid, fill=self._cell_tcs[rid].color())
            if not hold:
                self._frame_trace_old.append((rid, color))
        self._frame_trace.clear()
        # Add animations of the disappearance of cells.
        disappear_animate_end_time = self._delay*0.2
        for rid in self._rect_disappear:
            self._svg.add_animate_appear(rid, (0, disappear_animate_end_time), appear=False)
        has_move_animate = False
        move_animate_start_time = disappear_animate_end_time if len(self._rect_disappear) else 0
        move_animate_end_time = move_animate_start_time + (self._delay-move_animate_start_time)*0.6
        # Add animations of cells movement.
        if self._show_histogram > 0:
            self._update_bar_height_()
        for rid in self._rect_move.keys():
            if self._rect_move[rid] == 0:
                continue
            self._svg.add_animate_move(rid, (self._rect_move[rid]*(self._cell_width+self._cell_margin), 0),
                                        (move_animate_start_time, move_animate_end_time), bessel=False)
            has_move_animate = True
        # Add animations of the appearance of cells.
        appear_animate_start_time = move_animate_end_time if has_move_animate else move_animate_start_time
        for rid in self._rect_appear:
            self._svg.add_animate_appear(rid, (appear_animate_start_time, self._delay))
        # Update subscript index of vector cells.
        if self._show_index:
            if len(self._index2text) > len(self._data):
                for i in range(len(self._data), len(self._index2text)):
                    self._svg.delete_element(self._index2text[i])
                    self._index2text.pop(i)
            elif len(self._index2text) < len(self._data):
                self._create_new_subscripts_(len(self._index2text), len(self._data))
        self._rect_move.clear()
        self._cursor_manager.refresh_cursors_animation(all_data_num, (0, self._delay))
        res = self._svg._repr_svg_()
        # Clear the animation effect, update the SVG content, and prepare for the next frame.
        self._svg.clear_animates()
        if self._show_histogram > 0:
            self._update_bar_height_()
        else:
            for i in range(len(self._data)):
                rect_pos_x = self._cell_width*i + self._cell_margin*(i+1)
                rect_pos_y = self._cell_margin + self._cursor_manager.get_cursors_occupy()
                rect = (rect_pos_x, rect_pos_y, self._cell_width, self._cell_height)
                rid = self._index2rect[i]
                self._svg.update_rect_element(rid, rect=rect)
        for rid in self._rect_disappear:
            self._svg.delete_element(rid)
            self._cell_tcs.pop(rid)
        self._rect_disappear.clear()
        for rid in self._rect_appear:
            self._svg.update_rect_element(rid, opacity=True)
        self._rect_appear.clear()
        self._cursor_manager.update_cursors_position()
        return res
    

    def _update_bar_height_(self):
        """Update the height of each column in the histogram.
        """
        # Adjust the ratio and baseline position according to the value numbers range.
        mmax_data, max_data = 0, 0
        for num in self._data:
            if num is None:
                continue
            num = float(num)
            if num < 0:
                mmax_data = min(mmax_data, num)
            else:
                max_data = max(max_data, num)
        if (max_data - mmax_data) < 0.0001:
            ratio = 0
        else:
            useful_height = self._cell_height - 2*self._cell_margin
            if self._show_index:
                useful_height -= self._label_font_size
            ratio = useful_height/(max_data-mmax_data)
        baseline = max_data*ratio + self._cell_margin + self._cursor_manager.get_cursors_occupy()
        # Update the position coordinates of cells.
        for i in range(len(self._data)):
            if self._data[i] is None:
                num = 0
            else:
                num = float(self._data[i])
            rid = self._index2rect[i]
            x = self._cell_width*i + self._cell_margin*(i+1)
            if rid in self._rect_move.keys():
                x -= self._rect_move[rid] * (self._cell_width+self._cell_margin)
            height = ratio*num
            if num < 0:
                y = baseline
            else:
                y = baseline - height
            if num - int(num) > 0.001:
                num = '{:.2f}'.format(num)
            else:
                num = '{:.0f}'.format(num)
            if self._data[i] is None:
                num = None
            self._svg.update_rect_element(rid, rect=(x, y, self._cell_width, abs(height)), text=num)


    def _update_svg_size_(self, data_num):
        if self._show_histogram:
            self._svg_height = self._cell_height
        else:
            self._svg_height = self._cell_height + 2*self._cell_margin
            if self._show_index:
                self._svg_height += self._label_font_size
        self._svg_height += self._cursor_manager.get_cursors_occupy()
        self._svg_width = data_num*self._cell_width+(data_num+1)*self._cell_margin
        self._svg.update_svg_size(self._svg_width, self._svg_height)

    def _update_rects_position_(self):
        for i, gid in self._index2rect.items():
            rect_pos_x = self._cell_width*i+self._cell_margin*(i+1)
            rect_pos_y = self._cell_margin + self._cursor_manager.get_cursors_occupy()
            rect = (rect_pos_x, rect_pos_y, self._cell_width, self._cell_height)
            if self._svg:
                self._svg.update_rect_element(gid, rect)

    def _create_new_subscripts_(self, st, ed):
        for i in range(st, ed):
            pos_x = self._cell_width*(i+0.5)+self._cell_margin*(i+1)-self._label_font_size*len(str(i))*0.25
            pos_y = self._svg_height - self._cell_margin
            tid = self._svg.add_text_element((pos_x, pos_y), i, font_size=self._label_font_size)
            self._index2text[i] = tid

    def _update_subscripts_position_(self):
        for i, gid in self._index2text.items():
            gid = self._index2text[i]
            pos_x = self._cell_width*(i+0.5)+self._cell_margin*(i+1)-self._label_font_size*len(str(i))*0.25
            pos_y = self._svg_height - self._cell_margin
            self._svg.update_text_element(gid, (pos_x, pos_y))

    def _check_index_type_and_range_(self, index):
        res = None
        if type(index) is int:
            res = index
        elif type(index) is Cursor:
            res = index.index()
        else:
            raise RuntimeError('Index:{} type is not int or Cursor.'.format(index))
        if index < 0 or index >= len(self._data):
            raise RuntimeError('Vector index={} out of range!'.format(index))
        return res
