# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 20:23
# @Author   : Merak
# @File     : plot.py
# @Software : PyCharm
from matplotlib import pyplot as plt
import numpy as np


def plot(data: list, label1: int = 0, label2: int = 1) -> None:
    """
    输入数据以及要作为横纵坐标的两个标签
    """
    data = np.array(data)
    x1 = data[:, label1]  # 标记
    x2 = data[:, label2]
    T = data[:, -1]
    plt.scatter(x1, x2, s=5, c=T)
    plt.show()

