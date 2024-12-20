from Chessnut import Game
from collections import Counter
import random
import pygame

PIECE_VALUES = {
    "p": 100,
    "n": 300,
    "b": 300,
    "r": 500,
    "q": 900,
    "k": 1000000
}
PIECE_TABLE = {
    'p': [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50,50, 50, 50, 50, 50, 50, 50],
        [10,10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5, 5],
        [0,  0,  0, 20, 20,  0,  0, 0],
        [5, -5,-10,  0,  0,-10, -5, 5],
        [5, 10, 10,-20,-20, 10, 10, 5],
        [0,  0,  0,  0,  0,  0,  0, 0]
    ],
    'n': [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ],
    'b': [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ],
    'r': [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ],
    'q': [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ],
    'k': [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20]
    ]
}
ENDGAME_PIECE_TABLE = {
    'p': [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50,50, 50, 50, 50, 50, 50, 50],
        [10,10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5, 5],
        [0,  0,  0, 20, 20,  0,  0, 0],
        [5, -5,-10,  0,  0,-10, -5, 5],
        [5, 10, 10,-20,-20, 10, 10, 5],
        [0,  0,  0,  0,  0,  0,  0, 0]
    ],
    'n': [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ],
    'b': [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ],
    'r': [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ],
    'q': [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ],
    'k': [
        [-50, -40, -30, -20, -20, -30, -40, -50],
        [-30, -20, -10,   0,   0, -10, -20, -30],
        [-30, -10,  20,  30,  30,  20, -10, -30],
        [-30, -10,  30,  40,  40,  30, -10, -30],
        [-30, -10,  30,  40,  40,  30, -10, -30],
        [-30, -10,  20,  30,  30,  20, -10, -30],
        [-30, -30,   0,   0,   0,   0, -30, -30],
        [-50, -30, -30, -30, -30, -30, -30, -50]
    ]
}

def evaluate_material(board, is_endgame=False):
    material_score = 0
    for piece, count in Counter(board).items():
        piece_value = PIECE_VALUES[piece.lower()]
        material_score += piece_value * (1 if piece.isupper() else -1)
    return material_score


def evaluate_position(board, is_endgame=False):
    table = ENDGAME_PIECE_TABLE if is_endgame else PIECE_TABLE
    position_score = 0
    for square, piece in enumerate(board):
        if piece.lower() in table:
            row, col = square // 8, square % 8
            if piece.isupper():
                position_score += table[piece.lower()][row][col]
            else:
                position_score -= table[piece.lower()][7 - row][col]
    return position_score

def evaluate(board, is_endgame=False):
    material = evaluate_material(board, is_endgame)
    position = evaluate_position(board, is_endgame)
    return material + position

def is_capture(game, move):
    to_square = move[2:]
    captured_piece = game.board.get_piece(Game.xy2i(to_square))
    if captured_piece == ' ':
        return False
    return True

def get_capture_value(game, move):
    to_square = move[2:]
    captured_piece = game.board.get_piece(Game.xy2i(to_square))
    return PIECE_VALUES.get(captured_piece.lower(), 0)

def move_ordering(game, moves):
    ordered_moves = []
    for move in moves:
        if is_capture(game, move):
            captured = game.board.get_piece(Game.xy2i(move[2:])).lower()
            ordered_moves.append((PIECE_VALUES.get(captured, 0), move))
        else:
            ordered_moves.append((0, move))
    ordered_moves.sort(reverse=True, key=lambda x: x[0])
    return [move for _, move in ordered_moves]

def is_endgame(game):
    if game.state.player == 'w':
        board_str = str(game.board)
        minor_pieces = 0
        queen = 0
        for char in board_str:
            if char.islower():
                if char not in ['k']:
                    minor_pieces += 1
                    if char == 'q':
                        queen += 1
        if queen >= 1 and minor_pieces > 2:
            return False
        elif minor_pieces > 3:
            return False
        return True
    else:
        board_str = str(game.board)
        minor_pieces = 0
        queen = 0
        for char in board_str:
            if char.isupper():
                if char not in ['K']:
                    minor_pieces += 1
                    if char == 'Q':
                        queen += 1
        if queen >= 1 and minor_pieces > 2:
            return False
        elif minor_pieces > 3:
            return False
        return True

def quiescence(game, alpha, beta):
    stand_pat = evaluate(game)
    if stand_pat >= beta:
        return beta, None

    if alpha < stand_pat:
        alpha = stand_pat

    original_fen = game.get_fen()

    moves = move_ordering(game, game.get_moves())
    for move in moves:
        if is_capture(game, move):
            game.apply_move(move)
            score, _ = quiescence(game, -beta, -alpha)
            score = -score
            game.set_fen(original_fen)
            if score >= beta:
                return beta, None
            
            if score > alpha:
                alpha = score

    return alpha, None

def negamax(game, depth, alpha, beta):
    if depth == 0 or game.status >= 2:
        return quiescence(game, alpha, beta)

    original_fen = game.get_fen()
    best_score = float("-inf")
    best_move = None
    moves = move_ordering(game, game.get_moves())
    LATE_MOVE_THRESHOLD = 10  # Number of moves after which to apply LMP

    for idx, move in enumerate(moves):

        if idx >= LATE_MOVE_THRESHOLD:
            # Late Move Pruning
            game.apply_move(move)
            score, _ = negamax(game, depth - 1, -beta, -alpha)
            score = -score
            game.set_fen(original_fen)
            if score < alpha:
                continue  # Prune the move
        else:
            game.apply_move(move)

        if depth == 1 and not is_capture(game, move):
            # Futility pruning
            margin = 50  # Futility margin
            stand_pat = evaluate(game)
            if stand_pat + margin <= alpha:
                game.set_fen(original_fen)
                continue

            # Delta pruning
            if is_capture(game, move):
                delta = get_capture_value(game, move)
                if alpha + delta <= alpha:
                    game.set_fen(original_fen)
                    continue

        if idx == 0:
            # full window search
            score, _ = negamax(game, depth - 1, -beta, -alpha)
            score = -score
        else:
            # principal variation search
            score, _ = negamax(game, depth - 1, -alpha - 1, -alpha)
            score = -score
            if alpha < score < beta:
                # Search with full window
                score, _ = negamax(game, depth - 1, -beta, -alpha)
                score = -score

        game.set_fen(original_fen)

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return best_score, best_move

def make_move(game, depth=2):
    best_score, best_move = negamax(game, depth, float("-inf"), float("inf"))
    return best_move

class ChessGame():
    def __init__(self):
        self.game = Game()
        self.fen = self.game.get_fen()
        self.player = 'w'

    def move(self, move):
        if self.player == 'w':
            
    