# Changelog

## algviz 0.3.0

+ Support to layout different display objects and assemble the animation sequences. To use this feature, you need to do these things:

    1. The layout engine is platform specific, please make sure your OS is `Windows` or `Linux` and your platform is `amd64/x86_64` architecture.
    2. Add the `layout=True` parameter when creating the [`Visualizer`](https://algviz.readthedocs.io/en/0.3.0/api.html#algviz.visual.Visualizer) object (the default value of `layout` is `False` for compatibility).
    3. Add the [`Visualizer.layout`](https://algviz.readthedocs.io/en/0.3.0/api.html#algviz.visual.Visualizer.layout) function in your code where you want to assemble the animation sequences (usually at the end of the code path).

    <img src="https://raw.githubusercontent.com/zjl9959/algviz/main/docs/animation_images/layout_example.gif" alt="layout_example.gif" width=400px/>

+ **Fix bug**: [Histogram vector zero height cell text size error](https://github.com/zjl9959/algviz/issues/8).

## algviz 0.2.3

+ Adaptation to recent versions of the ipython library (8.0.0 ~ 8.12.0).
+ **New feature**: Added the [`generateRandomGraph`](https://algviz.readthedocs.io/en/0.2.3/api.html#algviz.graph.generateRandomGraph) interface, related [issue7](https://github.com/zjl9959/algviz/issues/7).
+ **Fix bug**: [Access table with cursor throw exception when "show_index=False"](https://github.com/zjl9959/algviz/issues/5)

## algviz 0.2.2

+ Add a new class [Map](https://algviz.readthedocs.io/en/0.2.2/api.html#algviz.map.Map) which can be used like the Python `dict` builtin.

    ![map_class_example](https://cdn.jsdelivr.net/gh/zjl9959/algviz@main/docs/animation_images/map_class_example.svg)

+ Fix bugs: `table.reshape` error, [algviz.parseBinaryTree issue](https://github.com/zjl9959/algviz/issues/4).

## algviz 0.2.1

+ Layout and display optimizations for [RecursiveTree](https://algviz.readthedocs.io/en/0.2.1/api.html#algviz.tree.RecursiveTree) and undirected graph.
+ Fix some typos and small mistakes.

## algviz 0.2.0

+ **New feature**: add animation effect for text labels in Vector, Table and Graph nodes.

    ![vector_text_animation](https://cdn.jsdelivr.net/gh/zjl9959/algviz@main/docs/animation_images/vector_text_animation.svg)

+ **New interfaces**: [Vector.removeMarks](https://algviz.readthedocs.io/en/0.2.0/api.html#algviz.vector.Vector.removeMarks), [Table.removeMarks](https://algviz.readthedocs.io/en/0.2.0/api.html#algviz.table.Table.removeMarks), [SvgGraph.removeMarks](https://algviz.readthedocs.io/en/0.2.0/api.html#algviz.svg_graph.SvgGraph.removeMarks) can remove multiple color marks in the display object.
+ **Change interface**: [Table.mark](https://algviz.readthedocs.io/en/0.2.0/api.html#algviz.table.Table.mark) adds two parameters `r2` and `c2` to support marking multiple elements in the given rectangle area.
+ **Fixed bugs**:
    + Unit tests failed for Logger.
    + Display area is clipped in some Logger object.
    + Refresh error when calling [Logger.clear](https://algviz.readthedocs.io/en/0.2.0/api.html#algviz.logger.Logger.clear).

## algviz 0.1.8

+ **New interfaces**:
    + [TreeNode.childCount](https://algviz.readthedocs.io/en/0.1.8/api.html#algviz.tree.TreeNode.childCount) returns the children nodes count. 
    + [GraphNode.neighborCount](https://algviz.readthedocs.io/en/0.1.8/api.html#algviz.graph.GraphNode.neighborCount) returns the neighbors count of this node.
+ **Logger new display style**: set the log font size and wheather to show log line num in the [Visualizer.createLogger](https://algviz.readthedocs.io/en/0.1.8/api.html#algviz.visual.Visualizer.createLogger) interface.

## algviz 0.1.7

+ New interfaces [TreeNode.childAt](https://algviz.readthedocs.io/en/0.1.7/api.html#algviz.tree.TreeNode.childAt),
[TreeNode.childIndex](https://algviz.readthedocs.io/en/0.1.7/api.html#algviz.tree.TreeNode.childIndex) and 
[TreeNode.removeAt](https://algviz.readthedocs.io/en/0.1.7/api.html#algviz.tree.TreeNode.removeAt) for `TreeNode`.
+ New interfaces [GraphNode.neighborAt](https://algviz.readthedocs.io/en/0.1.7/api.html#algviz.graph.GraphNode.neighborAt),
[GraphNode.neighborIndex](https://algviz.readthedocs.io/en/0.1.7/api.html#algviz.graph.GraphNode.neighborIndex) and 
[GraphNode.removeAt](https://algviz.readthedocs.io/en/0.1.7/api.html#algviz.graph.GraphNode.removeAt) for `GraphNode`.

## algviz 0.1.6

+ **Interfaces change**
    + [Visualizer.createCursor](https://algviz.readthedocs.io/en/0.1.6/api.html#algviz.visual.Visualizer.createCursor) swap the position of parameters `offset` and `name`.
    + [Visualizer.cursorRange](https://algviz.readthedocs.io/en/0.1.6/api.html#algviz.visual.Visualizer.cursorRange) swap the position of parameters `step` and `name`.
    + Add a new class [RecursiveTree](https://algviz.readthedocs.io/en/0.1.6/api.html#algviz.tree.RecursiveTree), which can make it easier to track the recursive algorithm.
+ **Fixed bugs**:
    + Crash when the [TreeNode](https://algviz.readthedocs.io/en/0.1.6/api.html#algviz.tree.TreeNode) value is an empty string.
    + [CursorRange](https://algviz.readthedocs.io/en/0.1.6/api.html/#algviz.Visualizer.cursorRange) iterator range error.

## algviz 0.1.5

+ Fixed some known bugs about cursor.
+ Update some constructor interfaces.

## algviz 0.1.4

This version adjusts the interfaces to create or remove cursors.
Instead of creating the identical cursors bound with different Vector or Table objects,
you can create the cursor one time then it will be bound with display objects which been accessed by the cursor.

+ **Interfaces change**:
    + **[Cursor](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.cursor.Cursor) operations extend**:
        + Add assignment operation: `<<`
        + Add mathmatics operations: `%`, `+=`, `-=`, `*=`, `//=`, `%=`
    + **Added interfaces**: [Visualizer.createCursor](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.visual.Visualizer.createCursor), [Visualizer.removeCursor](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.visual.Visualizer.removeCursor), [Visualizer.cursorRange](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.visual.Visualizer.cursorRange)
    + **Deprecated interfaces**: [Vector.new_cursor](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.vector.Vector.new_cursor), [Vector.remove_cursor](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.vector.Vector.remove_cursor), [Table.new_col_cursor](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.table.Table.new_col_cursor), [Table.new_row_cursor](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.table.Table.new_row_cursor), [Table.remove_cursor](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.table.Table.remove_cursor), [Cursor.dec](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.cursor.Cursor.dec), [Cursor.inc](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.cursor.Cursor.inc), [Cursor.update](https://algviz.readthedocs.io/en/0.1.3/api.html#algviz.cursor.Cursor.update).
+ Added new class: [AlgvizTypeError](https://algviz.readthedocs.io/en/0.1.4/api.html#algviz.utility.AlgvizTypeError).
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
