# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:03
# @Author   : Merak
# @File     : trainer.py
# @Software : PyCharm
import entropy
import numpy as np
from collections import defaultdict
import binary_tree


def train(data: list, data_size: int) -> None:
    # d = {0: [[1], [2]], 1: [[1], [2]]}
    print(data_size)
    print(data)
    l = np.array(data)[:, -1]
    origin_entropy = compute_ent(list(l))
    # origin_entropy = compute_entropy(data, data_size)
    print('origin_entropy: ', origin_entropy)
    tree_generate(data, max_usage=2)
    # compute_node(data, nodes_num=8)
    pass


def tree_generate(data: list, feature_usage: dict=None, max_usage: int=2, node=None):
    """
    :param data:
    :param feature_usage:
    :param max_usage:
    :param node:
    :return:
    """
    disabled_features = []
    if not feature_usage:  # 第一次初始化feature使用情况
        feature_usage = defaultdict(lambda: 0)
    else:  # 构造 disabled list
        for i, j in feature_usage.items():
            if j >= max_usage:
                disabled_features.append(i)

    bt = binary_tree.BinaryTree(data)
    break_info = compute_node(data, disabled_features, nodes_num=7)
    chosen_feature = break_info[0]
    break_num = break_info[1]
    feature_usage[chosen_feature] += 1

    # sorted_data = sorted(data, key=lambda s: s[chosen_feature])
    data_left = []
    data_right = []
    for datum in data:
        if datum[chosen_feature] < break_num:
            data_left.append(datum)
        else:
            data_right.append(datum)

    tree_generate(data_right, feature_usage, max_usage)
    # tree_generate(data_left, feature_usage, max_usage)



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


def compute_node(info: list, disabled_features: list=[], nodes_num: int=2)->tuple:
    """
    返回选取的节点
    chosen_node 格式为 (feature_id, 取值, 熵)
    :param info: 一阶dict，key为0/1
    :param disabled_features: 未启用的 features
    :param nodes_num: 可能选取的节点比例
    :return: chosen_node
    """
    feature_num = len(info[0]) - 2
    m = len(info)
    if m <= nodes_num:
        nodes_num = input('invalid nodes_num; Please input again: ')
    data_set = np.array(info)
    print('ent before chosen: ', compute_ent(list(data_set[:, -1])))
    print('ds', data_set[:, -1])
    print('dsl', len(data_set[:, -1]))

    break_length = m / (nodes_num + 1)  # 每隔这么长取一个点；此处m不知道是否应该使用 m+1 或者 m-1 代
    potential_nodes_index = [round(break_length * (i + 1)) for i in range(nodes_num)]  # 这个feature上所有可能的node_index
    # print('potential_nodes_index', potential_nodes_index)

    chosen_node = (-1, -1, -1)  # init
    chosen_b = []
    for feature_id in range(feature_num):
        if feature_id in disabled_features:
            continue
        sorted_data = np.array(sorted(data_set, key=lambda s: s[feature_id]))
        # print('sorted_data', sorted_data)
        potential_nodes = [sorted_data[i, feature_id] for i in potential_nodes_index]  # 根据先前计算出的index找值
        # print('potential_nodes', potential_nodes)
        chose_node = (-1, -1)  # init
        for potential_node in potential_nodes:  # 对于一个feature上每一个可能产生节点的点计算熵
            list_a = list(i[-1] for i in data_set if i[feature_id] < potential_node)
            list_b = list(i[-1] for i in data_set if i[feature_id] >= potential_node)
            # list_a = list(sorted_data[:potential_node_index, -1])  # 分支a，所有值为类别
            # list_b = list(sorted_data[potential_node_index:, -1])  # 分支b
            ent = len(list_a) / m * compute_ent(list_a) + len(list_b) / m * compute_ent(list_b)
            # print('ent', sorted_data[potential_node_index, feature_id], ent)
            if ent < chose_node[1] or chose_node[1] == -1:
                chose_node = (potential_node, ent)
                chose_a = list_a
                chose_b = list_b
        chose_node = (feature_id, chose_node[0], chose_node[1])
        # print('chose_node', chose_node)
        if chose_node[2] < chosen_node[2] or chosen_node[2] == -1:
            chosen_node = chose_node
            chosen_b = chose_b
            chosen_a = chose_a
    # print('a', compute_ent(list_a))
    print('b', compute_ent(chosen_b))
    print('rent', len(chosen_a) / m * compute_ent(chosen_a) + len(chosen_b) / m * compute_ent(chosen_b))
    if compute_ent(chosen_b) < 3:
        print('b', chosen_b)
        print('bl', len(chosen_b))
        print('a', chosen_a)
        # print('data', sorted_data)
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
