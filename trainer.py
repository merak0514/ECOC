# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:03
# @Author   : Merak
# @File     : trainer.py
# @Software : PyCharm
import entropy
import numpy as np
from collections import defaultdict


def train(data: dict, data_size: int) -> None:
    # d = {0: [[1], [2]], 1: [[1], [2]]}
    print(data_size)
    print(data)
    origin_entropy = compute_entropy(data, data_size)
    print(origin_entropy)
    compute_node(data, nodes_num=8)
    pass


def tree_generate(data: dict, feature_usage: dict=None, max_usage: int=2, node=None):
    """
    :param data:
    :param feature_usage:
    :param node:
    :return:
    """
    if not feature_usage:  # 第一次初始化feature使用情况
        feature_usage = defaultdict(lambda: 0)
    pass


def compute_entropy(data: dict, m: int) -> float:
    """
    计算按照目前分类的熵
    :param data: 二维dict，第一维为此处分类，第二维为0/1
    :param m: 此data中的所有样本数
    :return: ent
    """
    # keys = data.keys()
    # ent = 0
    # for k in keys:
    cl_set = [len(data[0]), len(data[1])]
    ent = entropy.entropy(cl_set) * sum(cl_set) / m
    return ent


def compute_ent(l: list):
    l2 = [l.count(i) for i in set(l)]
    ent = entropy.entropy(l2)
    return ent


def compute_node(info: dict, nodes_num: int=2)->tuple:
    """
    返回选取的节点
    chosen_node 格式为 (feature_id, 取值, 熵)
    :param info: 一阶dict，key为0/1
    :param nodes_num: 可能选取的节点比例
    :return: chosen_node
    """
    data_set = []
    for i in info.values():
        data_set += i
    feature_num = len(data_set[0]) - 1  # 最后一项是最原始的分类
    m = len(data_set)  # 样本量
    if m <= nodes_num:
        nodes_num = input('invalid nodes_num; Please inout again: ')
    data_set = np.array(data_set)[:, :-1]  # 变为矩阵，裁剪最后附带的原始分类
    signs = []
    for sign in info.keys():
        signs += [sign] * len(info[sign])
    data_set = np.c_[data_set, signs]  # 附加标记（0/1），在最后一列
    break_length = m / (nodes_num + 1)  # 每隔这么长取一个点；此处m不知道是否应该使用 m+1 或者 m-1 代
    potential_nodes_index = [round(break_length * (i + 1)) for i in range(nodes_num)]  # 这个feature上所有可能的node_index
    # print('potential_nodes_index', potential_nodes_index)

    chosen_node = (-1, -1, -1)  # init
    for feature_id in range(feature_num):
        sorted_data = np.array(sorted(data_set, key=lambda s: s[feature_id]))
        # print('sorted_data', sorted_data)
        # potential_nodes = [sorted_data[i, feature_id] for i in potential_nodes_index]  # 根据先前计算出的index找值
        # print('potential_nodes', potential_nodes)
        chose_node = (-1, -1)  # init
        for potential_node_index in potential_nodes_index:  # 对于一个feature上每一个可能产生节点的点计算熵
            list_a = sorted_data[:potential_node_index, -1]  # 分支a，所有值为类别
            list_b = sorted_data[potential_node_index:, -1]  # 分支b
            ent = len(list_a) / m * compute_ent(list(list_a)) + len(list_b) / m * compute_ent(list(list_b))
            # print('ent', sorted_data[potential_node_index, feature_id], ent)
            if ent < chose_node[1] or chose_node[1] == -1:
                chose_node = (potential_node_index, ent)
        chose_node = (feature_id, sorted_data[chose_node[0], feature_id], chose_node[1])
        # print('chose_node', chose_node)
        if chose_node[2] < chosen_node[2] or chosen_node[2] == -1:
            chosen_node = chose_node

    print('chosen_node', chosen_node)
    return chosen_node


if __name__ == '__main__':
    # train(1)
    a = {
        0: [[0, 1, 5], [8, 2, 5], [10, 3, 5], [9, 8, 5], [1, 8, 5]],
        1: [[2, 6, 5], [9, 10, 5], [351, 20, 5], [2, 15, 5]],
        3: [[3, 2, 5], [8, 9, 5], [8, 105, 5]]
    }
    compute_node(a)
    pass
