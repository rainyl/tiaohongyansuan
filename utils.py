from scipy import interpolate


# 插值计算
class Interpolate(object):
    @classmethod
    def inter1d(cls, x, y, xnew, kind='quadratic'):  # kind指定插值方法，默认二次样条曲线插值
        f = interpolate.interp1d(x, y, kind=kind)
        ynew = f(xnew)
        return ynew


if __name__ == '__main__':
    print("hi")
