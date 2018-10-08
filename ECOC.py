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
import pymongo


class ECOC(object):
    class_names: list
    feature_names: list
    data_size: int
    origin_data: list
    sample_dict: dict

    def __init__(self):
        fixed_data = data_import.get_data(show=True)
        self.sample_dict = fixed_data[2]  # 以类名为key的dict
        self.origin_data = fixed_data[3]  # 原始数据，为二维list
        self.data_size = len(self.origin_data)  # 数据量
        self.feature_names = fixed_data[0]  # 所有的feature名字集合
        self.class_names = fixed_data[1]  # 所有的类名集合
        self.re_classified_data = []  # 所有的分类方案
        self.choice_matrix = []  # 选择矩阵

    def train_all(self, k: int):
        """
        :param k: 训练k个分类器
        :return:
        :rtype:
        """
        self.re_classified_data, self.choice_matrix = classifier.classifier(self.sample_dict, self.class_names, k, False)

        for cl in self.re_classified_data:
            for i in cl.values():
                print(len(i))
            trainer.train(cl, self.data_size)

    def plot(self, label1, label2):
        plot.plot(self.origin_data, label1, label2)

    def mongo(self):
        my_client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = my_client['ECOC']
        form1 = db['winequality-white']
        for data_id in range(len(self.origin_data)):
            feature = self.feature_names
            feature.append('rank')
            temp_dict = dict(zip(feature, self.origin_data[data_id]))
            temp_dict['_id'] = data_id
            form1.insert_one(temp_dict)


if __name__ == '__main__':

    e = ECOC()
    e.train_all(6)
    e.mongo()
