# Algviz

[<img src="https://cdn.jsdelivr.net/gh/zjl9959/algviz@main/docs/images/logo_v1.svg"/>](https://algviz.com)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/algviz)
![PyPI](https://img.shields.io/pypi/v/algviz)
![Conda-forge](https://img.shields.io/conda/vn/conda-forge/algviz)
![License](https://img.shields.io/github/license/zjl9959/algviz)

[中文介绍文档](README_CN.md)

## What is algviz?

[Algviz](https://algviz.com) is an algorithm animation engine for your Python code in [Jupyter](https://jupyter.org/), which supports multiple data structures such as `vector`, `table`, `linked_list`, `tree` and `graph`.

| Vector | Table | Tree | Graph |
|:---:|:---:|:---:|:---:|
|  ![vector.svg] |   ![table.svg]  |  ![tree.svg]   |  ![graph.svg]   |

You can get live algorithm animation after bringing some algviz interfaces to your algorithm.
For example, this code below shows the bubble sort algorithm:

<details>

<summary>Click to show the code example</summary>

```python
import algviz

def bubble_sort(data):
    viz = algviz.Visualizer(0.5)
    vector = viz.createVector(data, cell_size=(40, 160), histogram=True)
    for i in range(len(vector)):
        for j in range(len(vector)-i-1):
            if vector[j] > vector[j+1]:
                vector.mark(algviz.cRed, j)
                vector.mark(algviz.cGreen, j+1)
                viz.display()
                vector.swap(j, j+1)
            else:
                vector.mark(algviz.cRed, j+1)
                vector.mark(algviz.cGreen, j)
            viz.display()
        vector.mark(algviz.cGray, len(vector)-i-1, hold=True)
    vector.removeMark(algviz.cGray)
    viz.display()

bubble_sort([5, 4, -2, 1, -1, 3])
```

</details>

<br>

The rendered animation looks like this:

![bubble_sort_animation](https://cdn.jsdelivr.net/gh/zjl9959/algviz-launch@master/svgs/BubbleSort.svg)

*If you are interested in this project, please give me a star⭐, thanks!*

## Examples

Ready to see the magic? Click this button to try more algorithms on Gitpod!

[![Open algviz examples in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/zjl9959/algviz-launch) *Need to login with your github account.*

## Installation

Please follow this [installation guide](https://algviz.com/en/installation.html) to setup algviz.

## Tutorial

This [tutorial](https://algviz.com/en/examples.html) gives you a quick start on using algviz.

All the API references can be found at [algviz API reference](https://algviz.readthedocs.io/en/latest/api.html#).

## License

Algviz uses GNU general public [LICENSE](https://github.com/zjl9959/algviz/blob/main/LICENSE). You can use it freely for learning and communication. For the commercial usage, please contact the author.

## Contribution

Any form of contribution is welcomed! Please feel free to report a [bug](https://github.com/zjl9959/algviz/issues) or create a [pull request](https://github.com/zjl9959/algviz/pulls).

If you want to share your algorithms using algviz, you can create a [PR](https://github.com/zjl9959/algviz-launch/pulls) from this repo: 👉 [algviz-launch](https://github.com/zjl9959/algviz-launch).

[bubble sort algorithm]: https://en.wikipedia.org/wiki/Bubble_sort
[vector.svg]: https://cdn.jsdelivr.net/gh/zjl9959/algviz.com@master/assets/img/data_vector.svg
[table.svg]: https://cdn.jsdelivr.net/gh/zjl9959/algviz.com@master/assets/img/data_table.svg
[tree.svg]: https://cdn.jsdelivr.net/gh/zjl9959/algviz.com@master/assets/img/data_tree.svg
[graph.svg]: https://cdn.jsdelivr.net/gh/zjl9959/algviz.com@master/assets/img/data_graph.svg


## Discussion

**QQ group**: [334605370](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=NYzoqZd6B8sryXf0S8o1uv72b_p2M5ai&authKey=qTbFUbVoI%2F8RWZVmlabPkuBHnuY2RzywEnKeNZlV8dOhcdcKY%2BoiYnPklmdfpwlE&noverify=0&group_code=334605370)

**Telegram**: https://t.me/+mvF8Sivxr3thZWY1
