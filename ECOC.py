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
import operation as op
import pymongo
import pymongo.errors
import mongo


class ECOC(object):
    class_names: list
    feature_names: list
    data_size: int
    origin_data: list
    sample_dict: dict

    def __init__(self):
        fixed_data = data_import.get_data(show=False)
        self.sample_dict = fixed_data[2]  # 以类名为key的dict
        self.origin_data = fixed_data[3]  # 原始数据，为二维list
        self.feature_names = fixed_data[0]  # 所有的feature名字集合
        self.class_names = fixed_data[1]  # 所有的类名集合
        self.train_data = fixed_data[4]  # 训练集
        self.validation_data = fixed_data[5]  # 验证集
        self.data_size = len(self.train_data)  # 数据量
        self.re_classified_data = []  # 所有的分类方案
        self.choice_matrix = []  # 选择矩阵
        self.client_name = 'mongodb://localhost:27017/'
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db_name = 'ECOC'
        self.tree_set = []

    def train_all(self, k: int):
        """
        :param k: 训练k个分类器
        :return:
        """
        db = self.client[self.db_name]
        self.choice_matrix = []
        if 'choice_matrix' in db.collection_names():  # 若数据库中已经存在choice_matrix
            form = db['choice_matrix']
            c_m = list(form.find())
            if len(c_m) == k:  # 若是k未更新
                for i in c_m:
                    choice = [float(m) for m in i['choice'].split(',')]
                    self.choice_matrix.append(choice)
                self.re_classified_data = classifier.classifier(
                    self.sample_dict, self.class_names, k, show=False, c_matrix=self.choice_matrix)[0]
            else:
                form.drop()
                self.re_classified_data, self.choice_matrix = \
                    classifier.classifier(self.sample_dict, self.class_names, k, False)
        else:
            self.re_classified_data, self.choice_matrix = \
                classifier.classifier(self.sample_dict, self.class_names, k, False)
        print(self.choice_matrix)
        self.mongo()

        print(self.class_names)
        # 开始训练
        for cl in self.re_classified_data:
            data_tuple = op.hold_out(cl)
            bt, accuracy = trainer.train(data_tuple, self.data_size)  # 得到一棵b_tree
            self.tree_set.append((bt, accuracy))
            # break

        self.validate()

    def plot(self, label1, label2):
        plot.plot(self.train_data, label1, label2)

    def mongo(self):
        m = mongo.Mongo(self.client_name, self.db_name)
        m.upload_train_data(self.origin_data, self.feature_names, 'winequality-white_origin')
        m.upload_train_data(self.train_data, self.feature_names, 'winequality-white_train')
        m.upload_train_data(self.validation_data, self.feature_names, 'winequality-white_validation')
        m.upload_choice_matrix(self.choice_matrix)

    def validate(self):
        op.validate(self.tree_set, self.validation_data, self.choice_matrix, self.class_names)


if __name__ == '__main__':

    e = ECOC()
    e.train_all(10)
