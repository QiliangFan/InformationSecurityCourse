from typing import List
from math import floor


class PixelPair:
    def __init__(self, *args, **kwargs):
        """
        xi : the i of pixel on the left
        xj : the j of pixel on the left
        yi : the i of pixel on the right
        yj : the j of pixel on the right
        """
        self.xi = int(kwargs["xi"])
        self.xj = int(kwargs["xj"])
        self.yi = int(kwargs["yi"])
        self.yj = int(kwargs["yj"])
        self._x = int(kwargs["x"])
        self._y = int(kwargs["y"])

    def compute_ex_ey(self, *args) -> tuple:
        """
        the order of PPs:
        up -> down -> left -> right
        :return (ex, ey)
        """
        v1, v2 = args[0].x, args[0].y
        v7, v8 = args[1].x, args[1].y
        v3, v4 = args[2].x, args[2].y
        v5, v6 = args[3].x, args[3].y
        px_ = (v2 + v5 + v8 + (v1 + v4 + v7) / 3) / 4
        py_ = (v1 + v4 + v7 + (v2 + v5 + v8) / 3) / 4
        px = floor((v1 + v4 + v7 + px_) / 4)
        py = floor((v2 + v5 + v8 + py_) / 4)
        ex = self.x - px
        ey = self.y - py
        return ex, ey

    def compute_LC(self, *args) -> int:
        """
        the order of PPs:
        top -> down and  left -> right
        :param args:
        :return: LC:int
        """
        v1, v2 = args[0].x, args[0].y
        v3, v4 = args[1].x, args[2].y
        v5, v6 = args[0].x, args[0].y
        w1, w2 = args[0].x, args[0].y
        v7, v8 = args[0].x, args[0].y
        w3, w4 = args[0].x, args[0].y
        w5, w6 = args[0].x, args[0].y
        w7, w8 = args[0].x, args[0].y
        w9, w10 = args[0].x, args[0].y
        delta = self.abs_delta
        lc_x_y = delta(v1, v2) + delta(v3, v4) + delta(v5, v6) \
                 + delta(w1, w2) + delta(w2, v7) + delta(v7, v8) \
                 + delta(v8, w3) + delta(w3, w4) + delta(w5, w6) \
                 + delta(w6, w7) + delta(w7, w8) + delta(w8, w9) \
                 + delta(w9, w10) + delta(v3, w1) + delta(w1, w5) \
                 + delta(v4, w2) + delta(w2, w6) + delta(v7, w7) \
                 + delta(v8, w8) + delta(v5, w3) + delta(w3, w9) \
                 + delta(v6, w4) + delta(w4, w10)
        return lc_x_y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @staticmethod
    def abs_delta(x: int, y: int) -> int:
        return abs(x - y)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    __repr__ = __str__
