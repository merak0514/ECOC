# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:56
# @Author   : Merak
# @File     : classifier.py
# @Software : PyCharm
import random
import numpy as np
import time


def choice_matrix(label, k):
    """
    随机生成一个k*c阶每一行不相同的0/1矩阵，代表k种，其中每一种包含哪些类。
    :param label:
    :type label: list
    :param k:
    :type k: int
    :return: choice_matrix
    :rtype: list
    """
    c = len(label)  # 总类数
    if k >= pow(2, c):
        print('输入的数据k有误（不能超过2^类数/2）')
        exit(1)
    choices_set = range(1, pow(2, c-1))
    choices = random.sample(choices_set, k)  # 随机挑选k个数字
    choice_matrix = np.zeros((k, c))  # |新生成类|*|原始类|阶0/1矩阵
    for i in range(len(choices)):
        choice = choices[i]
        binary = bin(choice)[2:]
        choice_matrix[i][:c-len(binary)] = 0  # 在二进制一开始部分补零
        for j in range(len(binary)):
            choice_matrix[i][c-len(binary)+j] = binary[j]
    print(choice_matrix)
    return choice_matrix


def new_class(data, label, choice_matrix):
    """
    :param data: 原始数据
    :type data: dict
    :param label: 标记
    :type: list
    :param choice_matrix: 上方函数生成的0/1矩阵
    :type choice_matrix: list
    :return: re_classified_data
    :rtype:list
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
        re_classified_data.append(new_data)

    return re_classified_data


def classifier(data, label, k):
    """
    :param data: 变为dict的数据，key为类名，value为此类包含的样本（list）
    :type data: dict
    :param label: 类的名字集合
    :type label: list
    :param k: 需要重新生成的类数
    :type k: int
    :return: re_classified_data: 重新分类后的数据，为长度为k的list，每一项是一个key为0/1的list
    :rtype: list
    :return: c: choice_matrix 选择矩阵
    :rtype: list
    """
    c = choice_matrix(label, k)
    re_classified_data = new_class(data, label, c)
    return re_classified_data, c
    # for i in re_classified_data:
    #     print(i)
    #     input(1)
    # print(re_classified_data)



