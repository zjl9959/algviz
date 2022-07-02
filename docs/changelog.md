# Changelog

## algviz 0.1.4

This version adjusts the interfaces to create or remove cursors.
Instead of creating the identical cursors bound with different Vector or Table objects,
you can create the cursor one time then it will be bound with display objects which been accessed by the cursor.

+ **Interfaces change**:
    + **[Cursor](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.cursor.Cursor) operations extend**:
        + Add assignment operation: `<<`
        + Add mathmatics operations: `%`, `+=`, `-=`, `*=`, `//=`, `%=`
    + **Added interfaces**: [`Visualizer.createCursor`](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.visual.Visualizer.createCursor), [`Visualizer.removeCursor`](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.visual.Visualizer.removeCursor), [`Visualizer.cursorRange`](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.visual.Visualizer.cursorRange)
    + **Deprecated interfaces**: [`Vector.new_cursor`](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.vector.Vector.new_cursor), [`Vector.remove_cursor`](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.vector.Vector.remove_cursor), [`Table.new_col_cursor`](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.table.Table.new_col_cursor), [`Table.new_row_cursor`](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.table.Table.new_row_cursor), [`Table.remove_cursor`](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.table.Table.remove_cursor), [`Cursor.dec`](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.cursor.Cursor.dec), [`Cursor.inc`](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.cursor.Cursor.inc), [`Cursor.update`](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.cursor.Cursor.update).
+ Added new class: [`AlgvizTypeError`](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.utility.AlgvizTypeError)
+ Fixed bugs:
    + Can not access Table row/column index with Cursor object.
    + Cursor move distance error when cell width is not equal with cell height in Table/Vector.

## algviz 0.1.3

+ **Interfaces change**:
    + Remove [colorsInfo()](https://algviz.readthedocs.io/en/0.1.1/api.html#algviz.colorsInfo) and `colors`, use `color_black`, `color_red` and so on instead.
    + Update interface [Visualizer.createTable](https://algviz.readthedocs.io/en/latest/api.html#algviz.visual.Visualizer.createTable): change the type of paramter `cell_size` from **float** into **tuple(float, float)**, in order to support setting the cell height of table elements.
    + Update interface [Visualizer.createVector](https://algviz.readthedocs.io/en/latest/api.html#algviz.visual.Visualizer.createVector):
        + Change the type of paramter `cell_size` from **float** into **tuple(float, float)**, in order to support setting the cell height of vector elements.
        + Change the paramter `bar` into `histogram`(type is **bool**, means display the data in the form of a histogram).
    + Update interfaces `Vector.mark`, `Table.mark`, `SvgGraph.markNode` and `SvgGraph.markEdge`: change the default value of paramter `hold` from **True** into **False**.
+ **Display change:**
    + Change `Logger` display format into normal string.
    + Display the name of visualizer objects by string instead of `Table`.
    + No longer mark items cell automatically when access or modify data in items.
+ Remove useless comments and titles in the SVG output result of `SvgGraph`..

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
