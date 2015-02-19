#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout

from iconbutton import IconButton
from gameselection import GameSelection
from scrollablelabel import ScrollableLabel


class EventSummary(Popup):
    
    def __init__(self, year, **kwargs):
        super(EventSummary, self).__init__(**kwargs)
        file_path = 'page/summary_WCC_' + year + '.txt'
        with open(file_path) as f:
            self.title = 'Summary of World Chess Championship %s' % year
            # https://github.com/kivy/kivy/wiki/Scrollable-Label
            lbl = ScrollableLabel(text=f.read(), size_hint_y=.95)
            self.content = lbl


class SelectionLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(SelectionLayout, self).__init__(**kwargs)
        self.gameselection = GameSelection(size_hint=(1., .9),
            pos_hint={'x': 0, 'y': .1})
        self.gameselection.load_events()
        self.btn_back = IconButton(text='Back', size_hint=(0.24, 0.1),
            pos_hint={'x': 0, 'y': .0})
        self.btn_back.bind(on_release=self.back)
        self.btn_load = IconButton(text='Load', size_hint=(0.24, 0.1),
            pos_hint={'x': .76, 'y': .0})
        self.btn_load.bind(on_release=self.load)
        self.btn_summary = IconButton(size_hint=(0.5, 0.1),
            pos_hint={'x': .25, 'y': .0})
        self.btn_summary.bind(on_release=self.show_summary)
        self.add_widget(self.gameselection)
        self.add_widget(self.btn_back)
        self.add_widget(self.btn_load)
        
    def back(self, *args):
        if hasattr(self, 'back_cb'):
            self.back_cb()
            
    def load(self, *args):
        selected_game = self.gameselection.gamelist.selected_item
        if selected_game is not None and hasattr(self, 'load_cb'):
            wgt = self
            while True:
                print wgt
                if wgt.parent == self.get_root_window():
                    break
                else: wgt = wgt.parent
            from kivy.uix.screenmanager import ScreenManager
            if wgt.__class__.__name__ == 'RootWidget':
                wgt.get_screen('game').children[0].setup(selected_game)
                self.load_cb()
        else:
            popup = Popup(title='Message',
            content=Label(text='Please select a game.'),
            size_hint=(None, None), size=(400, 400))
            popup.open()
            
    def set_year(self, year):
        self.btn_summary.text = 'Summary of WCC %s' % year
        if not self.btn_summary in self.children:
            self.add_widget(self.btn_summary)
            
    def show_summary(self, *args):
        summary = EventSummary(args[0].text[-4:], size_hint=[.85, .85])
        summary.open()
