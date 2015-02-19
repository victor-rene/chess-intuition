#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.properties import ListProperty


class MoveLabel(Label):
    
    background = ListProperty()
    
    def __init__(self, **kw):
        super(MoveLabel, self).__init__(**kw)
        with self.canvas.before:
            self.bg_color = Color(.2, .2, .2, 1.)
            self.rect = Rectangle()
        self.bind(pos=self._update_rect, size=self._update_rect)
        
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_background(self, *args):
        self.bg_color.rgb = self.background
