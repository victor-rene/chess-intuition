from vector import Vector
from movement import movements


def dest_rank(text):
    i = len(text) -1
    while i >= 0:
        if text[i].isdigit():
            return ord(text[i]) - 48 - 1
        else: i -= 1
    raise Exception("No number found in " + text + ".")

  
def dest_file(text):
    i = len(text) - 1
    while i >= 0:
        if text[i].islower():
            return ord(text[i]) - 96 - 1
        else: i -= 1
    raise Exception("No lowercase char found in " + text + ".")

        
def convert_file(c):
    return ord(c) - 96 - 1

  
def convert_rank(c):
    return ord(c) - 48 - 1


def search_pieces(board, type, file=None, rank=None):
    squares = []
    file_range = []
    rank_range = []
    if file != None:
        file_range = [file]
    else: file_range = range(8)
    if rank != None:
        rank_range = [rank]
    else: rank_range = range(8)
    for rank in rank_range:
        for file in file_range:
            if board.squares[file][rank] == type:
                squares.append([file, rank]);
    return squares
  
  
def clear_path(board, orig, dest, vector):
    square = orig[:]
    i = 1
    while i < 8: # safety measure to prevent infinite loop
        square[0] += vector.dx
        square[1] += vector.dy
        if square[0] == dest[0] and square[1] == dest[1]:
            return True
        if board.squares[square[0]][square[1]] == ' ':
            i += 1
        else: return False
  
  
def origin_hint(move):
    offset = 1 if 'x' in move else 0 # capture
    if len(move) < (4 + offset) or move[2 + offset].isdigit():
        return None
    else: return move[1]
  
  
# //http://en.wikipedia.org/wiki/Portable_Game_Notation
def read_algebraic(board, move):
    input = None
    if move[0] == 'O': # castle
        if board.side_to_move == -1:
            if move == "O-O": # short
                board.squares[5][7] = 'r'
                board.squares[6][7] = 'k'
                board.squares[7][7] = ' '
                board.squares[4][7] = ' '
                input = ([4, 7], [6, 7])
            elif move == "O-O-O": # long
                board.squares[3][7] = 'r'
                board.squares[2][7] = 'k'
                board.squares[0][7] = ' '
                board.squares[4][7] = ' '
                input = ([4, 7], [2, 7])
        else:
            if move == "O-O": # short
                board.squares[5][0] = 'R'
                board.squares[6][0] = 'K'
                board.squares[7][0] = ' '
                board.squares[4][0] = ' '
                input = ([4, 0], [6, 0])
            elif move == "O-O-O": # long
                board.squares[3][0] = 'R'
                board.squares[2][0] = 'K'
                board.squares[0][0] = ' '
                board.squares[4][0] = ' '
                input = ([4, 0], [2, 0])
  else: # not castle
    # if 'x' in move: # capture
      # captured = self.squares[destfile][destrank]
      # if captured == None:
        # raise Exception("No piece to capture on " + dest.ToString() + ".")
      # self.squares[destfile][destrank] = ' '
    destrank = dest_rank(move)
    destfile = dest_file(move)
    origfile = None
    origrank = None
    if move[0].islower(): # pawn move
      pawns = None
      origfile = convert_file(move[0])
      if board.side_to_move == 1:
        pawns = search_pieces(board, 'P', file=origfile)
      else: pawns = search_pieces(board, 'p', file=origfile)
      if move[1] == 'x': # capture
        origrank = destrank - board.side_to_move
        board.squares[destfile][destrank] = board.squares[origfile][origrank]
        board.squares[origfile][origrank] = ' '
        input = ([origfile, origrank], [destfile, destrank])
      else: # not a capture
        if len(pawns) == 1: # only one pawn in file
          origfile = pawns[0][0]
          origrank = pawns[0][1]
          board.squares[destfile][destrank] = board.squares[origfile][origrank]
          board.squares[origfile][origrank] = ' '
          input = ([origfile, origrank], [destfile, destrank])
        else: # find pawn closest to destination
          i = 1
          while i < 8:
            origrank = destrank - i * board.side_to_move
            if board.squares[origfile][origrank] != ' ':
              break
            i += 1
          board.squares[destfile][destrank] = board.squares[origfile][origrank]
          board.squares[origfile][origrank] = ' '
          input = ([origfile, origrank], [destfile, destrank])
      if move.find('=') != -1: # promotion
        pos = move.index('=')
        if board.side_to_move == 1:
          board.squares[destfile][destrank] = move[pos+1]
        else: board.squares[destfile][destrank] = move[pos+1].lower()
    else: # piece move
      if board.side_to_move == 1:
        squares = search_pieces(board, move[0])
      else: squares = search_pieces(board, move[0].lower())
      if len(squares) == 1: # only one piece
        origfile = squares[0][0]
        origrank = squares[0][1]
      else: # find origin square
        orig = None
        hint = origin_hint(move)
        if not hint: # only one candidate piece
          for file, rank in squares:
            vector = Vector.create(file, rank, destfile, destrank)
            squares = search_pieces(board, move[0])
            piece = board.squares[file][rank]
            if movements[piece].is_sliding:
              vector.normalize()
            for v in movements[piece].vectors:
              # print move, board.side_to_move, '.', v.dx, v.dy, '|', vector.dx, vector.dy
              if v == vector and clear_path(board, [file, rank], [destfile, destrank], v):
                orig = [file, rank]
                break
        else: # several candidates  pieces
          if hint.isdigit(): # hint is rank
            for square in squares:
              if square[1] == convert_rank(hint):
                orig = square
                break
          else: # hint is file
            for square in squares:
              if square[0] == convert_file(hint):
                orig = square
                break
        origfile = orig[0]
        origrank = orig[1]
      board.squares[destfile][destrank] = board.squares[origfile][origrank]
      board.squares[origfile][origrank] = ' '
      input = ([origfile, origrank], [destfile, destrank])
  board.switch_turn()
  # print move, board.to_fen() 
  return input
