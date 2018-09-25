# ECOC

## 简述
全称纠错输出码（Error Correcting Output Code），用于多分类MvM。
此处使用样本来自 [uci数据集](http://archive.ics.uci.edu/ml/machine-learning-databases/iris/bezdekIris.data')

## 基本步骤：
0. 绘图观察
1. 数据导入
导入数据集，进行基本处理
1. 标记
把几个类联合起来进行标记，分为正反两类，正类为1，反类为-1
把标记后的类分别记为
code_word: list: 标记每个原始class被分到哪个code  e.g.[{1: -1, 2: 1, 3: -1, 4: -1}, ...]
new_class: list: 按照上面的划分把所有的数据划分到1、0（代替-1）两个标记中去  e.g.[{1: (data), 0: (data)}, ...]

2. 循环
3. 对于每一个新类，进行训练分类