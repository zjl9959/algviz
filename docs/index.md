# Algviz

## Links:

+ GitHub: https://github.com/zjl9959/algviz
+ PyPi: https://pypi.org/project/algviz/
+ ReadtheDocs: https://algviz.readthedocs.io/en/latest/index.html

## What is algviz?

Algviz is an algorithm visualization tool for Jupyter-notebook.

Algviz can generate visualize animations for `vector`, `table`, `linked list`, `tree` and `graph` data structures.
You can bring your code to life after insert a few algviz [interfaces](https://algviz.readthedocs.io/en/latest/api.html#module-algviz) into code. All the animations were 
generated in real time, so you can easily preview the changes of the data with animation like that:

![vector_swap_animation](https://raw.githubusercontent.com/zjl9959/algviz/7532a63e4301f8f7652c1c59962f1a87643839cc/docs/animation_images/vector_swap_animation.svg)

If you come up with a good algorithm that can solve a problem, but don't know how to describe it to your friends. At this point, you can use algviz to create an intuitive animation demo to show to working process of your algorithm. The point is, you don't need to know about fundamentals of animation at all. Leave the dirty work to algviz and just focus on how to implement your algorithm.

It's useful when you try to express the working process of a complex algorithm.
For example, it's hard to image in mind the whole detail of [mirror binary tree](https://medium.com/@ajinkyajawale/convert-a-binary-tree-into-its-mirror-tree-42ea44cea237) algorithm.
Because the algorithm including some recursive operations on a binary tree, which subtree was moved first is a headache problem. But no matter how complex the binary tree is, algviz can tell you how the algorithm works by intuitive animations.

This animation below shows one swap subtrees operation in mirror binary tree algorithm:

![mirror_tree_animation](https://raw.githubusercontent.com/zjl9959/algviz/7532a63e4301f8f7652c1c59962f1a87643839cc/docs/animation_images/mirror_tree_animation.svg)

Furthermore, algviz provides some encapsulated data classes which support operations like python builtin class. For example, you can iterate on the [algviz.Vector](https://algviz.readthedocs.io/en/latest/api.html#algviz.vector.Vector) class just like Python list:

```python
import algviz                   # Import algviz library.
viz = algviz.Visualizer()       # Create a visualizer object.
data = [1, 2, 3]
vector = viz.createVector(data) # Create a vector data object.
for num in vector:              # Iterate over all the elements in vector.
    print(num)
    viz.display()               # Refresh the animation in Jupyter-notebook.
```

You can modify the data multi-times, and algviz will record all the operations since last time you call the [display](https://algviz.readthedocs.io/en/latest/api.html#algviz.visual.Visualizer.display) interface. Then it will merge all the operations in one animation when you call display next time. So the only thing you need to concern is: `when to call the display interface?` Because some operations may override other operations and the output animation may be confusing.

These animations below shows multiple operations in one render output:

+ Two [insert](https://algviz.readthedocs.io/en/latest/api.html#algviz.vector.Vector.insert) operations on vector. (Insert two elements "0" and "1" into vector ["a", "b", "c"].)

    ![vector_move_animation](https://raw.githubusercontent.com/zjl9959/algviz/7532a63e4301f8f7652c1c59962f1a87643839cc/docs/animation_images/vector_move_animation.svg)

+ Modify two edges on graph. ([Add](https://algviz.readthedocs.io/en/latest/api.html#algviz.graph.GraphNode.add) node7 into node5's neighbors;
[Remove](https://algviz.readthedocs.io/en/latest/api.html#algviz.graph.GraphNode.remove) nodes4 from node5's neighbors).

    ![graph_move_animation](https://raw.githubusercontent.com/zjl9959/algviz/7532a63e4301f8f7652c1c59962f1a87643839cc/docs/animation_images/graph_move_animation.svg)

All the animations created by algviz are [SVG](https://www.w3.org/Graphics/SVG/) string format. You can export the animation frames and review it in browser or embedded it in your slides.


## How to install algviz?

### Step1: Install Jupyter-notebook

Algviz can only run in [Jupyter-notebook](https://jupyter.org/). You can choose any of the following methods to install Jupyter-notebook.

+ If you are a vscode user, you can install Jupyter [extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) for vscode.
+ [Install Jupyter](https://jupyter.org/install) in your computer and view the animation on your browser.
+ [Install anaconda](https://docs.anaconda.com/anaconda/install/index.html) and [use Jupyter-notebook](https://docs.anaconda.com/ae-notebooks/user-guide/basic-tasks/apps/jupyter/index.html) in it.

### Step2: Install Graphviz

[Graphviz](https://graphviz.org/) was used to generate static layout of topology graph.
It's a popular open source software, you can download the program in it's [official site](https://graphviz.org/download/).

*Note: please remember to add graphviz into your system's environment path so that other programs can call it directly.*

### Step3: Install algviz

Note: algviz run on Python 3.7 or heigher version of Python.

```shell
python -m pip install --upgrade pip
pip install algviz
```

## How to use algviz?

TODO: Add online notebook examples.
