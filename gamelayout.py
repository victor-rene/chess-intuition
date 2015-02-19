#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButton

from iconbutton import IconButton
from chessgrid import Chessgrid
from movelist import MoveList


class GameLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.btn_back = IconButton(size_hint=(.19, .1), text='Back',
            pos_hint={'x':.62, 'y': 0.})
        self.btn_back.bind(on_release=self.back)
        self.btn_mode = ToggleButton(size_hint=(.19, .1), text='Learn',
            pos_hint={'x':.81, 'y': 0.})
        self.btn_mode.background_normal = 'img/btn_square_normal.png'
        self.btn_mode.background_down = 'img/btn_square_down.png'
        self.btn_mode.bind(on_release=self.switch_mode)
        self.movelist = MoveList(size_hint=(0.38, 0.9),
            pos_hint={'x':.62, 'y': .1})
        self.chessgrid = Chessgrid(size_hint=(0.62, 1.0),
            pos_hint={'x': 0, 'y': 0})
        self.add_widget(self.chessgrid)
        self.add_widget(self.btn_back)
        self.add_widget(self.btn_mode)
        self.add_widget(self.movelist)
        
    def setup(self, game):
        self.movelist.set_source(game, self.chessgrid.boardview)
        self.chessgrid.boardview.set_validator(self.movelist)
        self.movelist.first()
        
    def back(self, *args):
        if hasattr(self, 'back_cb'):
            self.back_cb()

    def switch_mode(self, *args):
        self.movelist.switch_mode()
