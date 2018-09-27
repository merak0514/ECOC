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
        print('输入的数据k有误（不能超过2^类数）')
        exit(1)
    choices_set = range(1, pow(2, c))
    choices = random.sample(choices_set, k)  # 随机挑选k个数字
    c_matrix = np.zeros((k, c))  # |新生成类|*|原始类|阶0/1矩阵
    for i in range(len(choices)):
        choice = choices[i]
        binary = bin(choice)[2:]
        c_matrix[i][:c-len(binary)] = 0  # 在二进制一开始部分补零
        for j in range(len(binary)):
            c_matrix[i][c-len(binary)+j] = binary[j]
    print(c_matrix)


choice_matrix([1, 2, 3], 5)
