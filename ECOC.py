# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 19:44
# @Author   : Merak
# @File     : ECOC.py
# @Software : PyCharm
import data_import
import plot
import classifier


if __name__ == '__main__':
    fixed_data = data_import.get_data(show=True)
    feature_name_set = fixed_data[0]  # 所有的feature名字集合
    class_names = fixed_data[1]  # 所有的类名集合
    classes = fixed_data[2]  # 以类名为key的dict
    origin_data = fixed_data[3]  # 原始数据，为二维list
    # plot.plot(origin_data, 3, 8)
    classifier.classifier(classes, class_names, 6)
