#!/usr/bin/env python
# -*- coding: utf-8 -*-


from vector import vectors


# Does not handle pawns moves (en-passant, double advance, promotion) and castle
class Movement:
    def __init__(self):
        self.vectors = []
        self.is_sliding = False
    
rook_movement = Movement()
rook_movement.vectors.append(vectors['N'])
rook_movement.vectors.append(vectors['E'])
rook_movement.vectors.append(vectors['S'])
rook_movement.vectors.append(vectors['W'])
rook_movement.is_sliding = True

bishop_movement = Movement()
bishop_movement.vectors.append(vectors['NE'])
bishop_movement.vectors.append(vectors['NW'])
bishop_movement.vectors.append(vectors['SW'])
bishop_movement.vectors.append(vectors['SE'])
bishop_movement.is_sliding = True

octopus = rook_movement.vectors + bishop_movement.vectors
queen_movement = Movement()
queen_movement.vectors = octopus
queen_movement.is_sliding = True
king_movement = Movement()
king_movement.vectors = octopus
king_movement.is_sliding = False
    
knight_movement = Movement()
knight_movement.vectors.append(vectors['NNE'])
knight_movement.vectors.append(vectors['NNW'])
knight_movement.vectors.append(vectors['SSE'])
knight_movement.vectors.append(vectors['SSW'])
knight_movement.vectors.append(vectors['ENE'])
knight_movement.vectors.append(vectors['ESE'])
knight_movement.vectors.append(vectors['WNW'])
knight_movement.vectors.append(vectors['WSW'])
knight_movement.is_sliding = False

movements = dict()
movements['k'] = king_movement
movements['K'] = king_movement
movements['q'] = queen_movement
movements['Q'] = queen_movement
movements['r'] = rook_movement
movements['R'] = rook_movement
movements['b'] = bishop_movement
movements['B'] = bishop_movement
movements['n'] = knight_movement
movements['N'] = knight_movement
