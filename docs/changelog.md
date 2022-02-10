# Changelog

## algviz 0.1.1

+ Add cursor support for Vector and Table.
    + Add [Cursor]() class to display the cursor position change in Vector and Table.
    + Add interface [new_cursor](), [remove_cursor]() in Vector.
    + Add interface [new_row_cursor](), [new_col_cursor]() in Table.
+ Add [reshape]() interface in Table.
+ Compress SVG size for tables with very many cells.
+ Changed the index range check rule for [insert](), [pop](), [swap]() interfaces in Vector, raise exception when index out of range.

## algviz 0.1.0

This is the first public release of algviz. Support animation generation for vector, table, linked list, tree and graph data structures in jupyter notebook.
