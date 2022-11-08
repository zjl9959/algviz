# Algviz

[Website](https://algviz.com/index_en.html) | 
[中文官网](https://algviz.com/index.html) | 
[GitHub](https://github.com/zjl9959/algviz) | 
[PyPi](https://pypi.org/project/algviz/) | 
[ReadtheDocs](https://algviz.readthedocs.io/en/latest/index.html)

## Introduce

<div align=center><img src="https://cdn.jsdelivr.net/gh/zjl9959/algviz@main/docs/images/logo_v1.svg"/></div>

Algviz is an algorithm visualization tool for your Python code in [Jupyter-notebook](https://jupyter.org/).

Algviz can generate visual animations for `vector`, `table`, `linked list`, `tree`, and `graph` data structures.
You can bring alive animations in your notebook after inserting a few algviz [interfaces](https://algviz.readthedocs.io/en/latest/api.html#module-algviz) into code. For example, this animation shows a [bubble sort algorithm]:

![bubble_sort_animation](https://cdn.jsdelivr.net/gh/zjl9959/algviz@main/docs/animation_images/bubble_sort.svg)

If you come up with a good algorithm that can solve a problem but don't know how to describe it to your friends. At this point, you can use algviz to create an intuitive animation demo to show the working process of your algorithm. The point is, that you don't need to know about the fundamentals of animation at all. Leave the dirty work to algviz and just focus on how to implement your algorithm.

It's useful when you try to express the working process of a complex algorithm.
For example, it's hard to imagine in mind the whole detail of [mirror binary tree](https://medium.com/@ajinkyajawale/convert-a-binary-tree-into-its-mirror-tree-42ea44cea237) algorithm.
Because the algorithm includes some recursive operations on a binary tree, which subtree was moved first is a headache problem. But no matter how complex the binary tree is, algviz can tell you how the algorithm works by intuitive animations.

![mirror_tree_animation](https://cdn.jsdelivr.net/gh/zjl9959/algviz@main/docs/animation_images/mirror_tree_complete.svg)

Furthermore, algviz provides some encapsulated data classes which support operations like Python built-in class. For example, you can iterate on the [algviz.Vector](https://algviz.readthedocs.io/en/latest/api.html#algviz.vector.Vector) class just like Python list:

```python
import algviz                   # Import algviz library.
viz = algviz.Visualizer()       # Create a visualizer object.
data = [1, 2, 3]
vector = viz.createVector(data) # Create a vector data object.
for num in vector:              # Iterate over all the elements in vector.
    print(num)
    viz.display()               # Refresh the animation in Jupyter-notebook.
```

You can modify the data multi-times, and algviz will record all the operations since the last time you call the [display](https://algviz.readthedocs.io/en/latest/api.html#algviz.visual.Visualizer.display) interface. Then it will merge all the operations in one animation when you call display next time. So the only thing you need to be concerned about is: `when to call the display interface?`


## Installation

### Step1: Install Jupyter-notebook

You can choose any of the following methods to install:

+ If you are a [vscode](https://code.visualstudio.com/) user, you can install Jupyter [extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) for vscode.
+ [Install Jupyter](https://jupyter.org/install) on your computer and view the animation on your browser.
+ [Install anaconda](https://docs.anaconda.com/anaconda/install/index.html) and [use Jupyter-notebook](https://docs.anaconda.com/ae-notebooks/user-guide/basic-tasks/apps/jupyter/index.html) in it.

### Step2: Install Graphviz

[Graphviz](https://graphviz.org/) is used to generate the static layout of the topology graph.
It's a popular open-source software, you can download the program on it's [official site](https://graphviz.org/download/).

*Note: please remember to add graphviz into your system's environment path so that other programs can call it directly.*

### Step3: Install algviz

Note: algviz runs on Python 3.7 or heigher versions.

```shell
python -m pip install --upgrade pip
pip install algviz
```

## API Reference

All the API references for algviz can be found on [readthedocs](https://algviz.readthedocs.io/en/latest/api.html#).

## Examples

The [examples](https://github.com/zjl9959/algviz/tree/main/examples) folder contains some tutorials on how to start with algviz. You can set up your local environment and try them in your notebook. And if you are a google [colab](https://colab.research.google.com/) user, you can try with the google colab links. Try your first cool algviz code and good luck!😀


| Example         |  Github link            | Google Colab link          |  Description                       |
| :----           | :------                 | :---------                 | :-------                           |
| **vector**      | [vector.ipynb]          | [vector.ipynb colab]       | Basic operations on [Vector] class. <br> Example of `bubble sort algorithm`. |
| **table**       | [table.ipynb]           | [table.ipynb colab]        | Basic operations on [Table] class.  |
| **linked list** | [linked_list.ipynb]     | [linked_list.ipynb colab]  | Create linked list and operate [ForwardLinkedNode], [DoublyLinkedNode] classes. |
| **tree**        | [tree.ipynb]            | [tree.ipynb colab]         | Create [binary tree], [normal tree] <br> Operate [TreeNode], [BinaryTreeNode] classes. <br> Example of `mirror binary tree`. <br> Example of construct `trie tree`. |
| **graph**       | [graph.ipynb]           | [graph.ipynb colab]        | Create [graph] and operate [GraphNode] class. |


## Unit Test

Make sure you have successfully installed [algviz](https://pypi.org/project/algviz/) from PyPi and download the [test codes](https://github.com/zjl9959/algviz/tree/main/tests) from Github.

Then call the command:

```shell
python tests/run.py
```

If you see the output like this:

> Congratulations, everything is OK !!!

It means algviz works fine in your environment.
But if you get any unexpected errors, please [report](https://github.com/zjl9959/algviz/issues) the bug.

## License

Algviz uses GNU general public [LICENSE](https://github.com/zjl9959/algviz/blob/main/LICENSE). You can use it freely for learning and communication.


[Vector]: https://algviz.readthedocs.io/en/latest/api.html#algviz.vector.Vector
[Table]: https://algviz.readthedocs.io/en/latest/api.html#algviz.table.Table
[ForwardLinkedNode]: https://algviz.readthedocs.io/en/latest/api.html#algviz.linked_list.ForwardLinkedListNode
[DoublyLinkedNode]: https://algviz.readthedocs.io/en/latest/api.html#algviz.linked_list.DoublyLinkedListNode
[binary tree]: https://algviz.readthedocs.io/en/latest/api.html#algviz.tree.parseBinaryTree
[normal tree]: https://algviz.readthedocs.io/en/latest/api.html#algviz.tree.parseTree
[TreeNode]: https://algviz.readthedocs.io/en/latest/api.html#algviz.tree.TreeNode
[graph]: https://algviz.readthedocs.io/en/latest/api.html#algviz.graph.parseGraph
[GraphNode]: https://algviz.readthedocs.io/en/latest/api.html#algviz.graph.GraphNode

[vector.ipynb]: https://github.com/zjl9959/algviz/blob/main/examples/vector.ipynb
[table.ipynb]: https://github.com/zjl9959/algviz/blob/main/examples/table.ipynb
[linked_list.ipynb]: https://github.com/zjl9959/algviz/blob/main/examples/linked_list.ipynb
[tree.ipynb]: https://github.com/zjl9959/algviz/blob/main/examples/tree.ipynb
[graph.ipynb]: https://github.com/zjl9959/algviz/blob/main/examples/graph.ipynb
[vector.ipynb colab]: https://colab.research.google.com/drive/1RgAoKbiSBXdSvBg65pwu9pJp5bQL1pCs?usp=sharing
[table.ipynb colab]: https://colab.research.google.com/drive/1GH6XgKDpUA2GKxiLm5tljp19wUvmnDxO?usp=sharing
[linked_list.ipynb colab]: https://colab.research.google.com/drive/1rsg-6irXzQODPi6DUZhtu-pKq_r55hwV?usp=sharing
[tree.ipynb colab]: https://colab.research.google.com/drive/138pnzwoS2vdhssZyTx-k5rwBQNb2Hi9N?usp=sharing
[graph.ipynb colab]: https://colab.research.google.com/drive/14hF30-N9VGBb5-vkERPuURvmnB9VspU9?usp=sharing

[bubble sort algorithm]: https://en.wikipedia.org/wiki/Bubble_sort
