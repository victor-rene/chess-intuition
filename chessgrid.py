#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.label import Label

from chess.board import Board
from iconbutton import IconButton

red = [1., 0., 0., 1.]
yellow = [1., 1., 0., 1.]


class BoardView(FloatLayout):

    def __init__(self, **kwargs):
        super(BoardView, self).__init__(**kwargs)
        self.is_flipped = False
        self.board = Board()
        self.board.add_listener(self)
        self.bind(pos=self.draw, size=self.draw)
        self.side_to_move = 1
        self.touches = []
        self.validator = None
        self.last_move = None
        self.selection = None
        self.hint = None
  
    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1., 1., 1., 1.)
            for rank in range(8):
                for file in range(8):
                    c = self.board.squares[file][rank]
                    if (rank + file) % 2 == 0:
                        background = 'b'
                    else: background = 'w'
                    if c == ' ':
                        piece = 'sq'
                    else:
                        if c.islower():
                            piece = 'b' + c.lower()
                        else: piece = 'w' + c.lower()
                    img_name = 'img/tiles/' + background + piece + '.png'
                    if self.is_flipped:
                        y = 8 - (rank + 1)
                        x = 8 - (file + 1)
                    else:
                        y = rank
                        x = file
                    Rectangle(source=img_name, pos=[self.x + x * self.width/8.0,
                            self.y + y * self.height/8.0],
                        size=[self.width/8.0, self.height/8.0])
              
    def draw_selection(self, square, color):
        file, rank = square[0], square[1]
        with self.canvas.after:
            Color(color[0], color[1], color[2], color[3])
            if self.is_flipped:
                rank = 8 - (rank + 1)
                file = 8 - (file + 1)
            x1 = self.x + file * self.width / 8.0
            x2 = self.width / 8.0
            y1 = self.y + rank * self.height / 8.0
            y2 = self.height / 8.0
            Line(rectangle=(x1, y1, x2, y2), width=2)
      
    def draw_last_move(self, input):
        orig = input[0]
        dest = input[1]
        with self.canvas.after:
            Color(1. ,1. ,1. , 1.)
            
            file, rank =  orig[0], orig[1]
            if self.is_flipped:
                rank = 8 - (rank + 1)
                file = 8 - (file + 1)
            x1 = self.x + file * self.width / 8.0
            x2 = self.width / 8.0
            y1 = self.y + rank * self.height / 8.0
            y2 = self.height / 8.0
            Line(rectangle=(x1, y1, x2, y2), width=2)
            
            file, rank =  dest[0], dest[1]
            if self.is_flipped:
                rank = 8 - (rank + 1)
                file = 8 - (file + 1)
            x1 = self.x + file * self.width / 8.0
            x2 = self.width / 8.0
            y1 = self.y + rank * self.height / 8.0
            y2 = self.height / 8.0
            Line(rectangle=(x1, y1, x2, y2), width=2)
      
    def draw_highlight(self):
        self.canvas.after.clear()
        if self.last_move:
            self.draw_last_move(self.last_move)
        if self.hint:
            self.draw_selection(self.hint, red)
        if self.selection: 
            self.draw_selection(self.selection, yellow)
            
    def flip_coords(self, n):
        return 8 - (n + 1)
              
    def flip(self, *args):
        self.is_flipped = not self.is_flipped
        if self.is_flipped:
            self.parent.lay_ranks.orientation = 'bt-lr'
            self.parent.lay_files.orientation = 'rl-tb'
        else:
            self.parent.lay_ranks.orientation = 'lr-tb'
            self.parent.lay_files.orientation = 'bt-lr'
        self.update()
    
    def update(self):
        self.draw()
        self.draw_highlight()
    
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            file = int( (touch.x - self.x) / self.width * 8 )
            rank = int( (touch.y - self.y) / self.height * 8 )
            if self.is_flipped:
                rank = 8 - (rank + 1)
                file = 8 - (file + 1)
            n = len(self.touches)
            if n == 0:
                self.touches.append([file, rank])
                self.selection = [file, rank]
                self.draw_highlight()
            if n == 1:
                self.touches.append([file, rank])
                self.validator.test_next(self.touches[:])
                del self.touches[:]
                self.selection = []
                self.draw_highlight()
      
    def set_validator(self, validator):
        self.validator = validator
    
    def show_hint(self, square):
        self.hint = square
        self.draw_highlight()
    
    def hide_hint(self):
        self.hint = None
        self.draw_highlight()


class Chessgrid(FloatLayout):

    def __init__(self, **kwargs):
        super(Chessgrid, self).__init__(**kwargs)
        self.boardview = BoardView(size_hint=[.9,.9], pos_hint={'x':.1, 'y':.1})
        self.add_widget(self.boardview)
        self.lay_files = StackLayout(pos_hint={'x':.1, 'y':0}, size_hint=[.9,.1],
            orientation='lr-tb')
        self.lay_files.canvas.before.add(Color(.2, .2, .2, 1.))
        for i in range(8):
            self.lay_files.add_widget(Label(text=chr(i+97), size_hint=[.99/8, 1]))
        self.add_widget(self.lay_files)
        self.lay_ranks = StackLayout(pos_hint={'x':0, 'y':.1}, size_hint=[.1,.9],
            orientation='tb-lr')
        for i in range(8):
            self.lay_ranks.add_widget(Label(text=str(8-i), size_hint=[1., .99/8]))
        self.add_widget(self.lay_ranks)
        self.flip_button = IconButton(size_hint=[.1,.1], pos_hint={'x':0, 'y':0},
            icon='img/flip.png')
        self.flip_button.bind(on_press=self.boardview.flip)
        self.add_widget(self.flip_button)
        with self.canvas.before:
            Color(.2, .2, .2, 1.)
            self.rect = Rectangle()
        self.bind(pos=self._update_rect, size=self._update_rect)
        
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
