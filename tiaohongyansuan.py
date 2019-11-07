import sqlite3
import numpy as np
from src.utils import Interpolate
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interpolate


def work5():
    cur.execute("SELECT day,des5,des02,des01 from flood_des")
    data = np.array(cur.fetchall())
    days, des5, des02, des01 = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    cur.execute("SELECT des5 FROM ap3")
    des5 = np.array(cur.fetchall()).flatten()
    cur.execute("SELECT z,v,a,q from zvaq")
    data = np.array(cur.fetchall())
    z, v = data[:, 0], data[:, 1]
    fzv = interpolate.interp1d(z, v)
    fvz = interpolate.interp1d(v, z)
    safedown = 15000
    # z_lim = 150.24
    z_lim = 150.24
    v_lim = fzv(z_lim)
    hours = np.array([i % 24 for i in range(0, 15*24)])
    daytime = np.array([pd.datetime.strftime(dt, '%m-%d-%H:%M')
                        for dt in pd.date_range('19640925', '19641009',
                                                periods=361)])
    x = np.arange(0, days.size)
    xnew = np.linspace(x.min(), x.max(), days.size*24)
    f5 = interpolate.interp1d(x, des5)
    ynew = f5(xnew)
    avein = np.array([0 if i == 0 else np.average(ynew[i-1:i+1]) for i in range(0, ynew.size)])
    qout = []
    dv, v = [], [float(v_lim), ]
    # mode->计算模式，0-->下游防洪标准 1--> 设计洪水 2-->校核洪水
    for i, y in enumerate(ynew):
        tmp = 0
        if i < list(ynew).index(ynew.max()):  # 洪峰之前
            if y < safedown:
                qout.append(y)
            else:
                qout.append(safedown)  # 蓄水
                tmp = (y-safedown)*3600/10**8
        else:
            qout.append(safedown)
            tmp = (y - safedown)*3600/10**8
        dv.append(tmp)
        v.append(v[i] + dv[i])
    ave_qout = np.array([0 if i==0 else np.average(qout[i-1:i+1]) for i in range(0, xnew.size)])
    z = np.array([float(fvz(i)) for i in v])
    v = np.array(v)
    dv = np.array(dv)
    qout = np.array(qout)
    result = np.hstack(([[float('%.2f' % i), ] for i in ynew],
                        [[float('%.2f' % i), ] for i in avein],
                        [[float('%.2f' % i), ] for i in qout],
                        [[float('%.2f' % i), ] for i in ave_qout],
                        [[float('%.2f' % i), ] for i in v[1:]],
                        [[float('%.2f' % i), ] for i in dv],
                        [[float('%.2f' % i), ] for i in z[1:]],
                        [[i, ] for i in daytime[:-1]]))
    df = pd.DataFrame(result)
    df.to_csv('hssj1.csv')
    # cur.executemany("INSERT INTO flood_cal5(time,qin,qin_ave,qout,qout_ave,v,dv,z)"
    #                 "VALUES(?,?,?,?,?,?,?,?)", result)
    # cur.executemany("update flood_cal5 set qin=?,qin_ave=?,qout=?,qout_ave=?,v=?,dv=?,z=?"
    #                 "where time=?", result)
    # 流量
    plt.plot(xnew, ynew, label='in')
    plt.plot(xnew, qout, '--', label='out')
    plt.xlabel('$t(h)$')
    plt.ylabel("$Q(m^3/s)$")
    plt.legend()
    plt.show()
    # 水位
    plt.plot(xnew, z[1:])
    maxz = z[1:].max()
    maxz_x = [xnew[list(z[1:]).index(maxz)] for i in range(2)]
    maxz_ys = np.linspace(150, maxz, 2)
    # plt.arrow(maxz_x, maxz, 0, maxz-150)
    plt.plot(maxz_x, maxz_ys, '--')
    plt.text(10, 152, '$155.65m$')
    plt.xlabel("$t$")
    plt.ylabel("$Z(m)$")
    plt.ylim(150, 157)
    # plt.xlim(0, 14)
    # plt.legend()
    plt.show()


