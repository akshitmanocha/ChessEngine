from chess_engine import agent
import chess
import chess.engine
import random
from elote import EloCompetitor
from elote import LambdaArena
from fractions import Fraction
from tqdm import tqdm
import numpy as np

engine_path = "/kaggle/working/stockfish/stockfish-ubuntu-x86-64-avx2"  # Update the path if necessary
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

class StockFish_BOT:
    def __init__(self, percentage_random_moves=0, time_limit=1, engine=None):
        if engine is None:
            engine = chess.engine.SimpleEngine.popen_uci("/kaggle/working/stockfish/stockfish-ubuntu-x86-64-avx2")
        else:
            self.engine = engine
        self.rnd_chance = max(min(percentage_random_moves, 1), 0)
        self.time_limit = time_limit
        self.limit = chess.engine.Limit(time=time_limit)
        self.elo = EloCompetitor(initial_rating=400)
        self.dilution_ratio = Fraction(self.rnd_chance/(1.01-self.rnd_chance)).limit_denominator(100)

    def make_move(self, board):
        if random.random() < self.rnd_chance:
            return random.choice(list(board.legal_moves))
        else:
            return engine.play(board, self.limit).move

    def __repr__(self):
        return f"Stockfish Bot - Thinking Time: {self.time_limit} Seconds - Diluted at {self.dilution_ratio} - Random move chance {round(self.rnd_chance, 2)*100}%"


class Benchmark:
    def __init__(self, num_baseline_players=10, baseline_player_time_limit=0.01, baseline_engine=None, use_random_percentages=False):
        self.arena = LambdaArena(self.play_game)
        self.num_baseline_players = num_baseline_players
        self.baseline_player_time_limit = baseline_player_time_limit
        if use_random_percentages:
            self.players = [StockFish_BOT(percentage_random_moves = random.random(), time_limit=self.baseline_player_time_limit, engine=baseline_engine) for _ in tqdm(range(self.num_baseline_players))]
        else:
            values = np.linspace(0, 1, self.num_baseline_players)
            self.players = [StockFish_BOT(percentage_random_moves = p, time_limit=self.baseline_player_time_limit, engine=baseline_engine) for p in tqdm(values)]
        

    def add_test_player(self, player):
        self.players.append(player)
    
    def play_game(self, player1, player2):
        board = chess.Board()
        board.push(random.choice(list(board.legal_moves)))
        done = False
    
        while not done:
            board.push(player2.make_move(board))
            
            outcome = board.outcome(claim_draw=True)
            if outcome is not None:
                return outcome.winner
    
            board.push(player1.make_move(board))
            
            outcome = board.outcome(claim_draw=True)
            if outcome is not None:
                return outcome.winner

    def run_games(self, num_games=10):
        matchups = [tuple(random.choices(self.players, k = 2)) for _ in range(num_games)]
        self.arena.tournament(matchups)

    def return_leaderboard(self):
        leaderboard = self.arena.leaderboard()

        min_score = min([i["rating"] for i in leaderboard])

        for player in leaderboard:
            player["rating"] = round((player["rating"] - min_score)+100, 2)

        return leaderboard
    
class CustomAgent:
    def __init__(self):
        self.elo = EloCompetitor(initial_rating=400)
        
    def make_move(self, board):
        # Convert chess.Board to the observation format your agent expects
        class Observation:
            def __init__(self, board):
                self.board = board.fen()
        
        obs = Observation(board)
        
        # Get move from your agent
        move_str = agent(obs, None)  # None for config since it's not used
        
        # Convert string move to chess.Move
        move = chess.Move.from_uci(move_str)
        return move
        
    def __repr__(self):
        return "Custom Chess Agent"

# Modify the benchmark code to test your agent
benchmark = Benchmark(num_baseline_players=50, baseline_player_time_limit=0.01, baseline_engine=engine, use_random_percentages=False)
benchmark.add_test_player(CustomAgent())  # Add your agent
benchmark.run_games(num_games=100)
print(benchmark.return_leaderboard())
