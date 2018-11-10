# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 20:31
# @Author   : Merak
# @File     : operation.py
# @Software : PyCharm

# 各种数学操作
import math
import numpy as np
import binary_tree


def entropy(l: list) -> float:
    """
    计算熵
    :param l: 值为每一类的所有数据
    :return: ent
    """
    m = sum(l)
    ent = - sum(i / m * math.log(i / m, 2) for i in l)
    return ent


def compute_ent(l: list):
    l2 = [l.count(i) for i in set(l)]
    ent = entropy(l2)
    return ent


def compute_accuracy(data: list, max_class=None)->tuple:
    """
    返回所标记的类别和精确率
    :param: max_class: 可以强行指定此处标记的类别
    """
    label = [i[-1] for i in data]
    # print([str(i) for i in set(label)])
    label_dict = {i: label.count(i) for i in set(label)}
    if max_class is None:
        try:
            max_class = max(label_dict, key=label_dict.get)
        except ValueError:
            print(label_dict)
            print(label)
            input(1)
    try:
        accuracy = label_dict[max_class] / len(label)
    except KeyError:
        accuracy = 0
    return max_class, accuracy


def hold_out(data: list, show=False) -> tuple:
    """
    将原始数据集分为train, test, validation
    :param data:
    :param show:
    :return: （train_data, test_data, validation_data）
    """
    train_data = []
    test_data = []
    validation_data = []
    rate = [0.6, 0.2, 0.2]
    data = np.array(data)
    label = list(data[:, -1])
    label_dict = {i: label.count(i) for i in set(label)}
    used_label = {i: 0 for i in set(label)}

    np.random.shuffle(data)

    for i in data:
        sign = i[-1]
        if used_label[sign] < rate[0] * label_dict[sign]:
            train_data.append(i)
            used_label[sign] += 1
        elif used_label[sign] < (rate[0] + rate[1]) * label_dict[sign]:
            test_data.append(i)
            used_label[sign] += 1
        else:
            validation_data.append(i)
    if show is True:
        print('train', len(train_data))
        print('test', len(test_data))
        print('validation', len(validation_data))
    return train_data, test_data, validation_data


def hold_validation_data(data: list, show=False) -> tuple:
    """
    将原始数据集分为train, validation
    :param data:
    :param show:
    :return: （train_data, test_data, validation_data）
    """
    train_data = []
    validation_data = []
    rate = [0.7, 0.3]
    data = np.array(data)
    label = list(data[:, -1])
    label_dict = {i: label.count(i) for i in set(label)}
    used_label = {i: 0 for i in set(label)}

    np.random.shuffle(data)

    for i in data:
        sign = i[-1]
        if used_label[sign] < rate[0] * label_dict[sign]:
            train_data.append(i)
            used_label[sign] += 1
        else:
            validation_data.append(i)
    if show is True:
        print('train', len(train_data))
        print('validation', len(validation_data))
    return train_data, validation_data


def validate(tree_set: list, validation_data, choice_matrix, classes_names):
    tree: binary_tree.BinaryTree
    choice_matrix = np.array(choice_matrix)

    correct = []
    correct2 = []
    average_bias = 0
    for datum in validation_data:
        distances = []
        distances2 = []
        datum_choice = []  # 计算出的选择，需要计算与选择矩阵每一列的距离，找出距离最小的
        datum_choice2 = []  # 计算出的选择，带有权重

        for tree, weight in tree_set:
            datum_choice.append(tree.decide(datum))
            if weight < 0.6:  # 原始树的正确率过低则直接设置为不判定
                datum_choice2.append(0)
            else:
                datum_choice2.append(tree.decide(datum))

        for i in range(np.size(choice_matrix, 1)):
            choice = choice_matrix[:, i]

            distance = np.sum(np.abs(choice - datum_choice))
            distance2 = np.sum(np.abs(choice - datum_choice2))

            distances.append(distance)
            distances2.append(distance2)

        chosen_class = round(classes_names[distances.index(min(distances))])
        chosen_class2 = round(classes_names[distances2.index(min(distances2))])

        # print(datum_choice)
        # print(distances)
        # print(datum)
        # print(chosen_class)
        # input(1)

        if chosen_class == datum[-1]:
            correct.append(1)
        else:
            correct.append(0)
            average_bias += abs(chosen_class - datum[-1])

        if chosen_class2 == datum[-1]:
            correct2.append(1)
        else:
            correct2.append(0)
        # print('datum', datum)
        # print('chosen_class', chosen_class)

    average_bias = average_bias / len(correct)

    print(sum(correct))
    print(len(correct))
    accuracy = sum(correct) / len(correct)
    accuracy2 = sum(correct2) / len(correct2)
    print('accuracy', accuracy)
    print('accuracy2', accuracy2)
    print('average_bias', average_bias)
