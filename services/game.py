# adjacency list for each intersection
from copy import deepcopy
from random import choice

from services.ai import AIPLayer
from domain.board import Board
from services.game_exceptions import AdjError, PlayerError

#TODO: daca face moara trebuie sa printeze prima data unde a mutat si apoi la ce piesa i-a dat remove atunci cand joaca pc-ul
#TODO: in lo ca make_move sa fie apelat din diferite clase, mai bine dau return la row si col si apelez din clasa game direct ca atunci cred ca mi-e mai usor si cu printatul

class Game(Board):
    def __init__(self, board: Board, graphic_mode, graphic):
        self._board = board
        self._white_pieces = []
        self._black_pieces = []
        self._white_mills = []
        self.black_mills = []
        self.graphic = graphic
        self.__graphic_mode = graphic_mode
        self._AIPlayer = AIPLayer(self, graphic)
        self._inv_coord = {
            1: "A",
            2: "B",
            3: "C",
            4: "D",
            5: "E",
            6: "F",
            7: "G",
        }
        self._ADJ = {(1, 1): [(1, 4), (4, 1)], (1, 4): [(1, 1), (1, 7), (2, 4)], (1, 7): [(1, 4), (4, 7)],
               (4, 7): [(1, 7), (7, 7), (4, 6)],
               (7, 7): [(4, 7), (7, 4)], (7, 4): [(7, 7), (7, 1), (6, 4)], (7, 1): [(7, 4), (4, 1)],
               (4, 1): [(7, 1), (1, 1), (4, 2)],
               (2, 2): [(2, 4), (4, 2)], (2, 4): [(2, 2), (2, 6), (1, 4), (3, 4)], (2, 6): [(2, 4), (4, 6)],
               (4, 6): [(2, 6), (6, 6), (4, 7), (4, 5)],
               (6, 6): [(4, 6), (6, 4)], (6, 4): [(6, 6), (6, 2), (7, 4), (5, 4)], (6, 2): [(6, 4), (4, 2)],
               (4, 2): [(6, 2), (2, 2), (4, 1), (4, 3)],
               (3, 3): [(3, 4), (4, 3)], (3, 4): [(3, 3), (3, 5), (2, 4)], (3, 5): [(3, 4), (4, 5)],
               (4, 5): [(3, 5), (5, 5), (4, 6)],
               (5, 5): [(4, 5), (5, 4)], (5, 4): [(5, 5), (5, 3), (6, 4)], (5, 3): [(5, 4), (4, 3)],
               (4, 3): [(5, 3), (3, 3), (4, 2)]
               }

        # list of mills
        self._MILLS = (((1, 1), (1, 4), (1, 7)), ((4, 1), (4, 2), (4, 3)), ((7, 1), (7, 4), (7, 7)),
                 ((2, 2), (2, 4), (2, 6)), ((2, 2), (4, 2), (6, 2)), ((6, 2), (6, 4), (6, 6)),
                 ((3, 3), (3, 4), (3, 5)), ((5, 3), (5, 4), (5, 5)), ((2, 6), (4, 6), (6, 6)),
                 ((1, 4), (2, 4), (3, 4)), ((3, 5), (4, 5), (5, 5)), ((1, 7), (4, 7), (7, 7)),
                 ((5, 4), (6, 4), (7, 4)), ((3, 3), (4, 3), (5, 3)), ((1, 1), (4, 1), (7, 1)),
                 ((4, 5), (4, 6), (4, 7))
                 )

        self._VALID_POSITIONS = [(1, 1), (1, 4), (1, 7),
                           (2, 2), (2, 4), (2, 6),
                           (3, 3), (3, 4), (3, 5),
                           (4, 1), (4, 2), (4, 3),
                           (4, 5), (4, 6), (4, 7),
                           (5, 3), (5, 4), (5, 5),
                           (6, 2), (6, 4), (6, 6),
                           (7, 1), (7, 4), (7, 7)]

    @property
    def black_pieces(self):
        return self._black_pieces

    @property
    def white_pieces(self):
        return self._white_pieces

    def can_place_piece(self, row, col):
        if row < 1 or row > 7 or col < 1 or col > 7 or (row, col) not in self._VALID_POSITIONS:
            raise ValueError("Invalid position")
        if self._board._data[row][col] != 0:
            raise ValueError("Position already occupied")

    def place_piece(self, row, col, player, game_mode):
        try:
            self.can_place_piece(row, col)
            self._board.update(row, col, player)
            if player == 1:
                self._white_pieces.append((row, col))
            else:
                self._black_pieces.append((row, col))

            self.is_mill(row, col, player, game_mode)
        except ValueError as ve:
            raise ve

    def valid_move(self, initial_row, initial_col, final_row, final_col, player, can_fly):
        try:
            self.can_place_piece(final_row, final_col)
        except ValueError as ve:
            raise ve

        if self._board._data[initial_row][initial_col] != player and self._board._data[initial_row][initial_col] != 0:
            raise PlayerError("This is the piece of the other player")

        if self._board._data[initial_row][initial_col] == 0:
            raise PlayerError(f"There is no piece at {self._inv_coord[initial_col]}{initial_row}")

        if (final_row, final_col) not in self._ADJ[(initial_row, initial_col)] and not can_fly:
            raise AdjError("Invalid move")

        print("True")
        return True

    def move_piece(self, initial_row, initial_col, final_row, final_col, player, game_mode):
        can_fly = True if ( len(self._white_pieces) == 3 and player == 1 ) or ( len(self._black_pieces) == 3 and player == 2 ) else False
        try:
            self.valid_move(initial_row, initial_col, final_row, final_col, player, can_fly)
            self._board.update(initial_row, initial_col, 0)
            self._board.update(final_row, final_col, player)
            if player == 1:
                self._white_pieces.remove((initial_row, initial_col))
                self._white_pieces.append((final_row, final_col))
            else:
                self._black_pieces.remove((initial_row, initial_col))
                self._black_pieces.append((final_row, final_col))

            self.is_mill(final_row, final_col, player, game_mode)
        except (ValueError, AdjError, PlayerError) as ve:
            raise ve

    def is_mill(self, row, col, player, game_mode):
        mill = self.check_mill(self._board._data, row, col, player)
        # print(f"White pieces: {self._white_pieces}")
        # print(f"Black pieces: {self._black_pieces}")
        if mill:
            if player == 1:
                self.remove_piece(1, game_mode)
            else:
                self.remove_piece(2, game_mode)

    def check_mill(self, board_state, row, col, player):
        """
        Checks if placing a piece at (row, col) will form a mill for the given player.

        :param board_state: The current state of the board (2D list).
        :param row: The row of the position being checked.
        :param col: The column of the position being checked.
        :param player: The player ID (1 for opponent, 2 for AI).
        :return: True if placing a piece forms a mill, False otherwise.
        """
        # Temporarily place the piece on the simulated board
        # print(row, col)
        new_state = deepcopy(board_state)
        new_state[row][col] = player

        for mill in self._MILLS:
            if (row, col) in mill:
                # Check if all 3 positions in the mill contain pieces from the same player
                if all(board_state[r][c] == player for r, c in mill):
                    self._white_mills.append(mill) if player == 1 else self.black_mills.append(mill)
                    return True
        return False

    def pieces_outside_mill(self, player):
        if player == 1:
            for piece in self._white_pieces:
                if not self.check_mill(self._board._data,piece[0], piece[1], player):
                    return True
        else:
            for piece in self._black_pieces:
                if not self.check_mill(self._board._data, piece[0], piece[1], player):
                    return True
        return False

    def valid_remove_piece(self, player):
        opponent = 2 if player == 1 else 1
        pieces_not_in_mill = self.pieces_outside_mill(opponent)
        valid_pieces = [
            piece for piece in (self._white_pieces if opponent == 1 else self._black_pieces)
            if not self.check_mill(self._board._data, piece[0], piece[1], opponent) or not pieces_not_in_mill
        ]
        return valid_pieces

    def best_piece_to_remove(self, player):
        # Get opponent player number
        opponent = 2 if player == 1 else 1

        # Call the AI player to get the best piece to remove based on evaluation
        best_piece = self._AIPlayer.best_piece_to_remove(player)

        # Return the coordinates of the best piece to remove
        return best_piece

    def get_remove_piece(self, player, game_mode):
        opponent = 2 if player == 1 else 1
        # pieces_not_in_mill = self.pieces_outside_mill(opponent)
        valid_pieces = self.valid_remove_piece(player)

        while True:
            try:
                if game_mode == "human_vs_human":
                    row, col = self.__graphic_mode.remove_piece(player, game_mode)

                elif game_mode == "human_vs_computer":
                    if self.graphic == "ui":
                        if player == 1:
                            row, col = self.__graphic_mode.remove_piece(player, game_mode)
                        else:
                            row, col = choice(valid_pieces)
                    else:
                        # print("in game valid pieces", valid_pieces)
                        row, col = self.__graphic_mode.remove_piece(player, game_mode)

                elif game_mode == "human_vs_ai":
                    if self.graphic == "ui":
                        if player == 1:
                            row, col = self.__graphic_mode.remove_piece(player, game_mode)
                        else:
                            row, col = self.best_piece_to_remove(player)
                    else:
                        row, col = self.__graphic_mode.remove_piece(player, game_mode)

                print("in game", row, col)
                if (row, col) in valid_pieces:
                    return row, col
                else:
                    print("Invalid piece")
            except (ValueError, AdjError):
                pass

    def remove_piece(self, player, game_mode):
        opponent = 2 if player == 1 else 1
        # while True:
        #     try:
        # if self.graphic == "ui":
        print(game_mode)
        row, col = self.get_remove_piece(player, game_mode)
        # else:
        #     row, col = self.__graphic_mode.remove_piece(player)

        # if (row, col) in valid_pieces:
        self._board.update(row, col, 0)
        if opponent == 1:
            if self.graphic == "ui":
                print(f"Player 2 removed piece at {self._inv_coord[col]}{row}")
            self._white_pieces.remove((row, col))
        else:
            if self.graphic == "ui":
                print(f"Player 1 removed piece at {self._inv_coord[col]}{row}")
            self._black_pieces.remove((row, col))

        if self.graphic == "ui":
            print(self._board)
            #     return
            # except (ValueError, AdjError):
            #     pass

    def check_moves_left(self, player):
        if player == 1:
            for piece in self._white_pieces:
                for adj in self._ADJ[piece]:
                    if self._board._data[adj[0]][adj[1]] == 0:
                        return True
        else:
            for piece in self._black_pieces:
                for adj in self._ADJ[piece]:
                    if self._board._data[adj[0]][adj[1]] == 0:
                        return True

        return False

