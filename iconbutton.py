#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.properties import StringProperty


class IconButton(Button):

    icon = StringProperty()

    def __init__(self, **kwargs):
        super(IconButton, self).__init__(**kwargs)
        self.background_normal = 'img/btn_rect_normal.png'
        self.background_down = 'img/btn_rect_down.png'
        self.bind(icon=self._update_icon)
        if 'icon' in kwargs:
            with self.canvas.after:
                self.icon_rect = Rectangle(source=self.icon)
        
    def on_size(self, *args):
        if self.height < self.width / 2.:
            self.background_normal = 'img/btn_square_normal.png'
            self.background_down = 'img/btn_square_down.png'
        if self.icon:
            self.icon_rect.size = self.width * .6, self.height * .6
            self.icon_rect.pos = self.x + self.width * .2, \
                self.y + self.height * .2
            
    def _update_icon(self, *args):
        if self.icon:
            self.canvas.after.clear()
            with self.canvas.after:
                self.icon_rect = Rectangle(source=self.icon)
                self.icon_rect.pos = self.pos
                self.on_size()