def work02():
    cur.execute("SELECT day,des5,des02,des01 from flood_des")
    data = np.array(cur.fetchall())
    days, des5, des02, des01 = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    cur.execute("SELECT des02 FROM ap3")
    des02 = np.array(cur.fetchall()).flatten()
    cur.execute("SELECT z,v,a,q from zvaq")
    data = np.array(cur.fetchall())
    z, v, a, qmax = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    fzv = interpolate.interp1d(z, v)
    pvz = np.polyfit(v, z, 3)
    fvz = np.poly1d(pvz)
    # fvz = interpolate.interp1d(v, z)
    # fzqmax = interpolate.interp1d(z, qmax)
    pzqmax = np.polyfit(z, qmax, 3)
    fzqmax = np.poly1d(pzqmax)
    safedown = 15000
    z_lim = 150.24
    v_lim = fzv(z_lim)
    hours = np.array([i % 24 for i in range(0, 15*24)])
    daytime = np.array([pd.datetime.strftime(dt, '%m-%d-%H:%M')
                        for dt in pd.date_range('19640925', '19641009',
                                                periods=361)])
    x = np.arange(0, days.size)
    xnew = np.linspace(x.min(), x.max(), days.size*24)
    f02 = interpolate.interp1d(x, des02)
    ynew = f02(xnew)
    avein = np.array([0 if i == 0 else np.average(ynew[i-1:i+1]) for i in range(0, ynew.size)])
    qout = []
    dv, v, z = [], [float(v_lim), ], [fvz(v_lim), ]
    for i, y in enumerate(ynew):
        tmp = 0
        if i < list(ynew).index(ynew.max()):  # 洪峰之前
            if y < safedown:
                qout.append(y)
            else:
                qout.append(safedown)  # 蓄水
                tmp = (y-safedown)*3600/10**8
        else:
            if z[i] >= 155.65:
                if y > safedown:
                    qoutmax = fzqmax(fvz(v[i]))
                    qout.append(qoutmax)
                    tmp = (y - qoutmax)*3600/10**8
                else:
                    qout.append(safedown)
                    tmp = (y-safedown)*3600/10**8
            else:
                qout.append(safedown)
                tmp = (y - safedown) * 3600 / 10 ** 8
        dv.append(tmp)
        v.append(v[i] + dv[i])
        z.append(float(fvz(v[i] + dv[i])))
    ave_qout = np.array([0 if i==0 else np.average(qout[i-1:i+1]) for i in range(0, xnew.size)])
    v = np.array(v)
    z = np.array(z)
    dv = np.array(dv)
    qout = np.array(qout)
    result = np.hstack(([['%.2f' % i, ] for i in ynew],
                        [['%.2f' % i, ] for i in avein],
                        [['%.2f' % i, ] for i in qout],
                        [['%.2f' % i, ] for i in ave_qout],
                        [['%.2f' % i, ] for i in v[1:]],
                        [['%.2f' % i, ] for i in dv],
                        [['%.2f' % i, ] for i in z[1:]],
                        [[i, ] for i in daytime[:-1]]))
    df = pd.DataFrame(result)
    df.to_csv('hssj2.csv')
    # cur.executemany("INSERT INTO flood_cal02(time,qin,qin_ave,qout,qout_ave,v,dv,z)"
    #                 "VALUES(?,?,?,?,?,?,?,?)", result)
    # cur.executemany("update flood_cal02 set qin=?,qin_ave=?,qout=?,qout_ave=?,v=?,dv=?,z=?"
    #                 "where time=?", result)
    # 流量
    print(fzqmax(fvz(183.23)))
    plt.plot(xnew, ynew, label='in')
    plt.plot(xnew, qout, '--', label='out')
    plt.xlabel('$t(h)$')
    plt.ylabel("$Q(m^3/s)$")
    plt.legend()
    plt.show()
    # 水位
    plt.plot(xnew, z[1:])
    maxz = z[1:].max()
    maxz_x = [xnew[list(z[1:]).index(maxz)] for i in range(2)]
    maxz_ys = np.linspace(150, maxz, 2)
    # plt.arrow(maxz_x, maxz, 0, maxz-150)
    plt.plot(maxz_x, maxz_ys, '--')
    plt.text(9, 152, '$157.72m$')
    plt.xlabel("$t$")
    plt.ylabel("$Z(m)$")
    plt.ylim(150, 158)
    plt.xlim(0, 14)
    # plt.legend()
    plt.show()


