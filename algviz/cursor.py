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
    """A cursor is a display object to show the current index of Vector or Table(row/column).

    A cursor object must be created from it's related Vector/Table object.
    Otherwise the disaplyed SVG can not track it's index change.
    You can access an element in it's related Vector/Table object.
    The index in cursor's should be an integer number.
    
    For example:
        i = vector.new_cursor('i')  # Create a cursor point to vector object.
        vector[i] = 3               # Set the cursor's index(0) element to 3 in vector.
    
    This class provide mathematics operations like: +, -, *, //.
    So you can change the cursor's index by do these operators on itself.
    But you can not assgin a integer number into a cursor directly.
    And you should only assign the result of mathematics operations into the cursor itself.
    Instead, use update method in cursor to update it's index.
    
    For example:
        i = vector.new_cursor('i')  # The index in cursor i is 0.
        i = i + 1                   # The index in cursor i is 1.
        i.update(10)                # The index in cursor i is 10.

    This class provide compare operations like: >, <, >=, <=, ==, !=.
    So you can do these operations between a cursor and an integer number or other cursor.

    For example:
        i = vector.new_cursor('i', 3)   # The index in cursor i is 3.
        j = vector.new_cursor('j', 5)   # The index in cursor j is 5.
        i < 10                          # True: 3 < 10 is true.
        i > j                           # False: 3 > 5 is false.
    """

    def __init__(self, manager, id, offset=0):
        self._manager = manager         # This cursor's related manager.
        self._id = id                   # The unique id of the cursor in it's related Vector or Table.
        self._index = offset            # The current index of cursor.

    def _on_cursor_updated_(self, new_index):
        if self._manager:
            self._manager.on_cursor_updated(self._id, new_index)

    def index(self):
        """
        Returns:
            int: The cursor's current index value.
        """
        return self._index

    def update(self, new_index):
        """Update the cursor's index manually.

        Args:
            new_index (int): The new index assigned to the cursor.
        """
        self._index = _get_rhs_index(new_index)
        self._on_cursor_updated_(self._index)

    # Mathmatics operators.
    def __add__(self, other):
        new_index = self._index + _get_rhs_index(other)
        self._on_cursor_updated_(new_index)
        return Cursor(self._manager, self._id, new_index)

    def __sub__(self, other):
        new_index = self._index - _get_rhs_index(other)
        self._on_cursor_updated_(new_index)
        return Cursor(self._manager, self._id, new_index)

    def __mul__(self, other):
        new_index = self._index * _get_rhs_index(other)
        self._on_cursor_updated_(new_index)
        return Cursor(self._manager, self._id, new_index)

    def __pow__(self, other):
        new_index = self._index ** _get_rhs_index(other)
        self._on_cursor_updated_(new_index)
        return Cursor(self._manager, self._id, new_index)

    def __floordiv__(self, other):
        new_index = self._index // _get_rhs_index(other)
        self._on_cursor_updated_(new_index)
        return Cursor(self._manager, self._id, new_index)

    def __mod__(self, other):
        new_index = self._index % _get_rhs_index(other)
        self._on_cursor_updated_(new_index)
        return Cursor(self._manager, self._id, new_index)

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
    def __init__(self, cell_size, svg, dir, margins=(0, 0)):
        self._next_cursor_id = 0
        self._cell_size = cell_size
        self._svg_margin = margins[0]            # The margin between cell and SVG.
        self._cell_margin = margins[1]           # The margin between cells.
        self._svg = svg                         # The SVGTable object in Vector or Table.
        self._dir = dir                         # The direction of the cursor's arrow (U:up, D:down, L:left, R:right).
        # The total height of a cursor (arrow and label).
        self._cursor_height = min(20, 0.4 * self._cell_size)
        # Cursor_offset = cursor_id*self._cursor_offset.
        self._cursor_offset = 1
        self._cursors_info = dict()             # key:cursor_id; value:cursor_gid in SVG.
        self._old_cursors_index = dict()        # key:cursor_id; value:cursor_index.
        self._new_cursors_index = dict()        # key:cursor_id; value:cursor_index.
        self._cursor_moves = dict()             # Cache the cursor move since last frame. key:cursor_id; value:(cursor_move_delt_x, cursor_move_delt_y).

    def new_cursor(self, name, offset):
        """Create a new cursor object and track it.
        """
        # Update old cursor's position.
        for gid in self._cursors_info.values():
            if self._dir == 'R':
                self._svg.update_cursor_element(gid, (self._cursor_height, 0))
            else:
                self._svg.update_cursor_element(gid, (0, self._cursor_height))
        cursor_id = self._next_cursor_id
        self._next_cursor_id += 1
        # Calculate cursor's position information according to it's index.
        offset_sign = 1 if cursor_id % 2 else -1
        cursor_offset = cursor_id*self._cursor_offset*offset_sign
        cursor_pos_x = self._svg_margin + offset*(self._cell_size + self._cell_margin) + self._cell_size*0.5
        cursor_pos_y = self.get_cursors_occupy()
        if self._dir == 'R':
            cursor_pos_x = self.get_cursors_occupy()
            cursor_pos_y = self._svg_margin + offset*(self._cell_size + self._cell_margin) + self._cell_size*0.5
        cursor_height = self._cursor_height * (cursor_id + 1)
        cursor_pos = (cursor_pos_x, cursor_pos_y, cursor_offset, self._cell_size, cursor_height)
        cursor_color = kcursor_colors[cursor_id % len(kcursor_colors)]
        cursor_node = self._svg.add_cursor_element(cursor_pos, cursor_color, name, self._dir)
        self._cursors_info[cursor_id] = cursor_node
        self._old_cursors_index[cursor_id] = offset
        return Cursor(self, cursor_id, offset)

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

    def get_cursors_occupy(self):
        """
        Returns:
            float: The sum of all the cursors height.
        """
        return self._next_cursor_id * self._cursor_height + self._svg_margin

    def on_cursor_updated(self, cursor_id, new_index):
        """Called when cursor's index changed.
        """
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
            if new_index < 0 or new_index >= max_index:
                new_index = -1 if new_index < 0 else max_index
            if self._dir == 'R':
                move_delt_y = (new_index - old_index) * (self._cell_size + self._cell_margin)
            else:
                move_delt_x = (new_index - old_index) * (self._cell_size + self._cell_margin)
            cursor_gid = self._cursors_info[cursor_id]
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
            cursor_gid = self._cursors_info[cursor_id]
            self._svg.update_cursor_element(cursor_gid, cursor_move)
