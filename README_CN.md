# 项目介绍

[<img src="https://cdn.jsdelivr.net/gh/zjl9959/algviz@main/docs/images/logo_v1.svg"/>](https://algviz.com)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/algviz)
![PyPI](https://img.shields.io/pypi/v/algviz)
![Conda-forge](https://img.shields.io/conda/vn/conda-forge/algviz)
![License](https://img.shields.io/github/license/zjl9959/algviz)

## 关于本项目

[Algviz](https://algviz.com) 是一个可以在你的 [Jupyter](https://jupyter.org/) 笔记中执行的算法动画引擎。 它支持多种数据结构的动画生成，例如下面的 `向量`、`表格`、`链表`、`树` 和 `拓扑图`。

| 向量 | 表格 | 树 | 拓扑图 |
|:---:|:---:|:---:|:---:|
|  ![vector.svg] |   ![table.svg]  |  ![tree.svg]   |  ![graph.svg]   |

你只需要在代码中引入少量的 algviz 接口，就可以得到栩栩如生的动画，来演示你的算法运行过程。

例如，下面的代码展示了一个冒泡排序算法的例子：

<details>

<summary>点击显示代码块</summary>

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

渲染出来的动画效果如下：

![冒泡排序算法动画](https://cdn.jsdelivr.net/gh/zjl9959/algviz-launch@master/svgs/BubbleSort.svg)

*如果你觉得本项目不错，请点一个收藏⭐，谢谢！*

## 例子

准备好见证奇迹了吗？点击下面的按钮即可在 Gitpod 云编辑器中在线运行演示笔记！

[![Open algviz examples in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/zjl9959/algviz-launch) *需要使用 Github 账户登录。*

## 安装步骤

请参考官网中的 [本地安装指南](https://algviz.com/cn/installation.html)。

## 教程

该链接中的 [教程](https://algviz.com/en/examples.html) 会帮你快速上手 algviz。

完整的接口文档请参考：[algviz API reference](https://algviz.readthedocs.io/en/latest/api.html#).

## 许可证

Algviz 使用 [GPL-v3 许可证](https://github.com/zjl9959/algviz/blob/main/LICENSE)，你可以免费使用它进行交流和学习！如需商用请联系作者！

## 贡献

欢迎大家为本项目做任何形式的贡献，包括报告 [bug](https://github.com/zjl9959/algviz/issues) 或是提交 [pull request](https://github.com/zjl9959/algviz/pulls).

此外，如果你想要分享使用了 algviz 的算法动画笔记，请到 👉 [algviz-launch](https://github.com/zjl9959/algviz-launch) 仓库中提交一个 [PR](https://github.com/zjl9959/algviz-launch/pulls)。

[bubble sort algorithm]: https://en.wikipedia.org/wiki/Bubble_sort
[vector.svg]: https://cdn.jsdelivr.net/gh/zjl9959/algviz.com@master/assets/img/data_vector.svg
[table.svg]: https://cdn.jsdelivr.net/gh/zjl9959/algviz.com@master/assets/img/data_table.svg
[tree.svg]: https://cdn.jsdelivr.net/gh/zjl9959/algviz.com@master/assets/img/data_tree.svg
[graph.svg]: https://cdn.jsdelivr.net/gh/zjl9959/algviz.com@master/assets/img/data_graph.svg


## 讨论组

**QQ群**: [334605370](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=NYzoqZd6B8sryXf0S8o1uv72b_p2M5ai&authKey=qTbFUbVoI%2F8RWZVmlabPkuBHnuY2RzywEnKeNZlV8dOhcdcKY%2BoiYnPklmdfpwlE&noverify=0&group_code=334605370)
