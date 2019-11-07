# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import random


class Utils(object):
    Z_fx = 214  # 汛限水位
    Z_fg = 228  # 防洪高水位
    Z_sj = 229.63  # 设计洪水位
    Z_jx = 231.27  # 校核洪水位
    DT = 1 * 3600  # dt, 时段长1小时
    # 水库特性曲线资料
    ZVQ = np.array([
        [170,    4.79,   73],
        [170.78, 5.00,   120],
        [175,    6.51,   377],
        [177.5,  7.40,   593],
        [180,    8.46,   809],
        [183.63, 10.00,  948],
        [185,    10.71,  1000],
        [187.5,  12.00,  1080],
        [190,    13.39,  1160],
        [192.88, 15.00,  1241],
        [195,    16.20,  1300],
        [200,    19.63,  1426],
        [200.54, 20.00,  1439],
        [203,    21.88,  1496],
        [205,    23.40,  1542],
        [207.06, 25.00,  1586],
        [210,    27.60,  1650],
        [212.58, 30.00,  2269],
        [214,    31.60,  2610],
        [215,    32.50,  2850],
        [217.33, 35.00,  3948],
        [220,    38.01,  5207],
        [221.76, 40.00,  6320],
        [225,    44.15,  8370],
        [228,    48.00,  10719],
        [229.66, 50.47,  12019],
        [230,    50.98,  12285],
        [231.49, 53.20,  13666],
        [233,    55.49,  15065],
        [233.73, 56.60,  15065],
    ])
    # 入库流量过程
    QIN = np.array([
            634.6,     648.1,     681   ,    713.8 ,    746.7 ,    779.5 ,    812.4 ,    845.3 ,    878.1 ,   911    ,
            943.8 ,    976.7,     1009.5,    1164.9,    1442.7,    1720.6,    1998.4,    2276.3,    2554.2,    2832  ,
            3109.9,    3387.7,    3665.6,    3943.5,    4221.3,    4502.3,    4786.5,    5070.7,    5354.9,    5639.1,
            5923.3,    6207.5,    6491.7,    6775.9,    7060.1,    7344.3,    7628.4,    7711.6,    7593.6,    7475.7,
            7357.7,    7239.8,    7121.8,    7003.9,    6885.9,    6768  ,    6650  ,    6532.1,    6414.1,    6268.4,
            6095.1,    5921.7,    5748.4,    5575,      5401.6,    5228.3,    5054.9,    4881.5,    4708.2,    4534.8,
            4361.4,    4209.4,    4078.8,    3948.2,    3817.6,    3687  ,    3556.4,    3425.7,    3295.1,    3164.5,
            3033.9,    2903.3,    2772.7,    2678.1,    2619.5,    2560.9,    2502.3,    2443.7,    2385.2,    2326.6,
            2268  ,     2209.4,   2150.8,    2092.3,    2033.7,    1989.7,    1960.4,    1931.2,    1901.9,    1872.6
    ])

    _fzv = interpolate.interp1d(ZVQ[:, 0], ZVQ[:, 1], kind='quadratic')
    _fvz = interpolate.interp1d(ZVQ[:, 1], ZVQ[:, 0], kind='quadratic')
    _fzq = interpolate.interp1d(ZVQ[:, 0], ZVQ[:, 2], kind='quadratic')
    _fqz = interpolate.interp1d(ZVQ[:, 2], ZVQ[:, 0], kind='quadratic')

    @classmethod
    def fzv(cls, xnew):  # kind指定插值方法，默认二次样条曲线插值
            ynew = cls._fzv(xnew)
            return ynew

    @classmethod
    def fvz(cls, xnew):  # kind指定插值方法，默认二次样条曲线插值
        ynew = cls._fvz(xnew)
        return ynew

    @classmethod
    def fzq(cls, xnew):  # kind指定插值方法，默认二次样条曲线插值
        ynew = cls._fzq(xnew)
        return ynew

    @classmethod
    def fqz(cls, xnew):  # kind指定插值方法，默认二次样条曲线插值
        ynew = cls._fqz(xnew)
        return ynew


def iteration():
    QIN = Utils.QIN
    (Q_qs, Q_ck, V, Z) = (np.zeros(QIN.size),  # 起始流量
                          np.zeros(QIN.size),  # 出库流量
                          np.zeros(QIN.size),  # 水库蓄水过程
                          np.zeros(QIN.size))  # 水位过程
    Z[0] = Utils.Z_fx
    Q_T = Utils.fzq(Z[0])  # 最大过流能力
    Q_ck[0] = Q_qs[0] + Q_T  # 出库流量过程
    Q_ck_2 = random.randint(1, int(Q_ck[0]))
    V[0] = Utils.fzv(Z[0])  # 水库蓄水量过程
    while True:
        Q_ck_3 =

class Worker(object):
    QIN = Utils.QIN
    (Q_qs, Q_ck, V, Z) = (np.zeros(QIN.size),  # 起始流量
                          np.zeros(QIN.size),  # 出库流量
                          np.zeros(QIN.size),  # 水库蓄水过程
                          np.zeros(QIN.size))  # 水位过程
    Z[0] = Utils.Z_fx
    Q_T = Utils.fzq(Z[0])  # 最大过流能力
    Q_ck[0] = Q_qs[0] + Q_T  # 出库流量过程
    V[0] = Utils.fzv(Z[0])  # 水库蓄水量过程

    def __init__(self):
        pass

    def iteration(self):
        pass

    def half_figure(self):
        pass

    def plot(self):
        pass


def main():
    print(Utils.ZVQ)


if __name__ == "__main__":
    main()
