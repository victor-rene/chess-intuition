#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.graphics import Rectangle
from kivy.uix.label import Label


class ScoreLabel(Label):

    def __init__(self, **kwargs):
        super(ScoreLabel, self).__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw)
        self.rect = Rectangle(pos=self.pos, size=[21., 21.])
    
    def draw(self, *args):
        x, y = self.x + 10, self.y + 10
        self.rect.pos=[x, y]
      
    def set_score(self, score):
        if score is None:
            return
        self.canvas.after.clear()
        with self.canvas.after:
            x, y = self.x + 10, self.y + 10
            self.rect = Rectangle(pos=[x, y], size=[21., 21.])
        if score == 1.0:
            self.rect.source='./img/s.png'
        elif score > 0.8:
            self.rect.source='./img/a.png'
        elif score > 0.6:
            self.rect.source='./img/b.png'
        elif score > 0.4:
            self.rect.source='./img/c.png'
        elif score > 0.2:
            self.rect.source='./img/d.png'
        else:
            self.rect.source='./img/e.png'