#i could still use it if i want to add another option to play the game
class ComputerPlayer:
    def __init__(self, game: Game, graphic):
        self.__game = game
        self.__game_mode = "human_vs_computer"
        self.__graphic = graphic

    def place_on_board(self):
        while True:
            try:
                (row, col) = choice(self.__game._VALID_POSITIONS)
                self.__game.place_piece(row, col, 2, self.__game_mode)
                # return self.__game._inv_coord[col], row
                if self.__graphic == "ui":
                    print(f"Computer placed piece at {self.__game._inv_coord[col]}{row}")
                break
            except ValueError as ve:
                pass

        return row, col
        # self.__game.is_mill(row, col, 2, self.__game_mode)

    def move_computer(self):
        while True:
            try:
                initial_row, initial_col = choice(self.__game._black_pieces)
                if len(self.__game.black_pieces) > 3:
                    final_row, final_col = choice(self.__game._ADJ[(initial_row, initial_col)])
                else:
                    final_row, final_col = choice(self.__game._VALID_POSITIONS)
                self.__game.move_piece(initial_row, initial_col, final_row, final_col, 2, self.__game_mode)
                if self.__graphic == "ui":
                    print(f"Computer moved piece from {self.__game._inv_coord[initial_col]}{initial_row} to {self.__game._inv_coord[final_col]}{final_row}")
                break
            except (ValueError, AdjError) as er:
                pass

        return initial_row, initial_col, final_row, final_col
        # self.__game.is_mill(final_row, final_col, 2, self.__game_mode)
