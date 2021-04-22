# -*- coding: utf-8 -*-
# @Date  : 2020/5/23
# @Author: Luokun
# @Email : olooook@outlook.com

import numpy as np


class DecisionTree:
    """
    Decision tree classifier(决策树分类器，ID3生成算法)
    """

    def __init__(self, rate: float = 0.95):
        self.rate, self.tree = rate, None

    def fit(self, X: np.ndarray, Y: np.ndarray):
        indices = np.arange(X.shape[0])  # 所有行索引
        features = np.arange(X.shape[1])  # 所有列索引
        self.tree = self._create_tree(X, Y, indices, features)

    def __call__(self, X: np.ndarray):
        Y = np.zeros([len(X)], dtype=int)  # 输出变量
        for i, x in enumerate(X):
            Y[i] = self._predict(self.tree, x)
        return Y

    def _predict(self, node, x):
        if isinstance(node, dict):  # 如果节点是树(字典)类型
            feature, trees = node['feature'], node['trees']
            return self._predict(trees[x[feature]], x)  # 根据值进行下一次递归
        return node  # 如果节点是叶子类型则直接返回该值

    def _create_tree(self, X, Y, indices, features):
        c, rate = self._select_class(X, Y, indices)  # 获得数量最多的类别及其频率
        if len(features) == 0 or rate > self.rate:  # 无特征可分或者满足一定的单一性
            return c  # 返回最单一的类别
        f = self._select_feature(X, Y, indices, features)  # 选择香农熵最小的特征
        trees = {}
        features_ = features[features != f]  # 除去选择的特征
        for v in np.unique(X[indices, f]).tolist():  # 为该特征的每一个取值都建立子树
            indices_ = self._query_indices(X, Y, indices, f, v)
            trees[v] = self._create_tree(X, Y, indices_, features_)  # 递归构建子决策树
        return {'feature': f, 'trees': trees}

    @staticmethod
    def _calc_entropy(X, Y, indices):  # 计算经验熵
        prob = np.bincount(Y[indices]) / len(indices)  # 采用二进制计数法，x必须为正整数向量
        prob = prob[prob != 0]  # 除去0概率
        return np.sum(prob * -np.log(prob))  # 经验熵

    @staticmethod
    def _query_indices(X, Y, indices, feature, value):
        return indices[X[indices, feature] == value]

    @staticmethod
    def _select_class(X, Y, indices):
        prob = np.bincount(Y[indices]) / len(indices)  # 计算类别频率
        c = np.argmax(prob)
        return c, prob[c]  # 返回出现次数最多的类别，以及其频率

    @classmethod
    def _calc_cond_entropy(cls, X, Y, indices, feature):  # 计算条件熵
        cond_ent = 0  # 经验条件熵
        for v in np.unique(X[indices, feature]):
            indices_ = cls._query_indices(X, Y, indices, feature, v)
            cond_ent += len(indices_) / len(indices) * cls._calc_entropy(X, Y, indices_)
        return cond_ent  # 条件熵

    @classmethod
    def _calc_info_gain(cls, X, Y, indices, feature):  # 计算信息增益
        ent = cls._calc_entropy(X, Y, indices)  # 经验熵
        cond_ent = cls._calc_cond_entropy(X, Y, indices, feature)  # 经验条件熵
        return ent - cond_ent  # 信息增益

    @classmethod
    def _select_feature(cls, X, Y, indices, features):
        gains = np.array([
            cls._calc_info_gain(X, Y, indices, f) for f in features
        ])  # 计算features中所有特征的信息增益
        return features[np.argmax(gains)]  # 返回信息增益最大的特征


def load_data():
    x = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 1, 1], [0, 1, 1],
                  [1, 0, 0], [1, 0, 0], [1, 0, 1], [1, 0, 1], [1, 1, 0], [1, 1, 0], [1, 1, 1], [1, 1, 1]])
    y = np.where(x.sum(axis=1) >= 2, 1, 0)
    return x, y


if __name__ == '__main__':
    x, y = load_data()

    decision_tree = DecisionTree(rate=0.95)
    decision_tree.fit(x, y)
    pred = decision_tree(x)

    print(decision_tree.tree)
    print(y)
    print(pred)

    acc = np.sum(pred == y) / len(pred)
    print(f'Accuracy = {100 * acc:.2f}%')