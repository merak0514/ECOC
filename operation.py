# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 20:31
# @Author   : Merak
# @File     : operation.py
# @Software : PyCharm

# 各种数学操作
import math
import numpy as np


def entropy(l: list) -> float:
    """
    计算熵
    :param l: 值为每一类的所有数据
    :return: ent
    """
    m = sum(l)
    ent = - sum(i / m * math.log(i / m, 2) for i in l)
    return ent


def compute_ent(l: list):
    l2 = [l.count(i) for i in set(l)]
    ent = entropy(l2)
    return ent


def compute_accuracy(data: list, max_class=None)->tuple:
    """
    返回所标记的类别和精确率
    :param: max_class: 可以强行指定此处标记的类别
    """
    label = [i[-1] for i in data]
    # print([str(i) for i in set(label)])
    label_dict = {i: label.count(i) for i in set(label)}
    if max_class is None:
        try:
            max_class = max(label_dict, key=label_dict.get)
        except ValueError:
            print(label_dict)
            print(label)
            input(1)
    try:
        accuracy = label_dict[max_class] / len(label)
    except KeyError:
        accuracy = 0
    return max_class, accuracy


def hold_out(data: list, show=False) -> tuple:
    """
    将原始数据集分为train, test, validation
    :param data:
    :param show:
    :return: （train_data, test_data, validation_data）
    """
    train_data = []
    test_data = []
    validation_data = []
    rate = [0.6, 0.2, 0.2]
    data = np.array(data)
    label = list(data[:, -1])
    label_dict = {i: label.count(i) for i in set(label)}
    used_label = {i: 0 for i in set(label)}
    np.random.shuffle(data)
    for i in data:
        sign = i[-1]
        if used_label[sign] < rate[0] * label_dict[sign]:
            train_data.append(i)
            used_label[sign] += 1
        elif used_label[sign] < (rate[0] + rate[1]) * label_dict[sign]:
            test_data.append(i)
            used_label[sign] += 1
        else:
            validation_data.append(i)
    if show is True:
        print('train', len(train_data))
        print('test', len(test_data))
        print('validation', len(validation_data))
    return train_data, test_data, validation_data


def hold_validation_data(data: list, show=False) -> tuple:
    """
    将原始数据集分为train, validation
    :param data:
    :param show:
    :return: （train_data, test_data, validation_data）
    """
    train_data = []
    validation_data = []
    rate = [0.7, 0.3]
    data = np.array(data)
    label = list(data[:, -1])
    label_dict = {i: label.count(i) for i in set(label)}
    used_label = {i: 0 for i in set(label)}
    np.random.shuffle(data)
    for i in data:
        sign = i[-1]
        if used_label[sign] < rate[0] * label_dict[sign]:
            train_data.append(i)
            used_label[sign] += 1
        else:
            validation_data.append(i)
    if show is True:
        print('train', len(train_data))
        print('validation', len(validation_data))
    return train_data, validation_data
