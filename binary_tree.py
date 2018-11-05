# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 22:03
# @Author   : Merak
# @File     : binary_tree.py
# @Software : PyCharm
import operation as op


class BinaryTree(object):
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

    def compute_accuracy(self, key: str='accuracy') -> float:
        """
        计算训练集的精确度
        :param key: node_info中的精确度的index
        """
        return self.accuracy_computer(key) / self.node_info['data_len']

    def accuracy_computer(self, key: str):
        """
        别用这个，这是递归用的
        """
        if self.is_leaf is True:
            return self.node_info[key] * self.node_info['data_len']
        else:
            return self.left_child.accuracy_computer(key) + self.right_child.accuracy_computer(key)

    def regenerate_tree(self):
        """
        原始训练得到的树进行简化，删除不需要的部分，只保留分割点的信息
        :return:树
        :rtype:
        """
        if self.is_leaf is False:
            bt = BinaryTree({
                'break_info': self.node_info['break_info'][0: 2],
                'class': self.node_info['class']
            })
            bt.set_left(self.left_child.regenerate_tree())
            bt.set_right(self.right_child.regenerate_tree())
        else:
            bt = BinaryTree({
                'class': self.node_info['class']
            })
            bt.set_leaf()
        return bt

    def apply_data(self, data_list):
        self.node_info['data_len'] = len(data_list)
        if self.is_leaf is False:
            # 非叶节点向下递归
            break_info = self.node_info['break_info']
            feature = break_info[0]
            value = break_info[1]
            left = []
            right = []
            for datum in data_list:
                # 分类
                if datum[feature] < value:
                    left.append(datum)
                else:
                    right.append(datum)
            self.left_child.apply_data(left)
            self.right_child.apply_data(right)
        else:
            # 叶节点计算accuracy
            accuracy = op.compute_accuracy(data_list, max_class=self.node_info['class'])[1]
            self.node_info['accuracy'] = accuracy

    def decide(self, datum: list) -> float:
        """
        确定输入的一条数据所属的类。
        :param datum:
        :return:
        """
        current_tree = self
        while current_tree.is_leaf is False:
            break_info = current_tree.node_info['break_info']
            feature = break_info[0]
            value = break_info[1]
            if datum[feature] < value:
                current_tree = current_tree.left_child
            else:
                current_tree = current_tree.right_child
        return current_tree.node_info['class']


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
