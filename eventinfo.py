#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from iconbutton import IconButton
from scrollablelabel import ScrollableLabel


class PlayerBio(Popup):
    
    def __init__(self, name, **kwargs):
        super(PlayerBio, self).__init__(**kwargs)
        file_path = 'img/players/' + name.lower() + '.txt'
        with open(file_path) as f:
            lines = f.readlines()
            self.title = lines[0]
            # https://github.com/kivy/kivy/wiki/Scrollable-Label
            lbl = ScrollableLabel(text=''.join(lines[2:]), size_hint_y=.95)
            self.content = lbl


class PlayerInfo(StackLayout):

    def __init__(self, name, orientation, **kwargs):
        super(PlayerInfo, self).__init__(**kwargs)
        self.name = name
        self.orientation = orientation
        picture_path = 'img/players/' + name.lower() + '.jpg'
        self.picture = Image(source=picture_path, size_hint=[.5, 1])
        file_path = 'img/players/' + name.lower() + '.txt'
        self.bio = BoxLayout(orientation='vertical', size_hint=[.5, 1])
        with open(file_path) as f:
            line = f.readline()
            self.caption = Label(text=line)
            line = f.readline()
            flag_path = 'img/players/' + line.strip()
            self.flag = Image(source=flag_path, allow_stretch=True)
            self.bio.add_widget(self.flag)
            self.bio.add_widget(self.caption)
        self.add_widget(self.picture)
        self.add_widget(self.bio)
        
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            bio = PlayerBio(self.name, size_hint=[.85, .85])
            bio.open()


class EventInfo(StackLayout):

    def __init__(self, **kwargs):
        super(EventInfo, self).__init__(**kwargs)
        self.player_info = []
        self.lbl_versus = None
        self.orientation = 'tb-lr'
        self.lbl_players = Label(text='Players', size_hint=[1, 1./9], bold=True)
        self.lbl_players.color = [.2, .2, .2, 1.]
        self.content = BoxLayout(orientation = 'vertical', size_hint=[1, 8./9],
            padding=10)
        self.add_widget(self.lbl_players)
        self.add_widget(self.content)
        self.bind(pos=self.draw, size=self.draw)
    
    def draw(self, *args):
        # header
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.8, .8, .8, 1.)
            x = self.x
            y = self.y + self.height * 8./9
            w = self.width
            h = self.height / 9
            Rectangle(pos=[x, y], size=[w, h])
    
    def set_players(self, names):
        orientations = ['lr-tb', 'rl-tb']
        del self.player_info[:]
        i = 0
        while i < 2:
            wgt = PlayerInfo(names[i], orientations[i])
            self.player_info.append(wgt)
            i += 1
    
    def set_text(self, text):
        self.lbl_versus = Label(text=text, markup=True, font_size=24)
  
    def build(self):
        self.content.clear_widgets()
        self.content.add_widget(self.player_info[0])
        self.content.add_widget(self.lbl_versus)
        self.content.add_widget(self.player_info[1])
