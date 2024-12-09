from Chessnut import Game
from collections import Counter
import time
import random

# Basic piece values

MATERIAL_VALUE = {
    "P": 82,
    "N": 337,
    "B": 365,
    "R": 477,
    "Q": 1025,
    "K": 0,
}


PAWN_VALUES = [
      0,   0,   0,   0,   0,   0,  0,   0,
     98, 134,  61,  95,  68, 126, 34, -11,
     -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0,
]


KNIGHT_VALUES = [
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
]

BISHOP_VALUES = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
]

ROOK_VALUES = [
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
]

QUEEN_VALUES = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
]

KING_VALUES = [
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
]

POSITIONAL_VALUE = {
    "P": PAWN_VALUES,
    "N": KNIGHT_VALUES,
    "B": BISHOP_VALUES,
    "R": ROOK_VALUES,
    "Q": QUEEN_VALUES,
    "K": KING_VALUES
}

def evaluate(game):
    eval = 0
    # Calculate the value of pieces on the board
    for char in str(game.board):
        if char.isupper() and char.upper() in MATERIAL_VALUE:
            eval += MATERIAL_VALUE[char.upper()]
        elif char.islower() and char.upper() in MATERIAL_VALUE:
            eval -= MATERIAL_VALUE[char.upper()]

    # Calculate the positional value of pieces on the board
    for i in range(64):
        piece = game.board.get_piece(i)
        if piece.upper() not in POSITIONAL_VALUE:
            continue
        piece_positional_value = POSITIONAL_VALUE[piece.upper()][i]
        eval += piece_positional_value if piece.isupper() else -piece_positional_value
    if game.state.player == "b":
        eval = -eval
    return eval

MAX_EVAL = float("inf")
DRAW_EVAL = 0

def is_threefold(fen_history):
    return Counter(fen_history).most_common(1)[0][1] >= 3


def quiescence(game, ply, alpha, beta, start_time, time_limit):
    if time.time() - start_time > time_limit:
        return evaluate(game), None

    stand_pat = evaluate(game)

    if stand_pat >= beta:
        return beta, None
    if alpha < stand_pat:
        alpha = stand_pat

    moves = list(game.get_moves())
    # Generate only capture moves
    capture_moves = []
    for move in moves:
        from_square = move[:2]
        to_square = move[2:4]
        captured_piece = game.board.get_piece(Game.xy2i(to_square))
        if captured_piece != ' ':
            capture_moves.append(move)

    if not capture_moves:
        return stand_pat, None

    best_value = stand_pat
    best_move = None

    original_fen = game.get_fen()
    fen_history_reference = game.fen_history.copy()

    for move in capture_moves:
        game.apply_move(move)
        value, _ = quiescence(game, ply + 1, -beta, -alpha, start_time, time_limit)
        value = -value

        game.set_fen(original_fen)
        game.fen_history = fen_history_reference.copy()

        if value >= beta:
            return beta, None
        if value > best_value:
            best_value = value
            best_move = move
        if value > alpha:
            alpha = value

    return best_value, best_move

def negamax(game, ply, depth, alpha, beta, start_time, time_limit):
    if time.time() - start_time > time_limit:
        return evaluate(game), None

    if depth == 0:
        return quiescence(game, ply, alpha, beta, start_time, time_limit)
    
    if is_threefold(game.fen_history):
        return DRAW_EVAL, None

    moves = list(game.get_moves())
    if len(moves) == 0:
        # Calculate whether the king is in check
        us = game.state.player
        king_piece, them = {"w": ("K", "b"), "b": ("k", "w")}.get(us)
        king_location = Game.i2xy(game.board.find_piece(king_piece))
        in_check = bool(
            [m[2:] for m in game._all_moves(player=them) if m[2:] == king_location]
        )

        # Stalemate
        if not in_check:
            return DRAW_EVAL, None

        # Prioritize shorter mates
        return -MAX_EVAL + ply, None
    
    best_value = -MAX_EVAL
    best_move = None

    original_fen = game.get_fen()
    fen_history_reference = game.fen_history.copy()

    for move in moves:
        game.apply_move(move)
        value, _ = negamax(game, ply + 1, depth - 1, -beta, -alpha, start_time, time_limit)
        value = -value

        game.set_fen(original_fen)
        game.fen_history = fen_history_reference.copy()

        if value > best_value:
            best_value = value
            best_move = move

        if best_value > alpha:
            alpha = best_value
            if alpha >= beta:
                break

    return best_value, best_move


