#!/usr/bin/env python3

"""Define linked list related classes and functions.

Including ForwardLinkedListNode, DoublyLinkedListNode class
and parseForwardLinkedList, parseDoublyLinkedList function to parse linked list from string.

Typical usage example:

  head = parseForwardLinkedList([1, 2, 3])  # Create a forward linked list: 1->2-3
  
  new_head = ForwardLinkedListNode(0)       # Create a forward linked list node: 0
  
  new_head.next = head                      # Link node into linked list, and get: 0->1->2->3

Author: zjl9959@gmail.com

License: GPLv3

"""

from algviz.graph_node_base import GraphNodeBase as NodeBase


class ForwardLinkedListNode(NodeBase):
    """The node for forward linked list.

    Attributes:
        val (printable): The label to be displayed in the forward linked list node.
        next (ForwardLinkedListNode): Point to the next ForwardLinkedListNode object.
    """

    def __init__(self, val, next=None):
        """
        Args:
            val (printable): The label to be displayed in forward linked list node.
            next (ForwardLinkedListNode): Point to the next ForwardLinkedListNode object.
        """
        super().__init__(val)
        super().__setattr__('next', next)
        self._on_update_neighbor_(next)


    def __getattribute__(self, name):
        if name == 'next':
            # Visit next node in the forward linked list and update the node's visit state.
            node = super().__getattribute__('next')
            return node
        else:
            return super().__getattribute__(name)
    

    def __setattr__(self, name, value):
        if name == 'next':
            super().__setattr__('next', value)
            self._on_update_neighbor_(value)
        else:
            super().__setattr__(name, value)
    

    def _neighbors_(self):
        """Interface for SvgGraph. Get this node's neighbors(next node).

        Returns:
            list(tuple(next_node, None)): The neighbors list of this node.
        """
        next_node = super().__getattribute__('next')
        return [(next_node, None)]


class DoublyLinkedListNode(NodeBase):
    """The node for doubly linked list.

    Attributes:
        val (printable): The label to be displayed in the doubly linked list node.
        prev (DoublyLinkedListNode): Point to the previous DoublyLinkedListNode object.
        next (DoublyLinkedListNode): Point to the next DoublyLinkedListNode object.
    """

    def __init__(self, val, prev=None, next=None):
        """
        Args:
            val (printable): The label to be displayed in doubly linked list node.
            prev (DoublyLinkedListNode): Point to the previous DoublyLinkedListNode object.
            next (DoublyLinkedListNode): Point to the next DoublyLinkedListNode object.
        """
        super().__init__(val)
        super().__setattr__('prev', prev)
        self._on_update_neighbor_(prev)
        super().__setattr__('next', next)
        self._on_update_neighbor_(next)


    def __getattribute__(self, name):
        if name == 'next' or name == 'prev':
            # Visit next node in the doubly linked list and update the node's visit state.
            node = super().__getattribute__(name)
            return node
        else:
            return super().__getattribute__(name)


    def __setattr__(self, name, value):
        if name == 'next' or name == 'prev':
            super().__setattr__(name, value)
            self._on_update_neighbor_(value)
        else:
            super().__setattr__(name, value)


    def _neighbors_(self):
        """Interface for SvgGraph. Get this node's neighbors(next node).
        
        Returns:
            list(tuple(next_node, None)): The neighbors list of this node.
        """
        next_node = super().__getattribute__('next')
        prev_node = super().__getattribute__('prev')
        return [(next_node, None), (prev_node, None)]


def parseForwardLinkedList(list_info):
    """Create a new forward linked list object and return it's head node.
    
    Args:
        list_info (list(printable)): The labels to display in the forward linked list's nodes.
    
    Returns:
        ForwardLinkedListNode: The head node objet for this forward linked list.
    """
    if len(list_info) == 0:
        return None
    head = ForwardLinkedListNode(list_info[0])
    cur_node = head
    for i in range(1, len(list_info)):
        cur_node.next = ForwardLinkedListNode(list_info[i])
        cur_node = cur_node.next
    return head


def parseDoublyLinkedList(list_info):
    """Create a new doubly linked list object and return it's head and tail node.
    
    Args:
        list_info (list(printable)): The labels to display in the doubly linked list's nodes.
    
    Returns:
        DoublyLinkedListNode, DoublyLinkedListNode: The head and tail node objects for this doubly linked list.
    """
    if len(list_info) == 0:
        return (None, None)
    head = DoublyLinkedListNode(list_info[0])
    cur_node, next_node = head, head
    for i in range(1, len(list_info)):
        next_node = DoublyLinkedListNode(list_info[i])
        cur_node.next = next_node
        next_node.prev = cur_node
        cur_node = cur_node.next
    return head, next_node
