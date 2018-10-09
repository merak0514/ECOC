# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:03
# @Author   : Merak
# @File     : trainer.py
# @Software : PyCharm
import entropy


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


if __name__ == '__main__':
    # train(1)
    pass
