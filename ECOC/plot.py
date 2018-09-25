# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 20:23
# @Author   : Merak
# @File     : plot.py
# @Software : PyCharm
from matplotlib import pyplot as plt
import numpy as np


def plot(data, label1, label2):
    """
    输入数据以及要作为横纵坐标的两个标签
    :param data:
    :type data: list
    :param label1:
    :type label1: int
    :param label2:
    :type label2: int
    """
    data = np.array(data)
    x1 = data[:, label1]  # 标记
    x2 = data[:, label2]
    T = data[:, -1]
    plt.scatter(x1, x2, s=5, c=T)
    plt.show()

