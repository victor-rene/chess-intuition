#!/usr/bin/env python
# -*- coding: utf-8 -*-


def try_save_score(pgnindex, score):
    filename = pgnindex.filename[0:-3] + 'sav'
    with open(filename, 'r') as f:
        d = eval(f.read())
    if (not pgnindex.index in d) or score > d[pgnindex.index]:
        with open(filename, 'w') as f:
            d[pgnindex.index] = score
            f.write(str(d))
      
def load_scores(filename):
    filename = filename[0:-3] + 'sav'
    with open(filename, 'r') as f:
        d = eval(f.read())
        return d
