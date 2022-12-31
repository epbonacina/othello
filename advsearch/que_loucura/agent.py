import random
from typing import Tuple, Union

from ..othello.gamestate import GameState

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state: GameState) -> Tuple[int, int]:
    """
    Returns an Othello move
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    v, a = maximum(state, float('-inf'), float('inf'), 0)
    return a


def maximum(state: GameState, alpha: int, beta: int, depth: int) -> Tuple[int, Tuple[int, int]]:
    if teste_corte(depth):
        return avalia(state), (-1, -1)

    v = float('-inf')
    a = None

    for succ_state, succ_a in sucessores(state):
        v = max(v, minimum(succ_state, alpha, beta, depth+1)[0])
        a = succ_a
        alpha = max(alpha, v)

        if alpha >= beta:
            break
    return alpha, a


def minimum(state: GameState, alpha: int, beta: int, depth: int) -> Tuple[int, Tuple[int, int]]:
    if teste_corte(depth):
        return avalia(state), (-1, -1)

    v = float('inf')
    a = None

    for succ_state, succ_a in sucessores(state):
        v = min(v, maximum(succ_state, alpha, beta, depth+1)[0])
        a = succ_a
        beta = min(beta, v)

        if alpha >= beta:
            break
    return beta, a


def teste_corte(depth: int) -> bool:
    return depth >= 5


def avalia(state: GameState) -> int:
    player = state.player
    tiles = state.board.tiles

    qtt = 0
    for line in tiles:
        for piece in line:
            if piece == player:
                qtt += 1
    return qtt


def sucessores(state: GameState) -> Tuple[GameState, Tuple[int, int]]:
    return [(state.next_state(move), move) for move in state.legal_moves()]

