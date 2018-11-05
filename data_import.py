# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 21:49
# @Author   : Merak
# @File     : data_import.py
# @Software : PyCharm

import csv
from collections import defaultdict
import operation as op


def get_data(show: bool = False) -> list:
    """
    获得所有的数据
    每一个class_names中的数字，均可以作为classes中的索引
    :param: show: 如果为true，则print数据，否则不显示
    :return: 返回 原始feature名称，分类集合，分类
    """
    path = 'data/winequality-white.csv'
    csv_file = open(path, 'r')
    reader = csv.reader(csv_file)

    classes = defaultdict(list)
    feature_name_set = []
    origin_data = []
    for i in reader:
        if reader.line_num == 1:
            feature_name_set = i
            continue
        datum = list(map(float, i))
        origin_data.append(datum)
    train_data, validation_data = op.hold_validation_data(origin_data)
    for datum in train_data:
        classes[int(datum[-1])].append(datum)
    class_names = list(classes.keys())
    if show is True:
        print('feature_name_set', feature_name_set)
        print('class_names', class_names)
        print('type of classes', type(classes))
        print('origin_data', origin_data[0])
        print('train_data', train_data[0])
        print('validation_data', validation_data[0])
    return [feature_name_set, class_names, classes, origin_data, train_data, validation_data]
