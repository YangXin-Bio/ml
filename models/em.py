# -*- coding: utf-8 -*-
# @Date  : 2020/5/27
# @Author: Luokun
# @Email : olooook@outlook.com

import numpy as np


class SimpleEM:
    """
    Expectation-maximization algorithm(期望最大算法,三硬币模型)
    """

    def __init__(self, prob: list, max_iter=100):
        self.prob, self.max_iter = np.array(prob), max_iter
        self.Y, self.N = None, 0

    def fit(self, Y: np.ndarray):
        self.Y = Y
        for _ in range(self.max_iter):
            mu = self._expect()
            self._maximize(mu)

    def _expect(self):  # E步
        p1, p2, p3 = self.prob
        a = p1 * (p2 ** self.Y) * ((1 - p2) ** (1 - self.Y))
        b = (1 - p1) * (p3 ** self.Y) * ((1 - p3) ** (1 - self.Y))
        return a / (a + b)

    def _maximize(self, mu):  # M步
        self.prob[0] = np.sum(mu) / len(self.Y)
        self.prob[1] = np.sum(mu * self.Y) / np.sum(mu)
        self.prob[2] = np.sum((1 - mu) * self.Y) / np.sum(1 - mu)

# EM算法与高斯混合模型可参见./gmm.py
