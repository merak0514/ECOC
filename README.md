# ECOC

## 简述
全称纠错输出码（Error Correcting Output Code），用于多分类MvM。
此处使用样本来自 [uci数据集](http://archive.ics.uci.edu/ml/machine-learning-databases/iris/bezdekIris.data')

## 常用记号：
* k：纠错输出码长度（选择矩阵的行数/新生成的分类器数量）
* c：原始类数（选择矩阵的列数）
* label：原始类名集合
## 基本步骤：
1. 数据导入

导入数据集，进行基本处理
`data_import.get_data(show=false)` 如果show的值为true，则会print部分数据。
0. 绘图观察


    plot.plot(data, label1=0, label2=1)

其中label1和label2为绘制横纵坐标对应的变量
1. 标记

把几个类联合起来进行标记，分为正反两类，正类为1，反类为-1。

* 先生成一个k*c的每行随机0/1不相同的选择矩阵choice_matrix

此处采用生成二进制不重复随机数的方法

    classifier.choice_matrix(label, k)
    c = len(label)
    
* 按照选择矩阵把原始类归到新类中，索引分别为0/1

    classifier.classifier(data, label, k)
    
返回: 分类后的新数据（包含k个dict的list，每个dict的key为0/1），和选择矩阵（作为之前分类的依据）。<br>
将此处选择矩阵的每一列中的0替换为-1后就是相应原始类的纠错输出码。

2. 循环
3. 对于每一个新类，进行训练分类