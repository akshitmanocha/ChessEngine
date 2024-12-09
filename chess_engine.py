from Chessnut import Game
import time
import random

PIECE_VALUES = {"p": 1000, "n": 3000, "b": 3000, "r": 5000, "q": 9000, "k": 100000}
PIECE_TABLE = {
    'p': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
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

def evaluate_board(game, perspective):
    board_str = str(game.board)
    if perspective == 'w':
        constant = 1
    else:
        constant = -1
    score = 0
    row = 0
    col = 0
    for char in board_str:
        if char == '/':
            row += 1
            col = 0
        elif char.isdigit():
            col += int(char)
        elif char.isalpha():
            piece = char.lower()
            if char.isupper():
                piece_value = PIECE_VALUES[piece]
                position_value = PIECE_TABLE[piece][row][col]
                score += piece_value + position_value
            else:
                piece_value = PIECE_VALUES[piece]
                position_value = PIECE_TABLE[piece][7 - row][7 - col]
                score -= piece_value + position_value
            col += 1
    return constant*score

def minimax(game, depth, maximizingPlayer, perspective, start_time, time_limit):
    if time.time() - start_time > time_limit:
        return evaluate_board(game, perspective), None

    if depth == 0 or game.status == Game.CHECKMATE or game.status == Game.STALEMATE:
        return evaluate_board(game, perspective), None

    moves = list(game.get_moves())
    best_move = None

    if maximizingPlayer:
        max_eval = float('-inf')
        for move in moves:
            new_game = Game(str(game))
            new_game.apply_move(move)
            eval_score, _ = minimax(new_game, depth - 1, False, perspective, start_time, time_limit)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_game = Game(str(game))
            new_game.apply_move(move)
            eval_score, _ = minimax(new_game, depth - 1,True, perspective, start_time, time_limit)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move
    
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
            capture_value = PIECE_VALUES[target_piece.lower()]
            move_score += capture_value * 100 
            piece_value = PIECE_VALUES.get(piece_moved.lower(), 0)
            net_gain = capture_value - piece_value
            move_score += net_gain * 50 

        if 'q' in move.lower():
            move_score += PIECE_VALUES['q'] * 100 


        if to_square in ['d4', 'e4', 'd5', 'e5']:
            move_score += 20

        if new_game.status == Game.CHECK:
            move_score += 30
            
        opponent_moves = list(new_game.get_moves())
        for opp_move in opponent_moves:
            opp_target_square = opp_move[2:4]
            own_piece = new_game.board.get_piece(Game.xy2i(opp_target_square))
            if own_piece != ' ' and own_piece.isupper(): 
                endangered_piece_value = PIECE_VALUES.get(own_piece.lower(), 0)
                move_score -= endangered_piece_value * 100 

        if move_score > best_score:
            best_score = move_score
            best_move = move

        move_end = time.time()
    return best_move if best_score > float('-inf') else None


def hybrid_chess_bot(obs):
    game = Game(obs.board)
    perspective = game.state.player
    if perspective == 'w':
        start_time = time.time()
        time_limit = 0.07
        best_move = None
        moves = list(game.get_moves())
        transposition_table = {}
        if is_endgame(game):
            return enhanced_heuristic_with_time_limit(obs, 0.09, time_limit)
        else:
            depth = 1
            while depth <= 5:
                elapsed_time = time.time() - start_time
                if elapsed_time >= time_limit:
                    break
                eval_score, move = minimax(game, depth, float('-inf'), float('inf'), True, perspective, start_time, time_limit, transposition_table)
                if move:
                    best_move = move
                depth += 1
            if best_move:
                return best_move
            else:
                elapsed_time = time.time() - start_time
                if elapsed_time < time_limit:
                    return enhanced_heuristic_with_time_limit(obs,0.015, time_limit - elapsed_time)
                else:
                    return random.choice(moves)
    else:
        enhanced_heuristic_with_time_limit(obs, 0.09, time_limit)

def agent(obs, config):
    return hybrid_chess_bot(obs)