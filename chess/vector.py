#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Vector:
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy
        self.is_capture = False # for pawns
  
    @classmethod
    def create(cls, x1, y1, x2, y2):
        return Vector(x2 - x1, y2 - y1)
  
    def __eq__(self, other):
        if other is None:
            return False
        elif not isinstance(other, Vector):
            return False
        else:
            test = (other.dx == self.dx and other.dy == self.dy
                and other.is_capture == self.is_capture)
            return test

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.dx) ^ hash(self.dy) ^ hash(self.is_capture)
  
    def normalize(self):
        abs_x = abs(self.dx)
        abs_y = abs(self.dy)
        if abs_x == abs_y:
            self.dx /= abs_x
            self.dy /= abs_y
        elif abs_x == 0:
            self.dy /= abs_y
        elif abs_y == 0:
            self.dx /= abs_x


vectors = dict()
vectors['N'] = Vector(dx=0, dy=1)
vectors['E'] = Vector(dx=1, dy=0)
vectors['S'] = Vector(dx=0, dy=-1)
vectors['W'] = Vector(dx=-1, dy=0)
vectors['NE'] = Vector(dx=1, dy=1)
vectors['NW'] = Vector(dx=-1, dy=1)
vectors['SE'] = Vector(dx=1, dy=-1)
vectors['SW'] = Vector(dx=-1, dy=-1)
vectors['NNE'] = Vector(dx=1, dy=2)
vectors['NNW'] = Vector(dx=-1, dy=2)
vectors['SSE'] = Vector(dx=1, dy=-2)
vectors['SSW'] = Vector(dx=-1, dy=-2)
vectors['ENE'] = Vector(dx=2, dy=1)
vectors['ESE'] = Vector(dx=2, dy=-1)
vectors['WSW'] = Vector(dx=-2, dy=-1)
vectors['WNW'] = Vector(dx=-2, dy=1)
