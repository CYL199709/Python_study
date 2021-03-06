# coding:utf-8
# Algorithm:朴素贝叶斯

'''
数据集：中文手写数字
训练集数量：12000
测试集数量：3000
------------------------------
运行结果：
正确率：%
运行时长：s
'''

import numpy as np
import time
import cv2
import os
import random

class NaiveBayes:
    # 定义构造函数，feature_num为特征数，class_num为标签的所有可能取值。
    def __init__(self, feature_num, class_num):
        self.feature_num = feature_num
        self.class_num = class_num
        self.Py = 0
        self.Pxy = 0

    # 计算先验概率和条件概率，构建查找表。
    def fit(self, train_data, train_label):
        print("开始计算先验概率和条件概率")
        feature_num = self.feature_num
        class_num = self.class_num
        Py = np.zeros((class_num, 1))  # 定义大小为15*1的先验概率矩阵
        for i in range(class_num):
            Py[i] = (np.sum(train_label == i) + 1) / (len(train_label) + class_num)  # 计算先验概率，同时使用拉普拉斯平滑对计算结果为0的数据进行处理。
        Py = np.log(Py)  # 对计算结果取对数。避免在特征过多时，分子的连乘得到的结果太小导致数据向下溢出。

        xy_count = np.zeros((class_num, feature_num, 256))  # 定义条件计数数组，其大小为15*4096*256，用于计算条件概率。
        # 遍历每一个样本，根据label、feature、特征取值对数据进行计数。
        for i in range(len(train_label)):  # 遍历每一个训练集样本
            label = train_label[i]  # 选取样本标签
            data = train_data[i]  # 选取样本数据
            for j in range(feature_num):  # 遍历样本矩阵(1*4096)的所有列数据
                xy_count[label][j][data[j]] += 1  # 对每一个符合条件（标签、特征维度、特征取值）的样本进行计数

        Pxy = np.zeros((class_num, feature_num, 256))  # 定义条件概率矩阵
        # 遍历条件计数数组，计算条件概率。
        for i in range(class_num):
            for j in range(feature_num):
                for k in range(256):
                    Pxy[i][j][k] = np.log((xy_count[i][j][k] + 1) / (np.sum(
                        xy_count[i][j]) + 256))  # 计算条件概率，使用拉普拉斯平滑对计算结果为0的情况进行处理。同时对结果取对数，避免多个接近于0的值相乘导致结果向下溢出。

        self.Py = Py
        self.Pxy = Pxy
        print("结束计算概率")

    # 基于fit函数计算的先验概率及条件概率计算后验概率，对测试样本标签进行预测。
    def predict(self, test_data):
        print("开始预测标签")
        Py = self.Py
        Pxy = self.Pxy
        n = len(test_data)  # 计算test_data的样本数量
        feature_num = self.feature_num
        class_num = self.class_num

        predict_label = []  # 定义预测标签列表
        # 遍历每一个测试集样本
        for i in range(n):
            P_check = [0] * class_num  # 定义预测标签概率列表
            x = test_data[i]
            for j in range(class_num):  # 计算每一个标签对应的概率，并将结果保存在P_check列表中。
                sum = 0
                for k in range(feature_num):  # 对每一个维度出现样本数据的概率求和（因为是对数所以求和，如果不取对数则应该是相乘。朴素贝叶斯认为每一个特征维度是相互独立的。）
                    sum += Pxy[j][k][x[k]]
                P_check[j] = Py[j] + sum
            predict_label.append(P_check.index(max(P_check)))  # 将后验概率最大的标签值添加到预测标签列表predict_label中
            print('\r预测进度|%-50s| [%d/%d]' % ('█' * int((i / n) * 50 + 2), i + 1, n), end='')  # 绘制进度条
        print("\n结束预测")

        return np.array(predict_label)  # 返回预测标签列表

    # 计算朴素贝叶斯算法预测准确率
    def score(self, test_data, test_label):
        predict_label = np.mat(self.predict(test_data)).T
        test_label = np.mat(test_label).T
        m, n = np.shape(test_label)
        error = 0
        for i in range(m):
            if (predict_label[i] != test_label[i]):
                error += 1
        accuracy = 1 - (error / m)
        return accuracy

def file_name(file_dir):
  L=[]
  for root, dirs, files in os.walk(file_dir):
    for file in files:
      if os.path.splitext(file)[1] == '.jpg':
        L.append(os.path.join(root, file))
  return L

def load_data(files):
    file_label = file_name(files)
    data = []
    label = []
    for file in file_label:
        data_temp = cv2.imread(file,0)
        data.append(data_temp)
        label_temp = file.split("_")[3].split(".")[0]
        label.append(int(label_temp)-1)
    data = np.asarray(data)
    label = np.asarray(label)
    print(data.shape)
    return data,label



if __name__ == '__main__':
    """
    data_files = "data/"
    
    data, label = load_data(data_files)
    train_data = []
    train_label = []
    test_data = []
    test_label = []
    if not os.path.exists("train_index.npy"):
        print("create random index")
        train_index = random.sample(range(0,len(data)),int(len(data)*0.7))
        np.save("train_index.npy",train_index)
    else:
        print("load file----")
        train_index = np.load("train_index.npy")
    for i in range(len(data)):
        if i in train_index:
            train_data.append(data[i])
            train_label.append(label[i])
        else:
            test_data.append(data[i])
            test_label.append(label[i])
    np.save("train_data.npy",train_data)
    np.save("test_data.npy", test_data)
    np.save("train_label.npy", train_label)
    np.save("test_label.npy", test_label)
    """
    train_data = np.load("train_data.npy")
    train_label = np.load("train_label.npy")
    test_data = np.load("test_data.npy")
    test_label = np.load("test_label.npy")

    train_data = np.array([np.array(i).flatten() for i in train_data])  # 将64*64维矩阵转换为1*4096的矩阵。
    test_data = np.array([np.array(i).flatten() for i in test_data])
    nb = NaiveBayes(feature_num=64 * 64, class_num=15)  # 初始化NaiveBayes分类器
    start = time.time()
    nb.fit(train_data, train_label)  # 计算训练集先验概率和条件概率
    print("朴素贝叶斯预测准确率：%.2f%%" % (nb.score(test_data, test_label) * 100))
    end = time.time()
    print("耗时：%.2f s" % (end - start))
