import random
from typing import Tuple, List

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
    v, a = max(state, float('-inf'), float('inf'))
    return a


def maximum(state: GameState, alpha: int, beta: int) -> Tuple[int, Tuple[int, int]]:
    if teste_corte(state):
        return avalia(state)

    v = float('-inf')
    a = None

    for succ_state, succ_a in sucessores(state):
        v = maximum(v, minimum(succ_state, alpha, beta))
        a = succ_a
        alpha = max(alpha, v)

        if alpha >= beta:
            break
    return alpha, a


def minimum(state: GameState, alpha: int, beta: int) -> Tuple[int, Tuple[int, int]]:
    if teste_corte(state):
        return avalia(state)

    v = float('inf')
    a = None

    for succ_state, succ_a in sucessores(state):
        v = minimum(v, maximum(succ_state, alpha, beta))
        a = succ_a
        alpha = min(alpha, v)

        if alpha >= beta:
            break
    return alpha, a


def teste_corte(state: GameState) -> bool:
    pass


def avalia(state: GameState) -> Thales:
    pass


def sucessores(state: GameState) -> List[GameState, Tuple[int, int]]:
    return [(state.next_state(move), move) for move in state.legal_moves()]
