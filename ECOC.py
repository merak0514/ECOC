# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 19:44
# @Author   : Merak
# @File     : ECOC.py
# @Software : PyCharm
import data_import
import plot
import classifier
import trainer


class ECOC(object):
    def __init__(self):
        fixed_data = data_import.get_data(show=True)
        self.sample_dict = fixed_data[2]  # 以类名为key的dict
        self.origin_data = fixed_data[3]  # 原始数据，为二维list
        self.feature_names = fixed_data[0]  # 所有的feature名字集合
        self.class_names = fixed_data[1]  # 所有的类名集合
        self.re_classified_data = []  # 所有的分类方案
        self.choice_matrix = []  # 选择矩阵

    def train_all(self, k):
        """
        :param k: 训练k个分类器
        :type k: int
        :return:
        :rtype:
        """
        self.re_classified_data, self.choice_matrix = classifier.classifier(self.sample_dict, self.class_names, k, True)
        for cl in self.re_classified_data:
            trainer.train(cl)

    def plot(self, label1, label2):
        plot.plot(self.origin_data, label1, label2)


if __name__ == '__main__':

    e = ECOC()
    e.train_all(6)
