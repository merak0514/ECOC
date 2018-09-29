# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:03
# @Author   : Merak
# @File     : trainer.py
# @Software : PyCharm
import entropy


def train(data):
    d = {'a': {0: [[1], [2]], 1: [[1], [2]]}, 'b': {0: [[1], [2]], 1: [[2]]}}
    origin_entropy = compute_entropy(d, 8)
    print(origin_entropy)


def compute_entropy(data, m):
    """
    计算按照目前分类的熵
    :param data: 二维dict，第一维为此处分类，第二维为0/1
    :type data: dict
    :param m: 此data中的所有样本数
    :type m: int
    :return:
    :rtype:
    """
    keys = data.keys()
    ent = 0
    for k in keys:
        cl_set = [len(data[k][0]), len(data[k][1])]
        ent -= entropy.entropy(cl_set) * sum(cl_set) / m
    return ent


if __name__ == '__main__':
    train(1)
