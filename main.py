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
    _fvq = interpolate.interp1d(ZVQ[:, 1], ZVQ[:, 2], kind='quadratic')

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
    def fvq(cls, xnew):  # kind指定插值方法，默认二次样条曲线插值
        ynew = cls._fvq(xnew)
        return ynew


def iteration():
    error = 0.1  # 允许误差
    q_rk = util.QIN
    T = q_rk.size
    (q_qs, q_ck, V, Z) = (0,  # 起始流量
                          np.zeros(T+1),  # 出库流量
                          np.zeros(T+1),  # 水库蓄水过程
                          np.zeros(T+1))  # 水位过程
    Z[0] = util.Z_fx
    V[0] = util.fzv(Z[0])
    for t in range(0, T-1):
        print("<DEBUG> time [{}]".format(t))
        Q_T = util.fzq(Z[t])  # 最大过流能力
        q_ck[t] = q_qs + Q_T  # 出库流量过程
        q_ck_2 = Q_T  # 初始化出库流量
        q_ck[t+1] = q_ck_2
        while True:
            v1 = util.fzv(Z[t])  # 水库蓄水量过程
            v2 = v1 + ((q_rk[t] + q_rk[t+1]) * util.DT / 2 - (q_ck[t] + q_ck[t+1]) * util.DT / 2)/10**8  # 水量平衡
            q_ck_new = util.fvq(v2)  # v查q
            if abs(q_ck_new-q_ck_2) > error:
                # print("<DEBUG> error [{}]".format(q_ck_new-q_ck_2))
                q_ck_2 = np.average([q_ck_new, q_ck_2])  # 初始化出库流量
            else:
                print("<DEBUG> q_rk[{}], q_ck [{}]".format(q_rk[t+1], q_ck_2))
                q_ck[t+1] = q_ck_2
                V[t+1] = v2
                Z[t+1] = util.fvz(v2)
                break
    # 画入库出库流量过程
    plt.plot(q_rk, '.-', label='In')
    inmax = (np.where(q_rk == np.max(q_rk))[0][0], np.max(q_rk))
    plt.plot(q_ck[:-2], 'r--', label='Out')
    omax = (np.where(q_ck == np.max(q_ck))[0][0], np.max(q_ck).round(1))
    plt.title("$In\\quad and\\quad Out(iterate)$")
    plt.xlabel("$T(\\Delta T=1h)$")
    plt.ylabel("$Q(m^3/s)$")
    plt.annotate("max{}".format(inmax), xy=inmax)
    plt.annotate("max{}".format(omax), xy=omax)
    plt.xlim(0)
    plt.legend()
    plt.grid()
    plt.show()
    # 画水位变化
    plt.plot(Z[:-1])
    plt.title("$Z$")
    plt.xlabel("$T$")
    plt.ylabel("$Z(m)$")
    zmax = (np.where(Z == np.max(Z))[0][0], np.max(Z).round(1))
    plt.annotate("max{}".format(zmax), xy=zmax)
    plt.xlim(0)
    plt.grid()
    plt.show()

# class Worker(object):
#     QIN = Utils.QIN
#     (Q_qs, Q_ck, V, Z) = (np.zeros(QIN.size),  # 起始流量
#                           np.zeros(QIN.size),  # 出库流量
#                           np.zeros(QIN.size),  # 水库蓄水过程
#                           np.zeros(QIN.size))  # 水位过程
#     Z[0] = Utils.Z_fx
#     Q_T = Utils.fzq(Z[0])  # 最大过流能力
#     Q_ck[0] = Q_qs[0] + Q_T  # 出库流量过程
#     V[0] = Utils.fzv(Z[0])  # 水库蓄水量过程
#
#     def __init__(self):
#         pass
#
#     def iteration(self):
#         pass
#
#     def half_figure(self):
#         pass
#
#     def plot(self):
#         pass


def half_figure():
    z, v, q = util.ZVQ[:, 0], util.ZVQ[:, 1], util.ZVQ[:, 2]
    y = v*10**8/util.DT+q/2
    # 散点图
    plt.scatter(y, q, label='scatter')
    # 插值
    fyq = interpolate.interp1d(y, q, 'quadratic')
    ynew = np.linspace(min(y), max(y), len(y)*100)
    qnew = fyq(ynew)
    plt.plot(ynew, qnew, 'g--', label='interpolate')
    # 拟合
    z1 = np.polyfit(y, q, 3)
    p1 = np.poly1d(z1)
    plt.plot(y, p1(y), 'r-', label='polyfit')
    # 调整图像
    plt.xlabel("$\\frac{V}{\\Delta t}+\\frac{q}{2}(m^3/s)$")
    plt.ylabel("$q(m^3/s)$")
    plt.title("$q-\\frac{V}{\\Delta t}+\\frac{q}{2}$")
    plt.legend()
    plt.grid()
    plt.show()

    # 计算，采用拟合图像
    q_rk = util.QIN
    T = q_rk.size
    (q_qs, q_ck, V, Z) = (0,  # 起始流量
                          np.zeros(T + 1),  # 出库流量
                          np.zeros(T + 1),  # 水库蓄水过程
                          np.zeros(T + 1))  # 水位过程
    Z[0] = util.Z_fx
    V[0] = util.fzv(Z[0])
    for t in range(0, T - 1):
        # print("<DEBUG> time [{}]".format(t))
        Q_T = util.fzq(Z[t])  # 最大过流能力
        q_ck[t] = q_qs + Q_T  # 出库流量过程
        y2 = np.average([q_rk[t], q_rk[t+1]]) - q_ck[t] + V[t] / util.DT + q_ck[t] / 2  # 计算右侧
        q2 = p1(y2)  # 查q2
        q_ck[t+1] = q2  # 放进结果
        V[t+1] = V[t] + ((q_rk[t] + q_rk[t+1]) * util.DT / 2 - (q_ck[t] + q_ck[t+1]) * util.DT / 2)/10**8  # 水量平衡
        Z[t+1] = util.fvz(V[t+1])  # 水位变化
    # 画水位变化
    plt.plot(Z[:-1])
    plt.title("$Z$")
    plt.xlabel("$T$")
    plt.ylabel("$Z(m)$")
    zmax = (np.where(Z == np.max(Z))[0][0], np.max(Z).round(1))
    plt.annotate("max{}".format(zmax), xy=zmax)
    plt.xlim(0)
    plt.grid()
    plt.show()
    # 画库容变化
    # plt.plot(V[:-1])
    # plt.title("$V$")
    # plt.xlabel("$T$")
    # plt.ylabel("$V(10^8m^3)$")
    # plt.grid()
    # plt.show()
    # 画入流出流过程线
    plt.plot(q_rk, '.-', label='In')
    inmax = (np.where(q_rk == np.max(q_rk))[0][0], np.max(q_rk))
    plt.plot(q_ck[:-2], 'r--', label='Out')
    omax = (np.where(q_ck == np.max(q_ck))[0][0], np.max(q_ck).round(1))
    plt.title("$In\\quad and\\quad Out(half-figure)$")
    plt.xlabel("$T(\\Delta T=1h)$")
    plt.ylabel("$Q(m^3/s)$")
    plt.annotate("max{}".format(inmax), xy=inmax)
    plt.annotate("max{}".format(omax), xy=omax)
    plt.xlim(0)
    plt.legend()
    plt.grid()
    plt.show()


def main():
    # iteration()
    half_figure()


if __name__ == "__main__":
    util = Utils()
    main()
