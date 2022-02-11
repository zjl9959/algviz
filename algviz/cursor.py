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

    This class provide compare operations like: >, <, >=, <=, ==, !=.
    So you can do these operations between a cursor and an integer number or other cursor.

    For example:
        i = vector.new_cursor('i', 3)   # The index in cursor i is 3.

        j = vector.new_cursor('j', 5)   # The index in cursor j is 5.

        i < 10                          # True: 3 < 10 is true.
        
        i > j                           # False: 3 > 5 is false.
    """

    def __init__(self, manager, id, index=0):
        self._manager = manager         # This cursor's related manager.
        self._id = id                   # The unique id of the cursor in it's related Vector or Table.
        self._index = index             # The current index of cursor.

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
    def inc(self, other=1):
        """Increase the index value in cursor.
        
        Args:
            other: The increment value, can be int or Cursor.

        Returns:
            int: The new index value in cursor.
        """
        self._index += _get_rhs_index(other)
        self._on_cursor_updated_(self._index)
        return self._index

    def dec(self, other=1):
        """Decrease the index value in cursor.
        
        Args:
            other: The decrement value, can be int or Cursor.

        Returns:
            int: The new index value in cursor.
        """
        self._index -= _get_rhs_index(other)
        self._on_cursor_updated_(self._index)
        return self._index

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
    def __init__(self, cell_size, svg, dir, svg_margin=(0, 0), cell_margin=0):
        """
        Args:
            cell_size (float): The rectangle cell size in SVG.
            svg (SvgTable): The SvgTable object to add cursors on.
            dir (str): The direction of cursors. (Support 'D':down, 'R':right)
            svg_margin (float, float): The margin between SVG side and cursor's start.
            cell_margin (float): The margin between rectangle cells.
        """
        self._next_cursor_id = 0
        self._cell_size = cell_size
        self._svg_margin = svg_margin           # The margin between cell and SVG.
        self._cell_margin = cell_margin         # The margin between cells.
        self._svg = svg                         # The SVGTable object in Vector or Table.
        self._dir = dir                         # The direction of the cursor's arrow (U:up, D:down, L:left, R:right).
        # The total height of a cursor (arrow and label).
        self._cursor_height = min(20, 0.4 * self._cell_size)
        self._cursor_margin = 3                 # The margin between cursor manager and SVG.
        # Cursor_offset = cursor_id*self._cursor_offset.
        self._cursor_offset = 2
        self._cursors_info = dict()             # key:cursor_id; value:(cursor_gid, cursor_color, cursor_name) in SVG.
        self._cursors_id_list = list()          # Keep the sequence of cursors id by create time.
        self._old_cursors_index = dict()        # key:cursor_id; value:cursor_index.
        self._new_cursors_index = dict()        # key:cursor_id; value:cursor_index.
        self._cursor_moves = dict()             # Cache the cursor move since last frame. key:cursor_id; value:(cursor_move_delt_x, cursor_move_delt_y).

    def new_cursor(self, name, index):
        """Create a new cursor object and track it.
        """
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
        cursor_color = kcursor_colors[cursor_seq % len(kcursor_colors)]
        cursor_node = self._svg.add_cursor_element(cursor_pos, cursor_color, name, self._dir)
        # Record the cursor's position and offset information.
        self._cursors_id_list.append(cursor_id)
        self._cursors_info[cursor_id] = (cursor_node, cursor_color, name)
        self._old_cursors_index[cursor_id] = index
        return Cursor(self, cursor_id, index)

    def remove_cursor(self, cursor_id):
        """Untrack the specific cursor from this cursor manager.
        """
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
        for i in range(cursor_seq+1, len(self._cursors_id_list)):
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
            cursor_pos = self._calculate_cursor_position_(i-1, cursor_index)
            cursor_pos_correct = (len(self._cursors_id_list)-i-1)*self._cursor_height
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
            if self._dir == 'R':
                move_delt_y = (new_index - old_index) * (self._cell_size + self._cell_margin)
            else:
                move_delt_x = (new_index - old_index) * (self._cell_size + self._cell_margin)
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
        cursor_offset = ((cursor_seq+1)//2)*self._cursor_offset*offset_sign
        cursor_pos_x, cursor_pos_y = 0, 0
        if self._dir == 'R':
            cursor_pos_x = self._cursor_height * (cursor_seq + 1) + self._cursor_margin
            cursor_pos_y = self._svg_margin[1] + index*(self._cell_size + self._cell_margin) + self._cell_size*0.5
        else:
            cursor_pos_x = self._svg_margin[0] + index*(self._cell_size + self._cell_margin) + self._cell_size*0.5
            cursor_pos_y = self._cursor_height * (cursor_seq + 1) + self._cursor_margin
        cursor_height = self._cursor_height * (cursor_seq + 1)
        return [cursor_pos_x, cursor_pos_y, cursor_offset, self._cell_size, cursor_height]
