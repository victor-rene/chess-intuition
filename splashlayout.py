#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.progressbar import ProgressBar

from iconbutton import IconButton


class SplashLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(SplashLayout, self).__init__(**kwargs)
        self.img_1 = Image(source='img/anand.jpg', size_hint=(1, .2),
            pos_hint={'center_x': .5, 'center_y': .85})
        self.lbl_1 = Label(text='[size=24]Vishy Anand Chess Champion[/size]',
            size_hint=(1, .2),
            pos_hint={'center_x': .5, 'center_y': .7}, font='font/Ubuntu-B.ttf',
            markup=True)
        self.img_2 = Image(source='img/logiqub_128.png', size_hint=(1, .2),
            pos_hint={'center_x': .5, 'center_y': .45})
        self.lbl_2 = Label(text='[size=24]by logiqub.com[/size]',
            size_hint=(1, .2),
            pos_hint={'center_x': .5, 'center_y': .3}, font='font/Ubuntu-B.ttf',
            markup=True)
        self.pb = ProgressBar(max=100, size_hint=(1, .2),
            pos_hint={'center_x': .5, 'center_y': .1})
        self.btn = IconButton(text='Start', size_hint=(.5, .1),
            pos_hint={'center_x': .5, 'center_y': .1})
        self.add_widget(self.img_1)
        self.add_widget(self.lbl_1)
        self.add_widget(self.img_2)
        self.add_widget(self.lbl_2)
        self.add_widget(self.btn)
        self.btn.bind(on_release=self.anim_load)
        
    def anim_load(self, *args):
        self.remove_widget(self.btn)
        self.add_widget(self.pb)
        anim = Animation(value=100)
        anim.bind(on_complete=self.anim_done)
        anim.start(self.pb)
        
    def anim_done(self, *args):
        pass
