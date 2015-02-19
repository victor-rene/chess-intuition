#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

import score
from chess.parser import read_algebraic
from movelabel import MoveLabel
from iconbutton import IconButton


class MoveList(GridLayout):

    def __init__(self, **kwargs):
        super(MoveList, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.pgnindex = None
        self.board = None
        self.mode = 'learn'
        self.header = BoxLayout(cols = 3, rows=1, orientation='vertical',
            size_hint=[1,.15])
        self.add_widget(self.header)
        self.scrollview = ScrollView()
        self.scrollview.do_scroll_x = False
        self.content = GridLayout(cols=3, size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scrollview.add_widget(self.content)
        self.add_widget(self.scrollview)
        self.buttons = GridLayout(cols=5, rows=1, size_hint=[1, .1])
        self.btn_next = IconButton(caption='', icon='img/next.png')
        self.btn_next.bind(on_press=self.next)
        self.btn_prev = IconButton(caption='', icon='img/prev.png')
        self.btn_prev.bind(on_press=self.previous)
        self.btn_auto = IconButton(caption='', icon='img/auto.png')
        self.btn_auto.bind(on_press=self.auto)
        self.btn_last = IconButton(caption='', icon='img/last.png')
        self.btn_last.bind(on_press=self.last)
        self.btn_first = IconButton(caption='', icon='img/first.png')
        self.btn_first.bind(on_press=self.first)
        self.buttons.add_widget(self.btn_first)
        self.buttons.add_widget(self.btn_prev)
        self.buttons.add_widget(self.btn_auto)
        self.buttons.add_widget(self.btn_next)
        self.buttons.add_widget(self.btn_last)
        self.add_widget(self.buttons)
        self.fens = []
        self.selected_index = -1
        self.selected_label = None
        self.touches = dict()
        with self.canvas.before:
            Color(.8, .8, .8, 1.)
            self.rect_before = Rectangle()
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.inputs = []
        self.mistakes = 0
        self.consecutive = 0
        self.running = False
        
    def set_source(self, pgnindex, boardview):
        self.header.clear_widgets()
        self.header.add_widget(Label(text=pgnindex.game.headers['White'],
            bold=True, color=(.2, .2, .2, 1.)))
        self.header.add_widget(Label(text=pgnindex.game.result,
            bold=True, color=(.2, .2, .2, 1.)))
        self.header.add_widget(Label(text=pgnindex.game.headers['Black'],
            bold=True, color=(.2, .2, .2, 1.)))
        
        self.boardview = boardview
        self.board = boardview.board
        self.board.starting_position()
        del self.fens[:]
        self.fens.append(self.board.to_fen())
        
        del self.inputs[:]
        self.inputs.append(None)
        self.content.clear_widgets()
        
        self.pgnindex = pgnindex
        i = 0
        for move in pgnindex.game.moves:
            if i % 2 == 0: # move number
                self.content.add_widget(MoveLabel(text=str((i/2) + 1) + '.',
                    height=50, size_hint_y=None))
            lbl_move = MoveLabel(text=move, height=50, size_hint_y=None)
            lbl_move.bind(on_touch_down=self.update_board)
            self.content.add_widget(lbl_move)
            self.inputs.append(read_algebraic(self.board, move))
            fen = self.board.to_fen()
            self.fens.append(fen)
            self.touches[lbl_move] = i
            i += 1
      
    def set_index(self, i):
        # reset previous color
        self.selected_index = i
        if self.selected_label:
            self.selected_label.background = [.2, .2, .2]
        
        self.board.from_fen(self.fens[self.selected_index]) 
        self.boardview.last_move = self.inputs[self.selected_index]
        self.boardview.draw_highlight()
        
        n = len(self.content.children)
        lbls = self.content.children[:]
        lbls.reverse()
        ilbl = (i-1) * 3/2 + 1
        if ilbl >= 0:
            self.selected_label = lbls[ilbl]
            self.selected_label.background = [.2, .3, .5]
      
    def update_board(self, instance, touch):
        if self.mode == 'play':
            return
        if instance.collide_point(touch.x, touch.y):
            self.set_index(self.touches[instance] + 1)
      
    def next(self, *args):
        if self.selected_index < len(self.fens) - 1:
            self.set_index(self.selected_index + 1)
        if not self.running or self.selected_index == len(self.fens) - 1:
            self.btn_auto.icon = 'img/auto.png'
            return False
      
    def previous(self, *args):
        if self.selected_index > 0:
            self.set_index(self.selected_index - 1)
      
    def first(self, *args):
        self.set_index(0)
    
    def last(self, *args):
        self.set_index(len(self.fens) - 1)
    
    def auto(self, *args):
        if self.running:
            self.running = False
            self.btn_auto.icon = 'img/auto.png'
        else:
            self.running = True
            self.btn_auto.icon = 'img/stop.png'
        if self.running:
            Clock.schedule_interval(self.next, 1.0)
    
    def switch_mode(self, *args):
        btn_mode = self.parent.btn_mode
        if btn_mode.text == 'Play':
            btn_mode.text = 'Learn'
        else: btn_mode.text = 'Play'
        if self.mode == 'learn':
            self.mode = 'play'
            self.hide()
            self.disable_buttons(True)
            self.first()
            self.mistakes = 0
        else:
            self.mode = 'learn'
            self.reveal()
            self.disable_buttons(False)
    
    def hide(self):
        with self.canvas.after:
            Color(1., 1., 1., 1.)
            self.rect = Rectangle(source='./img/dessin.png',
                pos=self.pos, size=self.size)
    
    def reveal(self):
        self.canvas.after.clear()
    
    def _update_rect(self, *args):
        self.rect_before.pos = self.pos
        self.rect_before.size = self.size
    
    def disable_buttons(self, value):
        self.btn_next.disabled = value
        self.btn_prev.disabled = value
        self.btn_last.disabled = value
        self.btn_first.disabled = value
    
    def test_next(self, squares):
        i_next = self.selected_index + 1
        if i_next < len(self.fens):
            test1 = squares[0][0] == self.inputs[i_next][0][0]
            test2 = squares[0][1] == self.inputs[i_next][0][1]
            test3 = squares[1][0] == self.inputs[i_next][1][0]
            test4 = squares[1][1] == self.inputs[i_next][1][1]
            test = test1 and test2 and test3 and test4
            if test:
                self.consecutive = 0
                self.boardview.hide_hint()
                self.next()
                n = len(self.fens) - 1
                ratio = float(n - self.mistakes) / n
                if self.selected_index == n and self.mode == 'play':
                    score.try_save_score(self.pgnindex, ratio)
                    self.show_perf(ratio, self.mistakes)
                return True
            else:
                if self.consecutive:
                    if self.consecutive == 2:
                        self.boardview.show_hint(self.inputs[i_next][0])
                else:
                    self.mistakes += 1
                self.consecutive += 1
                return False
        
    def show_perf(self, score, mistakes):
        if score == 1.0:
            rank='S'
        elif score > 0.8:
            rank='A'
        elif score > 0.6:
            rank='B'
        elif score > 0.4:
            rank='C'
        elif score > 0.2:
            rank='D'
        else:
            rank='E'
        s = str(mistakes) + ' mistake(s). Rank: ' + rank + '.'
        popup = Popup(title='Result',
        content=Label(text=s),
        size_hint=(None, None), size=(400, 400))
        popup.open()
