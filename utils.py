from scipy import interpolate
import numpy as np
import pandas as pd
import re
import sqlite3
import tqdm


# 插值计算
class Interpolate(object):
    @classmethod
    def inter1d(cls, x, y, xnew, kind='quadratic'):  # kind指定插值方法，默认二次样条曲线插值
        f = interpolate.interp1d(x, y, kind=kind)
        ynew = f(xnew)
        return ynew


class Reader(object):
    @classmethod
    def read(cls, file_path, sheet_name=0):
        file_type = re.split("\.", file_path)[-1]
        if file_type == 'csv':
            return cls.read_csv(file_path, sheet_name)
        elif file_type == 'xls' or file_type == 'xlsx':
            return cls.read_xls(file_path, sheet_name)
        else:
            return None

    @classmethod
    def read_csv(cls, file_path, sheet_name):
        df = pd.read_csv(file_path, sheet_name=sheet_name)
        data = np.array(df)
        return data

    @classmethod
    def read_xls(cls, file_path, sheet_name):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        data = np.array(df)
        return data


# 划分水文年
class Hydroyear(object):
    # example mons=4 mone=3
    def __init__(self, data, mons, mone):
        self.mons = mons  # 水文年起始月
        self.mone = mone  # 水文年终止月
        self.data = np.array(data)  # 流量数据
        self._rows = len(self.data)  # 多少年

    def split(self):
        left = self.data[:, :self.mone]  # 左半边表
        right = self.data[:, self.mons-1:]  # 右半边表

        line = np.hstack((right[-1, :], left[0, :]))  # 多余的一行
        tmp = np.hstack((right[:-1, :], left[1:, :]))  # 横向合并矩阵
        new = np.vstack((tmp, line))  # 纵向合并矩阵
        return new


# 年份、月份转化
class Calenear(object):
    @classmethod
    def to_cy(cls, mons, mone):
        res = [i for i in range(1, 13)]
        tmp = res[mons-1:]
        tmp.extend(res[:mone])
        return tmp


if __name__ == '__main__':
    conn = sqlite3.connect("hanjiang.db")
    cur = conn.cursor()

    data = np.loadtxt('F:\\college\\hwdcc2_design\\docs\\data2.txt')


    conn.commit()
    conn.close()

    print("hi")
