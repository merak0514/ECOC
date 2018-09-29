# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17:58
# @Author   : Merak
# @File     : entropy.py
# @Software : PyCharm
import math


def entropy(l):
    """
    计算熵
    :param l: 值为每一类的所有数据
    :type l: list
    :return:
    :rtype:
    """
    m = sum(l)
    ent = sum(-i / m * math.log(i, 2) for i in l)
    return ent
