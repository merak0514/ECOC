# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 21:49
# @Author   : Merak
# @File     : data_import.py
# @Software : PyCharm

import csv
from collections import defaultdict


def get_data():
    """
    获得所有的数据
    :return: 返回 原始feature名称，分类集合，分类
    :rtype: tuple
    """
    path = 'data/winequality-white.csv'
    csv_file = open(path, 'r')
    reader = csv.reader(csv_file)

    classes = defaultdict(list)
    origin_data = []
    name_set = []
    for i in reader:
        if reader.line_num == 1:
            name_set = i
            continue
        datum = list(map(float, i))
        classes[int(datum[-1])].append(datum)
    class_names = list(classes.keys())
    print(list(classes.keys()))
    return name_set, class_names, classes
