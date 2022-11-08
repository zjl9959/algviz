#!/usr/bin/env python3

"""Define tree related classes and functions.

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.utility import AlgvizParamError
from algviz.graph_node_base import GraphNodeBase as NodeBase


class BinaryTreeNode(NodeBase):
    """The definition of a binary tree node.

    Attributes:
        val (printable): The label to be displayed in the binary tree node.
        left (BinaryTreeNode): Point to the left subtree node object.
        right (BinaryTreeNode): Point to the right subtree node object.
    """

    def __init__(self, val, left=None, right=None):
        """
        Args:
            val (printable): The label value for binary node(should be printable object).
            left (BinaryTreeNode): Point to the left subtree node object.
            right (BinaryTreeNode): Point to the right subtree node object.
        """
        super().__init__(val)
        super().__setattr__('left', left)
        self._on_update_neighbor_(left)
        super().__setattr__('right', right)
        self._on_update_neighbor_(right)
    

    def __getattribute__(self, name):
        if name == 'left' or name == 'right':
            node = super().__getattribute__(name)
            return node
        else:
            return super().__getattribute__(name)
    

    def __setattr__(self, name, value):
        if name == 'left' or name == 'right':
            super().__setattr__(name, value)
            self._on_update_neighbor_(value)
        else:
            super().__setattr__(name, value)


    def _neighbors_(self):
        """Return all children nodes of this tree node.
        
        Returns:
            list(tuple(BinaryTreeNode, None)): Return left child node and right child node.
        """
        left_node = super().__getattribute__('left')
        right_node = super().__getattribute__('right')
        # Add edge label if this node just has single child node.
        left_label, right_label = None, None
        if left_node and not right_node:
            left_label = 'L'
        elif right_node and not left_node:
            right_label = 'R'
        return [(left_node, left_label), (right_node, right_label)]


def parseBinaryTree(tree_info):
    """ Create a new Tree from given node values.
    
    Args:
        tree_info (list(printable)): The label of each node in the tree must be given.
            Empty node is represented by None. eg:([1, None, 2, None, None, 3, 4])
    
    Returns:
        TreeNode: Root node object of this tree.
    """
    if len(tree_info) == 0:
        return None
    root = BinaryTreeNode(tree_info[0])
    node_queue = [root]
    index = 1
    while len(node_queue) > 0:
        cur_node = node_queue.pop(0)
        if index >= len(tree_info):
            break
        left_node = None
        if tree_info[index] is not None:
            left_node = BinaryTreeNode(tree_info[index])
        node_queue.append(left_node)
        if index + 1 >= len(tree_info):
            break
        right_node = None
        if tree_info[index + 1] is not None:
            right_node = BinaryTreeNode(tree_info[index+1])
        node_queue.append(right_node)
        if cur_node is not None:
            cur_node.left = left_node
            cur_node.right = right_node
        index += 2
    return root


class TreeChildrenIter():
    """Iterator for the children of TreeNode object.
    """
    def __init__(self, node, children):
        self._node = node
        self._children = children
        self._next_index = 0


    def __iter__(self):
        self._next_index = 0
        return self


    def __next__(self):
        if self._next_index >= len(self._children):
            raise StopIteration
        else:
            child = self._children[self._next_index]
            self._next_index += 1
            return child


class TreeNode(NodeBase):
    """A tree node has multiply children node.

    Attributes:
        val (printable): The label to be displayed in the binary tree node.
    """
    def __init__(self, val):
        """
        Args:
            val (printable): The label value for tree node.
        """
        super().__init__(val)
        super().__setattr__('_children', list())
    

    def children(self):
        """Return an iterator to iter over all the children nodes of this node.
        
        Returns:
            TreeChildrenIter: Children node iterator.
        """
        children_ = super().__getattribute__('_children')
        return TreeChildrenIter(self, tuple(children_))


    def childAt(self, index):
        """Return the child node at the index position of the children list.
        
        Args:
            index (int): The position of the child node.

        Returns:
            TreeNode: child node.

        Raises:
            AlgvizParamError: TreeNode child index type error or out of range.
        """
        children_ = super().__getattribute__('_children')
        if type(index) != int or index < 0 or index >= len(children_):
            raise AlgvizParamError('TreeNode child index type error or out of range.')
        return children_[index]


    def childIndex(self, child):
        """Return the child node index in the children list.

        Args:
            child (TreeNode): The child node object to be located.

        Returns:
            int: the index position of the child node. If child not found, then return -1.
        """
        res = -1
        children_ = super().__getattribute__('_children')
        for i in range(len(children_)):
            if child == children_[i]:
                res = i
        return res


    def add(self, child, index=None):
        """Add a child node for this node.
        
        Args:
            child (TreeNode): The child node object to be added.
            index (int): The position to insert the child node.

        Raises:
            AlgvizParamError: TreeNode child index should be a positive integer!
        """
        if (type(index) != int and index != None) or (type(index) == int and index < 0):
            raise AlgvizParamError('TreeNode child index should be a positive integer!')
        children_ = super().__getattribute__('_children')
        for n in children_:
            if child == n:
                return
        if index == None or index >= len(children_):
            children_.append(child)
        else:
            children_.insert(index, child)
        self._on_update_neighbor_(child)


    def remove(self, child):
        """Remove one child node.
        
        Args:
            child (TreeNode): The child node to be removed.
        """
        children_ = super().__getattribute__('_children')
        for i in range(len(children_)):
            if child == children_[i]:
                children_.pop(i)
                self._on_update_neighbor_(None)
                return

    
    def removeAt(self, index):
        """Remove the child at the index position.

        Args:
            index (int): The child node index to be removed.

        Raises:
            AlgvizParamError: TreeNode child index type error or out of range.
        """
        children_ = super().__getattribute__('_children')
        if type(index) != int or index < 0 or index >= len(children_):
            raise AlgvizParamError('TreeNode child index type error or out of range.')
        children_.pop(index)
        self._on_update_neighbor_(None)


    def _neighbors_(self):
        children_ = super().__getattribute__('_children')
        res = list()
        for child in children_:
            res.append((child, None))
        return res


def parseTree(tree_info, nodes_label=None):
    """Create a Tree from node_map information and return the root node.
    
    Input tree_info should meet these constraints:
        
        1. Each node must have one parent node expect for the root node.

        2. The node id in tree info should be unique,
        but you can set the nodes_label to map the unique id into it's display label text.

    Args:
        tree_info (dict(printable:list(printable))): Describe the linked information of this tree.
            Key is the label of root node, Value is the list of it's children nodes label.
        nodes_label (dict(printable:printable)): Map the node id into it's display label.
    
    Returns:
        TreeNode: The root node of this tree.

    Raises:
        AlgvizParamError: (parseTree) node xxx have more than one parent node!
        AlgvizParamError: (parseTree) tree has more than one root node.
    """
    # Create TreeNode objects.
    nodes_dict = dict()
    child_nodes = set()     # Used to find the root node and check the validity of tree.
    for node, children in tree_info.items():
        # Create parent node.
        node_val = node
        if nodes_label and node in nodes_label:
            node_val = nodes_label[node]
        nodes_dict[node] = TreeNode(node_val)
        for child in children:
            # Create children nodes.
            if child not in child_nodes:
                child_nodes.add(child)
                node_val = child
                if nodes_label and child in nodes_label:
                    node_val = nodes_label[child]
                nodes_dict[child] = TreeNode(node_val)
            else:
                raise AlgvizParamError('(parseTree) node {} have more than one parent node!'.format(child))
    # Check and find the root node of this tree.
    root = None
    for node in tree_info.keys():
        if node not in child_nodes:
            if not root:
                root = node
            else:
                raise AlgvizParamError('(parseTree) tree has more than one({}, {}) root node.'.format(root, node))
    # Link the edge between root and it's child.
    for node, children in tree_info.items():
        parent_node = nodes_dict[node]
        for child in children:
            child_node = nodes_dict[child]
            parent_node.add(child_node)
    return nodes_dict[root]


class RecursiveTree():
    """Used to trace the recursive process in the recursive algorithm.
    """
    def __init__(self, viz, name="Recursive tree"):
        """
        Args:
            viz (Visualizer): The visualizer object that contains this recursive tree.
            name (printable): The display name of this recursive tree.
        """
        self.root = TreeNode("root")
        self.graph = viz.createGraph([self.root], name, True)
        self.stack = list()     # Recursive stack.

    def forward(self, val=''):
        """Forward to a new depth of this recursive tree.
        Args:
            val (printable): The label to be displayed in the recursive tree node.
        """
        node = TreeNode(val)
        self.root.add(node)
        self.graph.removeMark((173, 255, 47))
        self.graph.markNode((173, 255, 47), node, hold=True)
        self.stack.append(self.root)
        self.root = node

    def backward(self):
        """Backward to the last visited node in the recursive tree.
        """
        self.graph.markNode((192, 192, 192), self.root, hold=True)
        self.root = self.stack.pop()
        self.graph.removeMark((255, 99, 71))
        self.graph.markNode((255, 99, 71), self.root, hold=True)
