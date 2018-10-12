# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:03
# @Author   : Merak
# @File     : trainer.py
# @Software : PyCharm
import entropy
import numpy as np


def train(data: dict, data_size: int) -> None:
    d = {'a': {0: [[1], [2]], 1: [[1], [2]]}, 'b': {0: [[1], [2]], 1: [[2]]}}
    print(data_size)
    origin_entropy = compute_entropy({0: data}, data_size)  # 按照compute_entropy的要求多套一层
    print(origin_entropy)


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


def compute_node(info: dict):
    """
    :param info: 一阶dict，key为0/1
    :return:
    """
    data_set = []
    for i in info.values():
        data_set += i
    feature_num = len(data_set[0]) - 1  # 最后一项是最原始的分类
    data_set = np.array(data_set)[:, :-1]  # 变为矩阵
    print(data_set)
    signs = []
    for sign in info.keys():
        signs += [sign] * len(info[sign])
    print(signs)
    data_set = np.c_[data_set, signs]  # 附加标记，在最后一列
    # print(data_set)
    # print(feature_num)
    for feature in range(feature_num):

        break





if __name__ == '__main__':
    # train(1)
    a = {
        'a': [[0, 1], [1, 2]],
        'b': [[5, 6], [9, 10]]
    }
    compute_node(a)
    pass
