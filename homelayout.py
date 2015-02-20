#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout

from iconbutton import IconButton


class HomeLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(HomeLayout, self).__init__(**kwargs)
        # self.img_1 = Image(source='img/anand.jpg', size_hint=(1, .2),
            # pos_hint={'center_x': .5, 'center_y': .85})
        self.lbl_1 = Label(text='Chess Intuition',
            size_hint=(1, .2),
            pos_hint={'center_x': .5, 'center_y': .8}, font='font/Ubuntu-B.ttf',
            )
        self.img = Image(source='img/logiqub_128.png', size_hint=(1. ,.2),
            pos_hint={'center_x': .5, 'center_y': .6})
        self.btn_about = IconButton(text='About', size_hint=(.3, .1),
            pos_hint={'center_x': .25, 'center_y': .4})
        self.btn_about.bind(on_release=self.show_about)
        self.btn_help = IconButton(text='How to use', size_hint=(.3, .1),
            pos_hint={'center_x': .25, 'center_y': .25})
        self.btn_help.bind(on_release=self.show_help)
        self.btn_games = IconButton(text='Game list', size_hint=(.3, .1),
            pos_hint={'center_x': .75, 'center_y': .4})
        self.btn_games.bind(on_release=self.show_games)
        self.btn_credits = IconButton(text='Credits', size_hint=(.3, .1),
            pos_hint={'center_x': .75, 'center_y': .25})
        self.btn_credits.bind(on_release=self.show_credits)
        # self.add_widget(self.img_1)
        self.add_widget(self.lbl_1)
        self.add_widget(self.img)
        self.add_widget(self.btn_about)
        self.add_widget(self.btn_help)
        self.add_widget(self.btn_games)
        self.add_widget(self.btn_credits)
            
    def show_about(self, *args):
        with open('page/about.txt') as f:
            p = Popup(content=Label(text=f.read()), size_hint=(.8, .8),
                title='About')
            p.open()
        
    def show_help(self, *args):
        with open('page/how_to_use.txt') as f:
            p = Popup(content=Label(text=f.read()), size_hint=(.8, .8),
                title='How to use')
            p.open()

    def show_games(self, *args):
        if hasattr(self, 'show_games_cb'):
            self.show_games_cb()
            
    def show_credits(self, *args):
        with open('page/credits.txt') as f:
            p = Popup(content=Label(text=f.read(),
                    font_name='font/UbuntuMono-R.ttf'),
                size_hint=(.8, .8),
                title='Credits')
            p.open()
