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
        self.node_info = root_obj
        self.left_child = None
        self.right_child = None
        self.is_leaf = False  # 若是是叶节点，则变为True; 叶节点没有分支

    def set_left(self, obj):
        self.left_child = obj

    def set_right(self, obj):
        self.right_child = obj

    def get_node_info(self):
        return self.node_info

    def set_node_info(self, root_obj):
        self.node_info = root_obj

    def set_leaf(self, is_leaf=True):
        self.is_leaf = is_leaf

    def compute_accuracy(self, accuracy_type: str='train_accuracy'):
        """
        计算训练集的精确度
        :param accuracy_type: node_info中的精确度的index
        :type accuracy_type:
        """
        return self.accuracy_computer(accuracy_type) / self.node_info['train_data_len']

    def accuracy_computer(self, accuracy_type: str):
        """
        别用这个，这是递归用的
        """
        if self.is_leaf is True:
            return self.node_info[accuracy_type] * self.node_info['train_data_len']
        else:
            return self.left_child.accuracy_computer(accuracy_type) + self.right_child.accuracy_computer(accuracy_type)

    def regenerate_tree(self):
        """
        原始训练得到的树进行简化，删除不需要的部分，只保留分割点的信息
        :return:
        :rtype:
        """
        if self.is_leaf is False:
            bt = BinaryTree(self.get_node_info()['break_info'])
            bt.set_left(self.left_child.regenerate_tree())
            bt.set_right(self.right_child.regenerate_tree())
        else:
            bt = BinaryTree(None)
        return bt

    def show_right_tree(self):
        """
        测试用
        """
        print(self.node_info)
        if self.right_child is not None:
            print('|')
            self.right_child.show_right_tree()


if __name__ == '__main__':
    # a = [1, 5, 6, 8, 0]
    #
    # bt = BinaryTree(-1)
    # origin_bt = bt
    # for i in a:
    #     bt = bt.insert_right(i)
    # origin_bt.show_right_tree()
    # bt.insert_left(bt)
    pass
