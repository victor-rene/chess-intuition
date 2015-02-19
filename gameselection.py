from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

import pgnutil, score
from eventinfo import EventInfo
from scorelabel import ScoreLabel


class GameList(StackLayout):

  def __init__(self, **kwargs):
    super(GameList, self).__init__(**kwargs)
    self.orientation = 'lr-tb'
    self.games = []
    self.bind(pos=self.draw, size=self.draw)
    self.data_bindings = dict()
    self.selected_view = None
    self.selected_item = None
    # header
    self.lbl_header = Label(text='Games', size_hint=[1., 1./9], bold=True)
    self.lbl_header.color = [.2, .2, .2, 1]
    self.add_widget(self.lbl_header)
    # content
    self.content = StackLayout(orientation = 'lr-tb')
    self.content.size_hint_y = None #for scrollviewer
    self.content.bind(minimum_height=self.content.setter('height'))
    self.scrollview = ScrollView(size_hint=[1, 8./9])
    self.scrollview.do_scroll_x = False
    self.scrollview.add_widget(self.content)
    self.add_widget(self.scrollview)
    self.scores = []
    
  def add_item(self, game, score):
    self.games.append(game)
    self.scores.append(score)
    self.draw()
    
  def clear(self):
    del self.games[:]
    del self.scores[:]
    self.clear_selection()
    self.draw()
    
  def clear_selection(self):
    self.selected_view = None
    self.selected_item = None
  
  def draw_background(self, *args):
    self.canvas.before.clear()
    with self.canvas.before:
      # header
      Color(.1, .1, .1, 1)
      Rectangle(pos=self.pos, size=self.size)
      Color(.8, .8, .8, 1.)
      w = self.width
      h = self.height / 9.
      x = self.x
      y = self.y + self.height * 8./9
      Rectangle(pos=[x, y], size=[w, h])
        
  def draw(self, *args):
    self.content.clear_widgets()
    self.data_bindings.clear()
    n = len(self.games)
    i = 0
    while i < n:
      pgnindex = self.games[i]
      lbl = ScoreLabel(text=pgnindex.game.headers['Round'], height=self.height/9,
        size_hint=[1, None]) #for scrollviewer parent
      lbl.bind(on_touch_down=self.selection_change)
      lbl.set_score(self.scores[i])
      self.content.add_widget(lbl)
      self.data_bindings[lbl] = pgnindex
      i += 1
    self.draw_background()
      
  def selection_change(self, instance, touch):
    for lbl in self.content.children:
      lbl.canvas.before.clear()
      if lbl.collide_point(touch.x, touch.y):
        lbl.bold = True
        lbl.canvas.before.add(Color(.2, .3, .5, 1.))
        lbl.canvas.before.add(Rectangle(pos=lbl.pos, size=lbl.size))
        lbl.canvas.before.add(Color(1., 1., 1., 1.))
        lbl.canvas.before.add(Line(points=[lbl.x+1, lbl.y, lbl.x+1, lbl.y + lbl.height]))
        self.selected_view = lbl
        self.selected_item = self.data_bindings[lbl]
      else:
        lbl.bold = False

        
class Event:

  def __init__(self, caption, filename, names):
    self.caption = caption
    self.filename = filename
    self.names = names
    
      
class EventList(StackLayout):

  def __init__(self, **kwargs):
    super(EventList, self).__init__(**kwargs)
    self.is_updating = False
    self.orientation = 'tb-lr'
    self.events = []
    self.bind(pos=self.draw, size=self.draw)
    self.selected = None
    self.lbl_event = Label(text='Event', size_hint=[1, 1./9], bold=True)
    self.lbl_event.color = [.2, .2, .2, 1.]
    self.add_widget(self.lbl_event)
    
  def begin_update(self):
    self.is_updating = True
    
  def end_update(self):
    self.is_updating = False
    self.draw()
    
  def add_event(self, event):
    self.events.append(event)
    if not self.is_updating:
      self.draw()
    
  def clear_events(self):
    del self.events[:]
    self.draw()
    
  def draw_background(self):
    self.canvas.before.clear()
    with self.canvas.before:
      # header
      Color(.8, .8, .8, 1.)
      w = self.width
      h = self.height / 9.
      x = self.x
      y = self.y + self.height * 8./9
      Rectangle(pos=[x, y], size=[w, h])
      # items
      i = 0
      n = len(self.events)
      h = (self.height * 8./9) / n
      while i < n:
        event = self.events[i]
        y = self.y + self.height * 8./9 - h * (i+1)
        if event.caption != self.selected:
          Color(.2, .2, .2, 1)
          Rectangle(pos=[x, y], size=[w, h])
        else:
          Color(.2, .3, .5, 1)
          Rectangle(pos=[x, y], size=[w, h])
          Color(1., 1., 1., 1.)
          Line(points=[self.right, y, self.right, y + h])
        i += 1
  
  def draw(self, *args):
    # remove children, except header
    lbls = [lbl for lbl in self.children if lbl != self.lbl_event]
    for lbl in lbls:
      self.remove_widget(lbl)
    # add one label for each event
    n = len(self.events)
    for event in self.events:
      lbl = Label(text=event.caption, size_hint=[1, 8./9/n], halign='center')
      if lbl.text == self.selected:
        lbl.bold = True
      else:
        lbl.bold = False
      self.add_widget(lbl)
    self.draw_background()
        
  def on_touch_down(self, touch):
    if self.collide_point(touch.x, touch.y):
      for lbl in self.children:
        if lbl != self.lbl_event and lbl.collide_point(touch.x, touch.y):
          self.selection_changed(lbl.text)

  def selection_changed(self, selected):
    self.selected = selected
    self.draw()
    self.parent.load_games(self.selected)
    for event in self.events:
      if event.caption == self.selected:
        self.parent.eventinfo.set_players(event.names)
        self.parent.eventinfo.set_text('VERSUS')
        self.parent.parent.set_year(event.caption[-4:])
        self.parent.eventinfo.build()
      
    
class GameSelection(FloatLayout):

    def __init__(self, **kwargs):
        super(GameSelection, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.eventlist = EventList(size_hint=[.24, 1.],
            pos_hint={'x': 0., 'y': 0.})
        self.eventinfo = EventInfo(size_hint=[.5, 1.],
            pos_hint={'x':.25, 'y': 0.})
        self.gamelist = GameList(size_hint=[.24, 1.],
            pos_hint={'x':.76, 'y': 0.})
        self.add_widget(self.eventlist)
        self.add_widget(self.eventinfo)
        self.add_widget(self.gamelist)

    def load_events(self):
        with open('data/game_selection.eng', 'r') as f:
            s = f.read()
            list = eval(s)
            for item in list:
                event = Event(item[0], './data/' + item[1], item[2])
                self.eventlist.begin_update()
                self.eventlist.add_event(event)
                self.eventlist.end_update()
        
    def load_games(self, caption):
        for event in self.eventlist.events:
            if event.caption == caption:
                scores = score.load_scores(event.filename)
                games = pgnutil.split_games(event.filename)
                self.gamelist.clear()
                i = 0
                n = len(games)
                while i < n:
                    game = games[i]
                    info = pgnutil.pgn_info(game)
                    pgn_index = pgnutil.PgnIndex(event.filename, i, info)
                    if i in scores:
                        self.gamelist.add_item(pgn_index, scores[i])
                    else: self.gamelist.add_item(pgn_index, None)
                    i += 1
