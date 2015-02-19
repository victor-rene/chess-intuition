#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from homelayout import HomeLayout
from splashlayout import SplashLayout
from selectionlayout import SelectionLayout
from gamelayout import GameLayout


class HomeScreen(Screen):
    
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        hl = HomeLayout()
        hl.show_games_cb = lambda *a: self.parent.navigate('selection')
        self.add_widget(hl)

        
class SplashScreen(Screen):

    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        sl = SplashLayout()
        sl.anim_done = lambda *a: self.parent.navigate('home')
        self.add_widget(sl)

        
class SelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(SelectionScreen, self).__init__(**kwargs)
        sl = SelectionLayout()
        sl.back_cb = lambda *a: self.parent.navigate('home', 'right')
        sl.load_cb = lambda *a: self.parent.navigate('game')
        self.add_widget(sl)
        
        
class GameScreen(Screen):

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        gl = GameLayout()
        gl.back_cb = lambda *a: self.parent.navigate('selection', 'right')
        self.add_widget(gl)

        
class RootWidget(ScreenManager):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        scr_splash = SplashScreen(name='splash')
        self.add_widget(scr_splash)
        scr_home = HomeScreen(name='home')
        self.add_widget(scr_home)
        scr_select = SelectionScreen(name='selection')
        self.add_widget(scr_select)
        scr_game = GameScreen(name='game')
        self.add_widget(scr_game)
        
    def navigate(self, name, direction='left'):
        self.transition.direction = direction
        self.current = name
      

class VaccApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    VaccApp().run()
