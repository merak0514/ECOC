# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:03
# @Author   : Merak
# @File     : trainer.py
# @Software : PyCharm
# Todo: 增加compute_node的验证（nodes_num < len(data)）
import entropy
import numpy as np


def train(data: dict, data_size: int) -> None:
    # d = {'a': {0: [[1], [2]], 1: [[1], [2]]}, 'b': {0: [[1], [2]], 1: [[2]]}}
    # print(data_size)
    # origin_entropy = compute_entropy({0: data}, data_size)  # 按照compute_entropy的要求多套一层
    # print(origin_entropy)
    pass


def compute_entropy(data: dict, m: int) -> float:
    """
    计算按照目前分类的熵
    :param data: 二维dict，第一维为此处分类，第二维为0/1
    :param m: 此data中的所有样本数
    :return: ent
    """
    keys = data.keys()
    ent = 0
    for k in keys:
        cl_set = [len(data[k][0]), len(data[k][1])]
        ent -= entropy.entropy(cl_set) * sum(cl_set) / m
    return ent


def compute_ent(l: list):
    l2 = [l.count(i) for i in set(l)]
    ent = entropy.entropy(l2)
    return ent



def compute_node(info: dict, nodes_num: int=2):
    """
    :param info: 一阶dict，key为0/1
    :param nodes_num: 可能选取的节点比例
    :return:
    """
    data_set = []
    for i in info.values():
        data_set += i
    feature_num = len(data_set[0]) - 1  # 最后一项是最原始的分类
    m = len(data_set)  # 样本量
    data_set = np.array(data_set)[:, :-1]  # 变为矩阵，裁剪最后附带的原始分类
    # print('data_set', data_set)
    signs = []
    for sign in info.keys():
        signs += [sign] * len(info[sign])
    data_set = np.c_[data_set, signs]  # 附加标记（0/1），在最后一列
    print('data_set', data_set)
    break_length = m / (nodes_num + 1)  # 每隔这么长取一个点；此处m不知道是否应该使用 m+1 或者 m-1 代
    potential_nodes_index = [round(break_length * (i + 1)) for i in range(nodes_num)]  # 这个feature上所有可能的node_index
    print('potential_nodes_index', potential_nodes_index)
    for feature_id in range(feature_num):
        sorted_data = np.array(sorted(data_set, key=lambda s: s[feature_id]))
        value_set = data_set[:, feature_id]
        value_set.sort()  # 排序
        print('sorted_data', sorted_data)
        for potential_node_index in potential_nodes_index:
            list_a = sorted_data[:potential_node_index, -1]  # 分支a
            list_b = sorted_data[potential_node_index:, -1]  # 分支b
            print(list_b)
            ent = len(list_a) / m * compute_ent(list(list_a)) + len(list_b) / m * compute_ent(list(list_b))
            print('ent', potential_node_index, ent)

        print('value_set', value_set)
        potential_nodes = [value_set[i] for i in potential_nodes_index]  # 根据先前计算出的index找值
        print('potential_nodes', potential_nodes)


        break



if __name__ == '__main__':
    # train(1)
    a = {
        0: [[0, 1], [8, 2], [10, 3], [9, 8], [1, 8], [2, 15]],
        1: [[2, 6], [9, 10], [351, 20]]
    }
    compute_node(a)
    pass
