# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 22:03
# @Author   : Merak
# @File     : binary_tree.py
# @Software : PyCharm
from typing import TypeVar, Generic
T = TypeVar('BinaryTree')


class BinaryTree(Generic[T]):
    def __init__(self, root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        if self.left_child is None:
            self.left_child = BinaryTree(new_node)
        else:
            temp = BinaryTree(new_node)
            temp.left_child = self.left_child
            self.left_child = temp.left_child
        return self.left_child

    def insert_right(self, new_code: T):
        if self.left_child is None:
            self.right_child = BinaryTree(new_code)
        else:
            temp = BinaryTree(new_code)
            temp.right_child = self.right_child
            self.right_child = temp.right_child
        return self.right_child

    def get_key(self):
        return self.key

    def set_key(self, root_obj):
        self.key = root_obj

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    def show_right_tree(self):
        print(self.key)
        if self.right_child is not None:
            print('|')
            self.right_child.show_right_tree()


if __name__ == '__main__':
    a = [1, 5, 6, 8, 0]

    bt = BinaryTree(-1)
    origin_bt = bt
    for i in a:
        bt = bt.insert_right(i)
    origin_bt.show_right_tree()
    bt.insert_left(bt)
