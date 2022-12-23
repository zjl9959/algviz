#!/usr/bin/env python3


"""Define the cursor related classes.

A cursor is an arrow shown in Vector or Table's SVG display.
The cursor represents the index of the element in Vector or Table.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.utility import AlgvizTypeError


# The alternative cursor colors list.
kcursor_colors = (
    (40, 116, 166),
    (147, 81, 22),
    (25, 111, 61),
    (203, 67, 53),
    (28, 40, 51),
    (99, 57, 116)
)


class Cursor:
    """A cursor is a display object to show the current index of Vector or Table(row/column).

    A cursor object should be created from Visualizer.create_cursor
    or Visualizer.cursorRange interfaces. After that,
    you can access the element in any Vector/Table object with
    the created cursor just like an integer index.
    The index in the cursor should be an integer number.

    Assignment operation: <<

    Mathmatics operations:
        No side effect, returns a int number: +, -, *, //, %

        Changes the cursor's index and returns itself: +=, -=, *=, //=, %=

    Compare operations: >, <, >=, <=, ==, !=

    The right-hand value of those operations above can be a cursor or an integer number.


    For example:
        i = viz.createCursor(3, 'i')   # The index in cursor i is 3.

        j = viz.createCursor(5, 'j')   # The index in cursor j is 5.

        i += j                          # The index in cursor i change from 3 into 8(3+5).

        j << i - 1                      # The index in cursor j change from 5 into 7(8-1).

        i > j                           # True: 8 > 7 is true.
    """

    def __init__(self, name, index, id):
        self._managers = list()         # This cursor's related managers.
        self._name = name               # The cursor's display name.
        self._index = index             # The current index of cursor.
        color = kcursor_colors[id % len(kcursor_colors)]
        self._color = color             # The display color of cursor.

    def _add_manager_(self, mgr):
        if mgr not in self._managers:
            self._managers.append(mgr)

    def _on_cursor_updated_(self, new_index):
        for mgr in self._managers:
            mgr.on_cursor_updated(self, new_index)

    def index(self):
        """
        Returns:
            int: The cursor's current index value.
        """
        return self._index

    def name(self):
        """
        Returns:
            str: Cursor display name.
        """
        return self._name

    # Index assignment operator.
    def __lshift__(self, other):
        self._index = _get_rhs_index(other)
        self._on_cursor_updated_(self._index)
        return self

    # Mathmatics operators.
    def __add__(self, other):
        rhs = _get_rhs_index(other)
        return self._index + rhs

    def __sub__(self, other):
        rhs = _get_rhs_index(other)
        return self._index - rhs

    def __mul__(self, other):
        rhs = _get_rhs_index(other)
        return self._index * rhs

    def __floordiv__(self, other):
        rhs = _get_rhs_index(other)
        return self._index // rhs

    def __mod__(self, other):
        rhs = _get_rhs_index(other)
        return self._index % rhs

    def __imul__(self, other):
        self._index *= _get_rhs_index(other)
        self._on_cursor_updated_(self._index)
        return self

    def __ifloordiv__(self, other):
        self._index //= _get_rhs_index(other)
        self._on_cursor_updated_(self._index)
        return self

    def __iadd__(self, other):
        self._index += _get_rhs_index(other)
        self._on_cursor_updated_(self._index)
        return self

    def __isub__(self, other):
        self._index -= _get_rhs_index(other)
        self._on_cursor_updated_(self._index)
        return self

    def __imod__(self, other):
        self._index %= _get_rhs_index(other)
        self._on_cursor_updated_(self._index)
        return self

    # Compare operators.
    def __lt__(self, other):
        return self._index < _get_rhs_index(other)

    def __le__(self, other):
        return self._index <= _get_rhs_index(other)

    def __eq__(self, other):
        return self._index == _get_rhs_index(other)

    def __ne__(self, other):
        return self._index != _get_rhs_index(other)

    def __gt__(self, other):
        return self._index > _get_rhs_index(other)

    def __ge__(self, other):
        return self._index >= _get_rhs_index(other)


def _get_rhs_index(rhs):
    if rhs is None:
        return None
    elif type(rhs) is int:
        return rhs
    elif type(rhs) is Cursor:
        return rhs._index
    else:
        raise AlgvizTypeError(rhs)


class _CursorRange:
    def __init__(self, id, name, start, end, step):
        self._end = end
        self._step = step
        self._next_index = start
        self._cursor = Cursor(name, start, id)

    def __iter__(self):
        return self

    def __next__(self):
        if self._next_index == self._end:
            raise StopIteration
        else:
            self._cursor << self._next_index
            self._next_index += self._step
            return self._cursor


class _CursorManager:
    def __init__(self, cell_size, svg, dir, svg_margin=(0, 0), cell_margin=0):
        """
        Args:
            cell_size (float, float): The rectangle cell size in SVG.
            svg (SvgTable): The SvgTable object to add cursors on.
            dir (str): The direction of cursors. (Support 'D':down, 'R':right)
            svg_margin (float, float): The margin between SVG side and cursor's start.
            cell_margin (float): The margin between rectangle cells.
        """
        self._next_cursor_id = 0
        self._cell_width = cell_size[0]
        self._cell_height = cell_size[1]
        self._svg_margin = svg_margin           # The margin between cell and SVG.
        self._cell_margin = cell_margin         # The margin between cells.
        self._svg = svg                         # The SVGTable object in Vector or Table.
        self._dir = dir                         # The direction of the cursor's arrow (U:up, D:down, L:left, R:right).
        # The total height of a cursor (arrow and label).
        if self._dir == 'U' or self._dir == 'D':
            self._cursor_height = min(20, 0.4 * self._cell_height)
        else:
            self._cursor_height = min(20, 0.4 * self._cell_width)
        self._cursor_margin = 3                 # The margin between cursor manager and SVG.
        self._cursor2id = dict()                # Map the cursor object id into the unique cursor id in this cursor manager.
        # Cursor_offset = cursor_id*self._cursor_offset.
        self._cursor_offset = 2
        self._cursors_info = dict()             # key:cursor_id; value:(cursor_gid, cursor_color, cursor_name) in SVG.
        self._cursors_id_list = list()          # Keep the sequence of cursors id by create time.
        self._old_cursors_index = dict()        # key:cursor_id; value:cursor_index.
        self._new_cursors_index = dict()        # key:cursor_id; value:cursor_index.
        self._cursor_moves = dict()             # Cache the cursor move since last frame. key:cursor_id; value:(cursor_move_delt_x, cursor_move_delt_y).

    def contains(self, cursor):
        """Check if the cursor was tracked by this manager.
        """
        return id(cursor) in self._cursor2id

    def add_cursor(self, cursor):
        """Create a new cursor object and track it.
        """
        if self.contains(cursor):
            return
        name = cursor.name()
        index = cursor.index()
        # Update old cursor's position.
        for cid in self._cursors_id_list:
            gid = self._cursors_info[cid][0]
            if self._dir == 'R':
                self._svg.update_cursor_element(gid, (self._cursor_height, 0))
            else:
                self._svg.update_cursor_element(gid, (0, self._cursor_height))
        # Create a new cursor and setup it's position and color.
        cursor_id = self._next_cursor_id
        self._next_cursor_id += 1
        cursor_seq = len(self._cursors_id_list)
        cursor_pos = self._calculate_cursor_position_(cursor_seq, index)
        cursor_color = cursor._color
        cursor_node = self._svg.add_cursor_element(cursor_pos, cursor_color, name, self._dir)
        # Record the cursor's position and offset information.
        self._cursors_id_list.append(cursor_id)
        self._cursors_info[cursor_id] = (cursor_node, cursor_color, name)
        self._old_cursors_index[cursor_id] = index
        # Update the cache and cursor.
        self._cursor2id[id(cursor)] = cursor_id
        cursor._add_manager_(self)

    def remove_cursor(self, cursor):
        """Untrack the specific cursor from this cursor manager.
        """
        if id(cursor) not in self._cursor2id:
            return
        cursor_id = self._cursor2id[id(cursor)]
        if cursor_id not in self._cursors_id_list:
            return
        cursor_seq = self._cursors_id_list.index(cursor_id)
        # Update the cursors who's sequence ahead of the cursor to be removed.
        for i in range(cursor_seq):
            cid = self._cursors_id_list[i]
            if cid not in self._cursors_info:
                print('[WARNING] _CursorManager.remove_cursor cursor {} not found in cursors_info.'.format(cid))
                continue
            gid = self._cursors_info[cid][0]
            if self._dir == 'R':
                self._svg.update_cursor_element(gid, (-self._cursor_height, 0))
            else:
                self._svg.update_cursor_element(gid, (0, -self._cursor_height))
        # Update the cursors who's sequence behind the cursor to be removed.
        for i in range(cursor_seq + 1, len(self._cursors_id_list)):
            cid = self._cursors_id_list[i]
            if cid not in self._cursors_info:
                print('[WARNING] _CursorManager.remove_cursor cursor {} not found in cursors_info.'.format(cid))
                continue
            cursor_info = self._cursors_info[cid]
            # The SVGTable class don't provide a update cursor's information interface,
            # so we need to delete the cursor node in SVG and create a new one with updated information.
            self._svg.delete_element(cursor_info[0])
            cursor_index = 0
            if cid in self._old_cursors_index:
                cursor_index = self._old_cursors_index[cid]
            cursor_pos = self._calculate_cursor_position_(i - 1, cursor_index)
            cursor_pos_correct = (len(self._cursors_id_list) - i - 1) * self._cursor_height
            if self._dir == 'R':
                cursor_pos[0] += cursor_pos_correct
            else:
                cursor_pos[1] += cursor_pos_correct
            cursor_node = self._svg.add_cursor_element(cursor_pos, cursor_info[1], cursor_info[2], self._dir)
            self._cursors_info[cid] = (cursor_node, cursor_info[1], cursor_info[2])
        # Remove the cursor in SVG.
        if cursor_id in self._cursors_info:
            gid = self._cursors_info[cursor_id][0]
            self._svg.delete_element(gid)
        if cursor_id in self._old_cursors_index:
            self._old_cursors_index.pop(cursor_id)
        if cursor_id in self._new_cursors_index:
            self._new_cursors_index.pop(cursor_id)
        self._cursors_id_list.remove(cursor_id)

    def get_cursors_occupy(self):
        """
        Returns:
            float: The sum of all the cursors height.
        """
        return len(self._cursors_id_list) * self._cursor_height + self._cursor_margin

    def on_cursor_updated(self, cursor, new_index):
        """Called when cursor's index changed.
        """
        if not self.contains(cursor):
            return
        cursor_id = self._cursor2id[id(cursor)]
        self._new_cursors_index[cursor_id] = new_index

    def refresh_cursors_animation(self, max_index, time):
        """Refresh all the animations in cursors node.

        Args:
            max_index (int): Used to check the max value of the cursor.
            time (tuple(float, float)): (begin, end) The begin and end time of cursor move animation.
        """
        self._cursor_moves.clear()
        for cursor_id in self._new_cursors_index.keys():
            move_delt_x, move_delt_y = 0, 0
            old_index = self._old_cursors_index[cursor_id]
            if old_index < 0 or old_index >= max_index:
                # The cursor should move out of range if in strict mode.
                old_index = -1 if old_index < 0 else max_index
            new_index = self._new_cursors_index[cursor_id]
            if self._dir == 'R':
                move_delt_y = (new_index - old_index) * (self._cell_height + self._cell_margin)
            else:
                move_delt_x = (new_index - old_index) * (self._cell_width + self._cell_margin)
            cursor_gid = self._cursors_info[cursor_id][0]
            self._svg.add_animate_move(cursor_gid, (move_delt_x, move_delt_y), time, False)
            self._cursor_moves[cursor_id] = (move_delt_x, move_delt_y)
        # Update the cached data.
        for cursor_id in self._new_cursors_index:
            self._old_cursors_index[cursor_id] = self._new_cursors_index[cursor_id]

    def update_cursors_position(self):
        """Update all the cursors position to the latest state.
        """
        for cursor_id in self._new_cursors_index.keys():
            cursor_move = self._cursor_moves[cursor_id]
            cursor_gid = self._cursors_info[cursor_id][0]
            self._svg.update_cursor_element(cursor_gid, cursor_move)

    def on_svg_margin_changed(self, svg_margin):
        """Called when svg margin changed.
        Args:
            svg_margin (float, float): The margin between SVG side and cursor's start.
        """
        delt_svg_margin = (svg_margin[0] - self._svg_margin[0], svg_margin[1] - self._svg_margin[1])
        self._svg_margin = svg_margin
        for cursor_id in self._cursors_id_list:
            cursor_gid = self._cursors_info[cursor_id][0]
            self._svg.update_cursor_element(cursor_gid, delt_svg_margin)

    def _calculate_cursor_position_(self, cursor_seq, index):
        offset_sign = 1 if cursor_seq % 2 else -1
        cursor_offset = ((cursor_seq + 1) // 2) * self._cursor_offset * offset_sign
        cursor_pos_x, cursor_pos_y = 0, 0
        if self._dir == 'R':
            cursor_pos_x = self._cursor_height * (cursor_seq + 1) + self._cursor_margin
            cursor_pos_y = self._svg_margin[1] + index * (self._cell_height + self._cell_margin) + self._cell_height * 0.5
            cursor_width = self._cell_height
        else:
            cursor_pos_x = self._svg_margin[0] + index * (self._cell_width + self._cell_margin) + self._cell_width * 0.5
            cursor_pos_y = self._cursor_height * (cursor_seq + 1) + self._cursor_margin
            cursor_width = self._cell_width
        cursor_height = self._cursor_height * (cursor_seq + 1)
        return [cursor_pos_x, cursor_pos_y, cursor_offset, cursor_width, cursor_height]
