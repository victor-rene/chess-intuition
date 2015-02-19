#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_string('''
<ScrollableLabel>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width * .95, None
        text: root.text
''')

class ScrollableLabel(ScrollView):
    text = StringProperty('')
