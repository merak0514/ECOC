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
import pymongo.errors


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
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db_name = 'ECOC'

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
                print(self.choice_matrix)
                self.re_classified_data = classifier.classifier(
                    self.sample_dict, self.class_names, k, show=False, c_matrix=c_m)[0]
            else:
                form.drop()
                self.re_classified_data, self.choice_matrix = \
                    classifier.classifier(self.sample_dict, self.class_names, k, False)
        else:
            self.re_classified_data, self.choice_matrix = \
                classifier.classifier(self.sample_dict, self.class_names, k, False)
        self.mongo()

        for cl in self.re_classified_data:
            # for i in cl.values():
            #     print(len(i))
            trainer.train(cl, self.data_size)
            break

    def plot(self, label1, label2):
        plot.plot(self.origin_data, label1, label2)

    def mongo(self):
        """
        上传到mongo数据库
        """
        form_name = 'winequality-white'
        db = self.client[self.db_name]
        if form_name not in db.collection_names():
            form1 = db[form_name]
            for data_id in range(len(self.origin_data)):
                feature = self.feature_names
                feature.append('rank')
                temp_dict = dict(zip(feature, self.origin_data[data_id]))
                temp_dict['_id'] = data_id
                try:
                    form1.insert_one(temp_dict)
                except pymongo.errors.DuplicateKeyError:
                    pass
                else:
                    print('Upload failed')
                    return 1
            print('Uploaded to mongo [Database {}, Form {}] successfully'.format(self.db_name, form_name))
        else:
            print('Form {} already exists'.format(form_name))

        form_name = 'choice_matrix'
        if form_name not in db.collection_names():
            form = db[form_name]
            for choice_id in range(len(self.choice_matrix)):
                choice = self.choice_matrix[choice_id]
                temp_dict = {
                    '_id': choice_id,
                    'choice': ','.join([str(i) for i in choice])
                }
                try:
                    form.insert_one(temp_dict)
                except pymongo.errors.DuplicateKeyError:
                    pass
            print('Uploaded to mongo [Database {}, Form {}] successfully'.format(self.db_name, form_name))
        else:
            print('Form {} already exists'.format(form_name))


if __name__ == '__main__':

    e = ECOC()
    e.train_all(7)
    # e.mongo()