def is_endgame(game):
    if game.state.player == 'w':
        board_str = str(game.board)
        minor_pieces = 0
        queen = 0
        for char in board_str:
            if char.islower():
                if char not in ['k', 'r']:
                    minor_pieces += 1
                    if char == 'q':
                        queen += 1
        if queen >= 1 and minor_pieces > 3:
            return False
        elif minor_pieces > 4:
            return False
        return True
    else:
        board_str = str(game.board)
        minor_pieces = 0
        queen = 0
        for char in board_str:
            if char.isupper():
                if char not in ['K', 'R']:
                    minor_pieces += 1
                    if char == 'Q':
                        queen += 1
        if queen >= 1 and minor_pieces > 3:
            return False
        elif minor_pieces > 4:
            return False
        return True


def enhanced_heuristic_with_time_limit(obs, per_move_time, remaining_time):
    game = Game(obs.board)
    moves = list(game.get_moves())
    random.shuffle(moves) 
    best_score = float('-inf')
    best_move = None
    start_time = time.time()

    for move in moves:
        move_start = time.time()
        elapsed = move_start - start_time
        remaining = remaining_time - elapsed
        if remaining <= 0:
            break 

        if elapsed >= per_move_time:
            continue

        move_score = 0
        from_square = move[:2]
        to_square = move[2:4]

        new_game = Game(str(game))
        new_game.apply_move(move)

        if new_game.status == Game.CHECKMATE:
            return move

        piece_moved = game.board.get_piece(Game.xy2i(from_square))
        target_piece = game.board.get_piece(Game.xy2i(to_square))

        if target_piece != ' ':
            capture_value = MATERIAL_VALUE[target_piece.upper()]
            move_score += capture_value * 100 
            piece_value = MATERIAL_VALUE.get(piece_moved.upper(), 0)
            net_gain = capture_value - piece_value
            move_score += net_gain * 50 

        if 'q' in move.lower():
            move_score += MATERIAL_VALUE['Q'] * 100 


        if to_square in ['d4', 'e4', 'd5', 'e5']:
            move_score += 20

        if new_game.status == Game.CHECK:
            move_score += 30
            
        opponent_moves = list(new_game.get_moves())
        for opp_move in opponent_moves:
            opp_target_square = opp_move[2:4]
            own_piece = new_game.board.get_piece(Game.xy2i(opp_target_square))
            if own_piece != ' ' and own_piece.isupper(): 
                endangered_piece_value = MATERIAL_VALUE.get(own_piece.upper(), 0)
                move_score -= endangered_piece_value * 100 

        if move_score > best_score:
            best_score = move_score
            best_move = move

        move_end = time.time()
    return best_move if best_score > float('-inf') else None

def hybrid_chess_bot(obs):
    game = Game(obs.board)
    perspective = game.state.player
    start_time = time.time()
    time_limit = 0.08
    best_move = None
    moves = list(game.get_moves())
    fen_history = [game.get_fen()]
    if is_endgame(game):
        return enhanced_heuristic_with_time_limit(obs, 0.09, time_limit)
    else:
        depth = 1
        while depth <= 3:
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_limit:
                break
            _ , move = negamax(game,0, depth, float('-inf'), float('inf'), start_time, time_limit)
            if move:
                best_move = move
            depth += 1
        if best_move:
            return best_move
        else:
            elapsed_time = time.time() - start_time
            if elapsed_time < time_limit:
                return enhanced_heuristic_with_time_limit(obs, 0.015, time_limit - elapsed_time)
            else:
                return random.choice(moves)
            
def agent(obs, config):
    return hybrid_chess_bot(obs)