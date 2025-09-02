from copy import deepcopy
from services.game import Game
INF = 1000000000

class State(object):
    def __init__(self, board, game, parent, player, nextstate=None):
        if nextstate is None:
            nextstate = []

        self.board = board
        self.__game = game
        self.parent = parent
        self.nextstate = nextstate
        self.player = player

    def is_terminal_state(self):
        ai_lose = not self.__game.check_moves_left(player=1)
        player_lose = not self.__game.check_moves_left(player=2)
        self.ai_lose = (not player_lose)
        return ai_lose or player_lose

    def get_terminal_state_value(self):
        if self.ai_lose:
            return -INF
        return INF

    def next_states_place(self):
        for pos in self.__game._VALID_POSITIONS():
            boardcopy = deepcopy(self.board)
            if self.player == 1:
                boardcopy[pos[0]][pos[1]] = 1
            else:
                boardcopy[pos[0]][pos[1]] = 2
            self.nextstate.append(State(boardcopy, self.__game, pos, player=3 - self.player, self))

    def next_states_move(self):
        for pos in self.__game._VALID_POSITIONS():
            for move in self.__game.(pos):
                boardcopy = deepcopy(self.board)
                boardcopy[move[0]][move[1]] = self.player
                boardcopy[pos[0]][pos[1]] = 0
                self.nextstate.append(State(boardcopy, self.__game, move, player=3 - self.player, self))
