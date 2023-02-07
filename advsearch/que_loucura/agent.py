import random
import math
from timeit import default_timer as timer
from typing import Tuple

from ..othello.gamestate import GameState
from ..othello.board import Board

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

clock = 0
iters = 10

prune_over = 7
w1 = 0.1
w2 = 1
w3 = 2

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def alpha_beta_setup(state: GameState, depth: int) -> Tuple[Tuple[int,int], float]:
    global eval_f
    global max_player
    global min_player
    max_player = state.player
    min_player = state.get_board().opponent(max_player)
    alpha_beta = AlphaBeta
    return alpha_beta(state, depth)

def eval_execute(state: GameState) -> float:
    board = state.get_board()
    total_w = w1+w2+w3
    normal = (w1 * coin_parity(board) + w2 * (actual_mobility(board) + potential_mobility(board)) + w3 * corners(board))/(total_w)
    return normal

def coin_parity(board: Board) -> float:
    delta = board.num_pieces(max_player) - board.num_pieces(min_player)
    total = board.num_pieces(max_player) + board.num_pieces(min_player)
    return (delta/total)

def actual_mobility(board:Board) -> float:
    max_mobility = len(board.legal_moves(max_player))
    min_mobility = len(board.legal_moves(min_player))
    if(max_mobility + min_mobility) != 0:
        return (max_mobility - min_mobility) / (max_mobility + min_mobility)
    return 0

def potential_mobility(board:Board) -> float:
    max_mobility = 0
    min_mobility = 0
    for x in range(8):
        for y in range(8):
            if board.tiles[x][y] == max_player:
                for direction in Board.DIRECTIONS:
                    dx, dy = direction
                    if board.tiles[dx][dy] == '.':
                        max_mobility += 1
            if board.tiles[x][y] == min_player:
                for direction in Board.DIRECTIONS:
                    dx,dy = direction
                    if board.tiles[dx][dy] == '.':
                        min_mobility += 1
    if (max_mobility + min_mobility) != 0:
        v = (max_mobility - min_mobility) / (max_mobility + min_mobility)
        return v
    return 0

def corners(board: Board) -> float:
    tiles = board.tiles
    max_corners = 0
    min_corners = 0
    corner_coor = [(0,0), (0,7), (7,0), (7,7)]
    for x,y in corner_coor:
        if tiles[x][y] == max_player:
            max_corners += 10
        if tiles[x][y] == min_player:
            min_corners += 10
        if (x,y) in board.legal_moves(max_player):
            max_corners += 3
        if(x,y) in board.legal_moves(min_player):
            min_corners += 3
    if (max_corners + min_corners) != 0:
        return (max_corners - min_corners) / (max_corners + min_corners)
    return 0

max_player = None
min_player = None
eval_f = eval_execute
alpha_beta = alpha_beta_setup

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Returns an Othello move
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada com as pretas.
    # Remova-o e coloque a sua implementacao da poda alpha-beta
    #return random.choice([(2, 3), (4, 5), (5, 4), (3, 2)])
    global clock, iters
    clock = timer()
    move, v = alpha_beta(state, iters)
    

    if timer() - clock <= 4.5:
        iters = iters+1
    else:
        iters = max(5, iters-1)
    
    return move

def AlphaBeta(state: GameState, depth: int) -> Tuple[Tuple[int,int], float]:
    # Shared variables
    transp_table = dict()

    def max_val(state: GameState, alpha:float, beta:float, depth:int):

        # Leaf?
        if(state.is_terminal()):
            return 1000 if state.winner() == max_player else -1000
        # Max depth?
        if(depth <= 0 or timer() - clock > 4.5):
            return eval_f(state)
        v = -math.inf

        moves = state.legal_moves()
        ordered_moves = []
        for move in moves:
            val = eval_f(state.next_state(move))
            ordered_moves.append((val, move))
        
        # Search high-value moves first
        ordered_moves.sort(reverse=True)

        # Aggressively cuts low-performers
        if len(ordered_moves) > prune_over:
            ordered_moves = ordered_moves[0:prune_over]

        for _, a in ordered_moves:
            if timer() - clock > 4.5:
                return v
            n_state = state.next_state(a)
            n_board = str(n_state.get_board)
            if n_board in transp_table:
                v2 = transp_table[n_board]
            else:
                v2 = min_val(n_state, alpha, beta, depth-1)
                transp_table[n_board] = v2
            if v2 > v:
                v = v2
                alpha = max(alpha, v)
            if v >= beta:
                return v
        return v
        
    def min_val(state, alpha, beta, depth):
        
        # Leaf?
        if(state.is_terminal()):
            return -1000 if state.winner() == min_player else 1000
        # Max depth?
        if(depth <= 0 or timer() - clock > 4):
            return eval_f(state)
        
        v = math.inf
        
        moves = state.legal_moves()
        ordered_moves = []
        for move in moves:
            val = eval_f(state.next_state(move))
            ordered_moves.append((val, move))
        
        # Search low-value moves first
        ordered_moves.sort()
        
        # Aggressively cuts low-performers
        if len(ordered_moves) > prune_over:
            ordered_moves = ordered_moves[0:prune_over]
        
        for _, a in ordered_moves:
            if timer() - clock > 4:
                return v
            n_state = state.next_state(a)
            n_board = str(state.get_board())
            if n_board in transp_table:
                v2 = transp_table[n_board]
            else:
                v2 = max_val(n_state, alpha, beta, depth-1)
                transp_table[n_board] = v2
            if v2 < v:
                v = v2
                beta = min(beta, v)
            if v <= alpha:
                return v
        return v
    
    # Body of function
    v = -math.inf
    beta = math.inf
    best_action = None

    moves = state.legal_moves()
    if not moves:
        return (-1,-1), -math.inf
    
    ordered_moves = []
    for move in moves:
        val = eval_f(state.next_state(move))
        ordered_moves.append((val, move))
    
    # Search high-value moves first
    ordered_moves.sort(reverse=True)
    for _, a in ordered_moves:
        n_state = state.next_state(a)
        n_board = str(n_state.get_board)
        if n_board in transp_table:
            v2 = transp_table[n_board]
        else:
            v2 = min_val(n_state, v, beta, depth-1)
            transp_table[n_board] = v2
        if v2 > v:
            v = v2
            best_action = a
    
    return (best_action, v)