from entity.pixelpair import PixelPair as PP
from typing import List


class Threshold:
    def __init__(self, pp_list: List[PP], lc_list: List[int], **kwargs):
        self.m = kwargs["m"]
        self.lc_list = lc_list

    def get_threshold(self, j) -> int:
        N = len(self.lc_list)
        for n in range(0, max(self.lc_list) + 2):
            if self.compute_sum_of_LC_with_thereshold(n) / N >= (j + 1) / self.m:
                return n

    def compute_sum_of_LC_with_thereshold(self, n: int) -> int:
        sum = 0
        for item in self.lc_list:
            if item < n:
                sum += 1
        return sum

    def get_all_thereshold(self) -> List[int]:
        result = []
        for j in range(self.m-1):
            result.append(self.get_threshold(j))
        return result

    @property
    def LC(self):
        return self.lc_list
