# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:56
# @Author   : Merak
# @File     : classifier.py
# @Software : PyCharm
import random
import numpy as np


def choice_matrix(label, k):
    """
    随机生成一个k*c阶每一行不相同的0/1矩阵，代表k种，其中每一种包含哪些类。
    :param label:
    :type label: list
    :param k:
    :type k: int
    :return:
    :rtype:
    """
    c = len(label)  # 总类数
    if k >= pow(2, c):
        print('输入的数据k有误（不能超过2^类数/2）')
        exit(1)
    choices_set = range(1, pow(2, c)/2)
    choices = random.sample(choices_set, k)  # 随机挑选k个数字
    choice_matrix = np.zeros((k, c))  # |新生成类|*|原始类|阶0/1矩阵
    for i in range(len(choices)):
        choice = choices[i]
        binary = bin(choice)[2:]
        choice_matrix[i][:c-len(binary)] = 0  # 在二进制一开始部分补零
        for j in range(len(binary)):
            choice_matrix[i][c-len(binary)+j] = binary[j]
    # print(c_matrix)
    return choice_matrix


def new_class(data, label, choice_matrix):
    """
    :param data: 原始数据
    :type data: dict
    :param label: 标记
    :type: list
    :param choice_matrix: 上方函数生成的0/1矩阵
    :type choice_matrix: list
    :return:
    :rtype:
    """
    c = len(label)  # 总类数
    choice_matrix = np.array(choice_matrix)
    re_classified_data = []
    for choice in choice_matrix:
        new_data = {0: [], 1: []}
        for i in range(c):
            l = label[i]
            b = choice[i]
            if b == 1:
                for datum in data[l]:
                    new_data[1].append(datum)
            elif b == 0:
                for datum in data[l]:
                    new_data[0].append(datum)

    return re_classified_data


choice_matrix([1, 2, 3], 5)
