#!/usr/bin/env python3


"""Define the cursor related classes.

A cusor is a arrow show in Vector or Table's SVG display.
The cusor represent the index of element in Vector or Table.

Author: zjl9959@gmail.com

License: GPLv3

"""

# The alternative cursor colors list.
kcursor_colors = (
    (128, 128, 128),    # gray
    (0, 255, 0),        # lime
    (255, 215, 0),      # gold
    (255, 192, 203),    # pink
    (218, 112, 214),    # orchild
    (255, 99, 71),      # tomato
    (245, 222, 179),    # wheat
    (192, 192, 192),    # silver
)

class Cursor:
    """Random access cursor class.

    Provide common mathematics operators like +,-,*,//,==,!=,>,<.
    The lhs is this cursor object and the rhs is a integer number or a cursor object.

    """
    def __init__(self, table, id, offset=0):
        self._table = table             # This cursor's related Vector or Table object.
        self._id = id                   # The unique id of the cursor in it's related Vector or Table.
        self._index = offset            # The current index of cursor (0 <= index < max_val).

    def _on_cursor_changed(self, new_index):
        if self._table:
            self._table._on_cursor_changed(self._id, new_index)

    # Mathmatics operators.
    def __add__(self, other):
        new_index = self._index + _get_rhs_index(other)
        self._on_cursor_changed(new_index)
        return Cursor(self._table, self._id, new_index)

    def __sub__(self, other):
        new_index = self._index - _get_rhs_index(other)
        self._on_cursor_changed(new_index)
        return Cursor(self._table, self._id, new_index)

    def __mul__(self, other):
        new_index = self._index * _get_rhs_index(other)
        self._on_cursor_changed(new_index)
        return Cursor(self._table, self._id, new_index)

    def __pow__(self, other):
        new_index = self._index ** _get_rhs_index(other)
        self._on_cursor_changed(new_index)
        return Cursor(self._table, self._id, new_index)

    def __floordiv__(self, other):
        new_index = self._index // _get_rhs_index(other)
        self._on_cursor_changed(new_index)
        return Cursor(self._table, self._id, new_index)

    def __mod__(self, other):
        new_index = self._index % _get_rhs_index(other)
        self._on_cursor_changed(new_index)
        return Cursor(self._table, self._id, new_index)

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
    if type(rhs) is int:
        return rhs
    elif type(rhs) is Cursor:
        return rhs._index
    else:
        return int(rhs)     # Try to convert unkonw type into int.


class _CursorManager:
    def __init__(self, cell_size, svg, dir, anchor):
        self._next_cursor_id = 0
        self._cell_size = cell_size
        self._svg = svg                         # The SVGTable object in Vector or Table.
        self._dir = dir                         # The direction of the cursor's arrow (U:up, D:down, L:left, R:right).
        self._anchor = anchor                   # Cursor's anchor (pos_x:float, pos_y:float).
        self._cursor_height = 0.5 * self._cell_size     # The total height of a cursor (arrow and label).
        self._cursor_offset = 0.1 * self._cell_size     # Cursor_offset = cursor_id*self._cursor_offset.
        self._cursors_info = dict()             # key:cursor_id; value:cursor_gid in SVG.
        self._old_cursors_index = dict()        # key:cursor_id; value:cursor_index.
        self._new_cursors_index = dict()        # key:cursor_id; value:cursor_index.

    def new_cursor(self, table, name, offset):
        """Create a new cursor object and track it.
        """
        cursor_id = self._next_cursor_id
        self._next_cursor_id += 1
        # Calculate cursor's position information according to it's index.
        offset_sign = 1 if cursor_id % 2 else -1
        cursor_offset = cursor_id*self._cursor_offset*offset_sign
        cursor_pos_x = self._anchor[0] + offset*self._cell_size
        cursor_pos_y = self._anchor[1]
        if self._dir == 'L' or self._dir == 'R':
            cursor_pos_x = self._anchor[0]
            cursor_pos_y = self._anchor[1] + offset*self._cell_size
        cursor_height = self._cursor_height * (cursor_id + 1)
        cursor_pos = (cursor_pos_x, cursor_pos_y, cursor_offset, self._cell_size, cursor_height)
        cursor_color = kcursor_colors[cursor_id % len(kcursor_colors)]
        cursor_node = self._svg.add_cursor_element(cursor_pos, cursor_color, name, self._dir)
        self._cursors_info[cursor_id] = cursor_node
        self._old_cursors_index[cursor_id] = offset
        return Cursor(table, cursor_id, offset)

    def remove_cursor(self, cursor_id):
        """Untrack the specific cursor from this cursor manager.
        """
        if cursor_id in self._cursors_info:
            gid = self._cursors_info[cursor_id]
            self._svg.remove_element(gid)
            self._cursors_info.pop(cursor_id)
        if cursor_id in self._old_cursors_index:
            self._old_cursors_index.pop(cursor_id)
        if cursor_id in self._new_cursors_index:
            self._new_cursors_index.pop(cursor_id)

    def get_cursors_margin(self):
        return len(self._cursors_info) * self._cursor_height

    def on_update_cursor(self, cursor_id, new_index):
        self._new_cursors_index[cursor_id] = new_index

    def refresh_cursors(self, max_index, time, strict=True):
        """Refresh all the animations in cursors node.
        
        Args:
            max_index (int): Used to check the max value of the cursor.
            time (tuple(float, float)): (begin, end) The begin and end time of cursor move animation.
            strict (boolean): Wheather the index value of cursor can be rounded by max_index.
        """
        for cursor_id in self._cursors_info.keys():
            if cursor_id not in self._new_cursors_index:
                continue
            move_delt_x, move_delt_y = 0, 0
            old_index = self._old_cursors_index[cursor_id]
            if old_index < 0 or old_index >= max_index:
                if not strict:
                    old_index %= max_index
                else:
                    # The cursor should move out of range if in strict mode.
                    old_index = -1 if old_index < 0 else max_index
            new_index = self._new_cursors_index[cursor_id]
            if new_index < 0 or new_index >= max_index:
                if not strict:
                    new_index %= max_index
                else:
                    new_index = -1 if new_index < 0 else max_index
            if self._dir == 'L' or self._dir == 'R':
                move_delt_y = (new_index - old_index)*self._cell_size
            else:
                move_delt_x = (new_index - old_index)*self._cell_size
            cursor_gid = self._cursors_info[cursor_id]
            self._svg.add_animate_move(cursor_gid, (move_delt_x, move_delt_y), time, False)
        # Update the cached data.
        for cursor_id in self._new_cursors_index:
            self._old_cursors_index = self._new_cursors_index[cursor_id]
