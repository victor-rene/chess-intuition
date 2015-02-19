#!/usr/bin/env python
# -*- coding: utf-8 -*-


def split_games(filename):
    with open(filename) as f:
        lines = f.readlines()
    games = []
    str_list = []
    n = len(lines)
    i = 0
    while i < n:
        line = lines[i]
        if line.startswith('[Event '):
            if i > 0:
                games.append('\n'.join(str_list))
                del str_list[:]
        if line: # not empty
            str_list.append(line)
        i += 1
    games.append('\n'.join(str_list))
    return games

  
def pgn_header(text):
    i = text.index(' ');
    key = text[1:i]
    value = text[i+2:-2]
    return key, value

  
class PgnIndex:

    def __init__(self, filename, index, game):
        self.filename = filename
        self.index = index
        self.game = game
  

class PgnInfo:

    def __init__(self):
        self.headers = dict()
        self.moves = []
        self.result = None
    

def pgn_info(text):
    pgnInfo = PgnInfo()
    lines = text.split('\n')
    i = 0
    n = len(lines)
    afterheaders = False
    s = ''
    # set headers
    while i < n:
        line = lines[i]
        if line:
            if afterheaders:
                s += line + " "
            elif line.startswith("1."):
                afterheaders = True;
                s += line + " "
            else:
                entry = pgn_header(line)
                pgnInfo.headers[entry[0]] = entry[1]
        i += 1

    # set moves and result
    tmp = s.split()
    moves = []
    for s in tmp:
        if not s or '.' in s:
            continue
        else: moves.append(s)
              
    last = len(moves) - 1
    pgnInfo.result = moves[last]
    del moves[last]
    pgnInfo.moves = moves

    return pgnInfo