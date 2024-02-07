import math

from Transformation.ExtendedPattern import ExtendedPattern
from Transformation.Pattern import Pattern
from data_processor import Matcher


class TransformationSetEval:
    def __init__(self, tables, item, transformation_list, swap_src_target):
        self.tables = tables
        self.item = item
        self.transformation_list = transformation_list
        assert type(transformation_list) == list
        self.swap_src_target = swap_src_target

        self._rows = None
        self.is_swapped = None
        self._pat_inp = None
        self._inp_pat = None
        self._inputs = None

    @property
    def rows(self):
        if self._rows is None:
            self._rows, self.is_swapped = Matcher.get_matching_rows_golden(
                                           self.tables, self.item, swap_src_target=self.swap_src_target)
        return self._rows

    @property
    def inp_pat(self):
        if self._inp_pat is None:
            self._init_inp_pat()
        return self._inp_pat

    @property
    def pat_inp(self):
        if self._pat_inp is None:
            self._init_inp_pat()
        return self._pat_inp

    @property
    def covered(self):
        return sum(1 for p in self.inp_pat if len(p) > 0)

    @property
    def coverage(self):
        return float(self.covered) / len(self.inp_pat)


    def best_pattern_covered(self, n=1):
        if len(self.pat_inp) < n:
            return math.nan
        return sorted([len(pat) for pat in self.pat_inp], reverse=True)[n-1]
        # return max(len(pat) for pat in self.pat_inp)

    @property
    def best_pattern_coverage(self):
        return float(self.best_pattern_covered()) / len(self.inp_pat)


    def kth_pattern_coverage(self, k):
        return float(self.best_pattern_covered(k)) / len(self.inp_pat)


    def get_transformation_coverage(self, pattern):
        inputs = []
        for inp, outs in self.rows.items():
            for out in outs:
                inputs.append((inp, out))


        cnt = 0
        for inp_idx, inp in enumerate(inputs):
            if type(pattern) is Pattern:
                if pattern.apply(inp[0]) == inp[1]:
                    cnt += 1
            elif type(pattern) is ExtendedPattern:  # @TODO: This is not the best way to measure coverage
                outs = pattern.apply(inp[0])
                if inp[1] in outs:
                    cnt += 1
            else:
                raise AttributeError

        return cnt


    def _init_inp_pat(self):
        pat_inp = [set() for i in range(len(self.transformation_list))]

        inputs = []
        for inp, outs in self.rows.items():
            for out in outs:
                inputs.append((inp, out))
        inp_pat = [set() for i in range(len(inputs))]

        for inp_idx, inp in enumerate(inputs):
            for pat_idx, pattern in enumerate(self.transformation_list):
                if type(pattern) is Pattern:
                    if pattern.apply(inp[0]) == inp[1]:
                        pat_inp[pat_idx].add(inp_idx)
                        inp_pat[inp_idx].add(pat_idx)
                elif type(pattern) is ExtendedPattern:  # @TODO: This is not the best way to measure coverage
                    outs = pattern.apply(inp[0])
                    if inp[1] in outs:
                        pat_inp[pat_idx].add(inp_idx)
                        inp_pat[inp_idx].add(pat_idx)
                else:
                    raise AttributeError

        self._pat_inp = pat_inp
        self._inp_pat = inp_pat
        self._inputs = inputs

    def __repr__(self):
        s = "Trans Eval: { " + self.item['src_table'][4:]
        s += f"\nInput Len: {len(self.inp_pat)},\n"
        s += f"Number of Trans: {len(self.transformation_list)},\n"
        s += f"Best pattern Coverage: {self.best_pattern_coverage},\n"
        s += f"Coverage: {self.coverage},\n"
        return s + "\n}"



