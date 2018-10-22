# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:56
# @Author   : Merak
# @File     : classifier.py
# @Software : PyCharm
import random
import numpy as np


def choice_matrix(label: list, k: int):
    """
    随机生成一个k*c阶每一行不相同的0/1矩阵，代表k种，其中每一种包含哪些类。
    :param label:
    :param k:
    :return: choice_matrix
    """
    c = len(label)  # 总类数
    if k >= pow(2, c):
        print('输入的数据k有误（不能超过2^类数/2）')
        exit(1)
    choices_set = range(1, pow(2, c-1))
    choices = random.sample(choices_set, k)  # 随机挑选k个数字
    c_matrix = np.zeros((k, c))  # |新生成类|*|原始类|阶0/1矩阵
    for i in range(len(choices)):
        choice = choices[i]
        binary = bin(choice)[2:]
        c_matrix[i][:c-len(binary)] = 0  # 在二进制一开始部分补零
        for j in range(len(binary)):
            c_matrix[i][c-len(binary)+j] = binary[j]
    return c_matrix


def new_class(data: dict, label: list, c_matrix: list) -> list:
    """
    :param data: 原始数据
    :param label: 标记
    :param c_matrix: 上方函数生成的0/1矩阵
    :return: re_classified_data
    """
    c = len(label)  # 总类数
    c_matrix = np.array(c_matrix)
    re_classified_data = []
    for choice in c_matrix:
        new_data = {0: [], 1: []}
        for i in range(c):
            la = label[i]
            b = choice[i]
            if b == 1:
                for datum in data[la]:
                    new_data[1].append(datum)
            elif b == 0:
                for datum in data[la]:
                    new_data[0].append(datum)
        re_classified_data.append(new_data)
    # print(re_classified_data[0])
    # input(1)

    return re_classified_data


def classifier(data: dict, label: list, k: int, show: bool = False, c_matrix=0) -> tuple:
    """
    :param data: 变为dict的数据，key为类名，value为此类包含的样本（list）
    :param label: 类的名字集合
    :param k: 需要重新生成的类数
    :param show:  是否展示
    :return: re_classified_data: 重新分类后的数据，为长度为k的list，每一项是一个key为0/1的dict, \
    其中0 和1 对应的值都是一个list，该list中的每一项为一条数据
    :return: c_matrix: choice_matrix 选择矩阵
    """
    if not c_matrix:
        c_matrix = choice_matrix(label, k)
    re_classified_data = new_class(data, label, list(c_matrix))
    if show is True:
        for i in re_classified_data:
            print(i)
            input('任意键继续')
    return re_classified_data, c_matrix