def work01():
    cur.execute("SELECT day,des5,des02,des01 from flood_des")
    data = np.array(cur.fetchall())
    days, des5, des02, des01 = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    cur.execute("SELECT des01 FROM ap3")
    des01 = np.array(cur.fetchall()).flatten()
    cur.execute("SELECT z,v,a,q from zvaq")
    data = np.array(cur.fetchall())
    z, v, a, qmax = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    fzv = interpolate.interp1d(z, v)
    pvz = np.polyfit(v, z, 3)
    fvz = np.poly1d(pvz)
    print(fvz(0))
    # fvz = interpolate.interp1d(v, z)
    # fzqmax = interpolate.interp1d(z, qmax)
    pzqmax = np.polyfit(z, qmax, 3)
    fzqmax = np.poly1d(pzqmax)
    safedown = 15000
    z_lim = 150.24
    v_lim = fzv(z_lim)
    hours = np.array([i % 24 for i in range(0, 15*24)])
    daytime = np.array([pd.datetime.strftime(dt, '%m-%d-%H:%M')
                        for dt in pd.date_range('19640925', '19641009',
                                                periods=361)])
    x = np.arange(0, days.size)
    xnew = np.linspace(x.min(), x.max(), days.size*24)
    f01 = interpolate.interp1d(x, des01)
    ynew = f01(xnew)
    avein = np.array([0 if i == 0 else np.average(ynew[i-1:i+1]) for i in range(0, ynew.size)])
    qout = []
    dv, v, z = [], [float(v_lim), ], [fvz(v_lim), ]
    for i, y in enumerate(ynew):
        tmp = 0
        if z[i] >= 155.65:
            if z[i] >= 157.72:
                qoutmax = fzqmax(fvz(v[i])) + 10000
                qout.append(qoutmax)
                tmp = (y - qoutmax) * 3600 / 10 ** 8
            else:
                if y > safedown:
                    qoutmax = fzqmax(fvz(v[i]))
                    qout.append(qoutmax)
                    tmp = (y - qoutmax)*3600/10**8
                else:
                    qout.append(safedown)
                    tmp = (y-safedown)*3600/10**8
        else:
            if y < safedown:
                qout.append(y)
            else:
                qout.append(safedown)  # 蓄水
                tmp = (y - safedown) * 3600 / 10 ** 8
        print(z[i])
        dv.append(tmp)
        v.append(v[i] + dv[i])
        z.append(float(fvz(v[i] + dv[i])))
    ave_qout = np.array([0 if i==0 else np.average(qout[i-1:i+1]) for i in range(0, xnew.size)])
    v = np.array(v)
    z = np.array(z)
    dv = np.array(dv)
    qout = np.array(qout)
    result = np.hstack(([['%.2f' % i, ] for i in ynew],
                        [['%.2f' % i, ] for i in avein],
                        [['%.2f' % i, ] for i in qout],
                        [['%.2f' % i, ] for i in ave_qout],
                        [['%.2f' % i, ] for i in v[1:]],
                        [['%.2f' % i, ] for i in dv],
                        [['%.2f' % i, ] for i in z[1:]],
                        [[i, ] for i in daytime[:-1]]))
    df = pd.DataFrame(result)
    df.to_csv('hssj3.csv')
    # cur.executemany("INSERT INTO flood_cal02(time,qin,qin_ave,qout,qout_ave,v,dv,z)"
    #                 "VALUES(?,?,?,?,?,?,?,?)", result)
    cur.executemany("update flood_cal01 set qin=?,qin_ave=?,qout=?,qout_ave=?,v=?,dv=?,z=?"
                    "where time=?", result)
    # 流量
    print(fzqmax(fvz(196.19)))
    plt.plot(xnew, ynew, label='in')
    plt.plot(xnew, qout, '--', label='out')
    plt.xlabel('$t(h)$')
    plt.ylabel("$Q(m^3/s)$")
    plt.legend()
    plt.show()
    # 水位
    plt.plot(xnew, z[1:])
    maxz = z[1:].max()
    maxz_x = [xnew[list(z[1:]).index(maxz)] for i in range(2)]
    maxz_ys = np.linspace(150, maxz, 2)
    # plt.arrow(maxz_x, maxz, 0, maxz-150)
    plt.plot(maxz_x, maxz_ys, '--')
    plt.text(9, 152, '$157.72m$')
    plt.xlabel("$t$")
    plt.ylabel("$Z(m)$")
    plt.ylim(150, 160)
    plt.xlim(0, 14)
    # plt.legend()
    plt.show()


if __name__ == "__main__":
    conn = sqlite3.connect("hanjiang.db")
    cur = conn.cursor()

    work5()
    work02()
    work01()

    conn.commit()
    conn.close()
