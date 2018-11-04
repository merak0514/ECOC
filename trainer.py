# !/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 16:03
# @Author   : Merak
# @File     : trainer.py
# @Software : PyCharm
import entropy
import numpy as np
from collections import defaultdict
import binary_tree


def train(data_tuple: tuple, data_size: int) -> None:
    train_data = data_tuple[0]
    test_data = data_tuple[1]
    validation_data = data_tuple[2]
    print(data_size)
    # print(train_data)
    l = np.array(train_data)[:, -1]
    origin_entropy = compute_ent(list(l))
    print('origin_entropy: ', origin_entropy)
    bt = tree_generate(train_data, test_data, max_usage=3, node_num=7)
    print('accuracy', bt.compute_accuracy())
    b_tree = bt.regenerate_tree()
    # raise Exception  # 强行报错，使用pycharm自带的debug看内存
    # compute_node(train_data, nodes_num=8)
    return b_tree


def tree_generate(train_data: list, test_data: list, feature_usage: dict=None, max_usage: int=2, node_num=7):
    """
    :param train_data: 训练集
    :param test_data: 测试集
    :param feature_usage: 所有的feature的使用情况
    :param max_usage: 每个feature可以使用的最大次数
    :param node_num: 最大可供选择的节点数，默认为7
    :return: bt 返回一棵树
    """
    disabled_features = []
    if not feature_usage:  # 第一次初始化feature使用情况
        feature_usage = defaultdict(lambda: 0)
    else:  # 构造 disabled list
        for i, j in feature_usage.items():
            if j >= max_usage:
                disabled_features.append(i)
    test_chosen_class, test_accuracy = compute_accuracy(test_data)
    print('accuracy', test_accuracy)

    # 该节点信息
    print('length', len(train_data))
    chosen_class, accuracy = compute_accuracy(train_data)
    node_info = {
        'train_data_len': len(train_data),
        'class': chosen_class,
        'train_accuracy': accuracy,
        'test_accuracy': test_accuracy,
    }
    bt = binary_tree.BinaryTree(node_info)

    if len(train_data) <= node_num or accuracy == 1 or test_accuracy == 1:  # 数据量小于要产生可能分叉点的量，返回
        bt.set_leaf()  # 标记为叶节点
        # bt.set_right(0)
        print('无法继续分支，标记为叶节点')
        return bt

    break_info = compute_node(train_data, disabled_features, nodes_num=7)
    bt.node_info['break_info'] = break_info

    chosen_feature = break_info[0]
    break_num = break_info[1]
    feature_usage[chosen_feature] += 1

    train_data_left = []
    train_data_right = []
    for datum in train_data:
        if datum[chosen_feature] < break_num:
            train_data_left.append(datum)
        else:
            train_data_right.append(datum)
            
    test_data_left = []
    test_data_right = []
    for datum in test_data:
        if datum[chosen_feature] < break_num:
            test_data_left.append(datum)
        else:
            test_data_right.append(datum)

    if not test_data_left or not test_data_right:
        # 测试集用完标记为叶节点
        bt.set_leaf()  # 标记为叶节点
        # bt.set_right(1)
        print('测试集为空，标记为叶节点')
        return bt

    # 计算标记的类，在下方测试集上强行标记
    train_left_chosen_class, train_left_accuracy = compute_accuracy(train_data_left)
    train_right_chosen_class, train_right_accuracy = compute_accuracy(train_data_right)

    test_left_chosen_class, test_left_accuracy = compute_accuracy(test_data_left, max_class=train_left_chosen_class)
    test_right_chosen_class, test_right_accuracy = compute_accuracy(test_data_right, max_class=train_right_chosen_class)

    # 加权计算得到的测试集上的综合准确率
    mixed_accuracy = (len(test_data_left) * test_left_accuracy + len(test_data_right) * test_right_accuracy) / \
                     (len(test_data_right) + len(test_data_left))

    print('mixed_accuracy', mixed_accuracy)

    if (mixed_accuracy > test_accuracy) or (len(train_data) > 100)\
            or (mixed_accuracy >= test_accuracy and len(train_data_right) > 30):  # 预剪枝
        feature_usage_left = defaultdict(lambda: 0)
        for i, j in feature_usage.items():
            feature_usage_left[i] = j
        feature_usage_right = defaultdict(lambda: 0)
        for i, j in feature_usage.items():
            feature_usage_right[i] = j
        print('剪枝')
        bt.set_right(tree_generate(train_data_right, test_data_right, feature_usage_right, max_usage))
        bt.set_left(tree_generate(train_data_left, test_data_left, feature_usage_left, max_usage))
        return bt
    else:
        bt.set_leaf()  # 标记为叶节点
        # bt.set_right(2)
        print('不能减少准确度，标记为叶节点')
        return bt


def compute_ent(l: list):
    l2 = [l.count(i) for i in set(l)]
    ent = entropy.entropy(l2)
    return ent


def compute_node(info: list, disabled_features: list=[], nodes_num: int=2)->tuple:
    """
    返回选取的节点
    chosen_node 格式为 (feature_id, 取值, 熵)
    :param info: list
    :param disabled_features: 未启用的 features
    :param nodes_num: 可能选取的节点比例
    :return: chosen_node
    """
    feature_num = len(info[0]) - 2
    m = len(info)
    if m <= nodes_num:
        nodes_num = input('invalid nodes_num; Please input again: ')
    data_set = np.array(info)
    print('ent before chosen: ', compute_ent(list(data_set[:, -1])))

    break_length = m / (nodes_num + 1)  # 每隔这么长取一个点；此处m不知道是否应该使用 m+1 或者 m-1 代
    potential_nodes_index = [round(break_length * (i + 1)) for i in range(nodes_num)]  # 这个feature上所有可能的node_index
    # print('potential_nodes_index', potential_nodes_index)

    chosen_node = (-1, -1, -1)  # init
    for feature_id in range(feature_num):
        if feature_id in disabled_features:
            continue
        sorted_data = np.array(sorted(data_set, key=lambda s: s[feature_id]))
        potential_nodes = [sorted_data[i, feature_id] for i in potential_nodes_index]  # 根据先前计算出的index找值
        # print('potential_nodes', potential_nodes)
        chose_node = (-1, -1)  # init
        for potential_node in potential_nodes:  # 对于一个feature上每一个可能产生节点的点计算熵
            list_a = list(i[-1] for i in data_set if i[feature_id] < potential_node)
            list_b = list(i[-1] for i in data_set if i[feature_id] >= potential_node)
            ent = len(list_a) / m * compute_ent(list_a) + len(list_b) / m * compute_ent(list_b)
            if ent < chose_node[1] or chose_node[1] == -1:
                chose_node = (potential_node, ent)
        chose_node = (feature_id, chose_node[0], chose_node[1])
        # print('chose_node', chose_node)
        if chose_node[2] < chosen_node[2] or chosen_node[2] == -1:
            chosen_node = chose_node
    print('chosen_node', chosen_node)
    return chosen_node


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


if __name__ == '__main__':
    a = [[1], [1], [1], [2], [2]]
    print(compute_accuracy(a))
    pass
