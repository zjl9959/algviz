# Changelog

## algviz 0.1.2

+ SVG animation visual effection optimization: divide the animation of disappearing, moving and appearing into different animation sequences.
+ Add new exceptions: [AlgvizParamError](https://algviz.readthedocs.io/en/latest/api.html#algviz.AlgvizParamError), [AlgvizRuntimeError](https://algviz.readthedocs.io/en/latest/api.html#algviz.AlgvizRuntimeError), [AlgvizFatalError](https://algviz.readthedocs.io/en/latest/api.html#algviz.AlgvizFatalError).

## algviz 0.1.1

+ Add cursor support for Vector and Table.

    ![cursor_example](https://cdn.jsdelivr.net/gh/zjl9959/algviz@main/docs/animation_images/vector_cursor_example.svg)

    + Add [Cursor](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.cursor.Cursor) class to display the cursor position change in Vector and Table.
    + Add interface [new_cursor](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.vector.Vector.new_cursor), [remove_cursor](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.vector.Vector.remove_cursor) in Vector.
    + Add interface [new_row_cursor](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.table.Table.new_col_cursor), [new_col_cursor](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.table.Table.new_row_cursor) in Table.
+ Add [reshape](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.table.Table.reshape) interface in Table.
+ Compress SVG size for tables with very many cells.
+ Changed the index range check rule for [insert](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.vector.Vector.insert), [pop](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.vector.Vector.pop), [swap](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.vector.Vector.swap) interfaces in Vector, raise exception when index out of range.

## algviz 0.1.0

This is the first public release of algviz. Support animation generation for vector, table, linked list, tree and graph data structures in jupyter notebook.
