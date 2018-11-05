# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 11:45
# @Author   : Merak
# @File     : mongo.py
# @Software : PyCharm
import pymongo
import pymongo.errors


class Mongo:
    def __init__(self, client_name: str, db_name: str):
        self.client_name = client_name
        self.db_name = db_name
        self.db = pymongo.MongoClient(self.client_name)[self.db_name]

    def upload_choice_matrix(self, choice_matrix, form_name: str='choice_matrix'):
        if form_name not in self.db.collection_names():
            form = self.db[form_name]
            for choice_id in range(len(choice_matrix)):
                choice = choice_matrix[choice_id]
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

    def upload_train_data(self, data, feature_names, form_name: str):
        if form_name not in self.db.collection_names():
            form1 = self.db[form_name]
            for data_id in range(len(data)):
                feature = feature_names
                feature.append('rank')
                temp_dict = dict(zip(feature, data[data_id]))
                temp_dict['_id'] = data_id
                try:
                    form1.insert_one(temp_dict)
                except pymongo.errors.DuplicateKeyError:
                    pass
            print('Uploaded to mongo [Database {}, Form {}] successfully'.format(self.db_name, form_name))
        else:
            print('Form {} already exists'.format(form_name))

    def upload(self, data, form_name: str):
        if form_name not in self.db.collection_names():
            form1 = self.db[form_name]

            print('Uploaded to mongo [Database {}, Form {}] successfully'.format(self.db_name, form_name))

        else:
            print('Form {} already exists'.format(form_name))
