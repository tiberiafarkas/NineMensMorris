from copy import deepcopy
from random import choice
from turtledemo.penrose import start

from numpy.ma.extras import atleast_1d

from services.game import Game
from services.game_exceptions import AdjError, PlayerError


class SmartComputer:
    def __init__(self, game: Game, game_mode):
        self.__game = game
        self.game_mode = game_mode

    """
    how we reward our ai:
    1. if ai blocks opponent morris -> +600p
    2. if ai forms morris -> +400p
    3. if ai forms open morris -> +1000p
    4. if ai gets 2 pieces in a row -> +200p
    5. if ai blocks opponent 2 pieces in a row -> +300p

    for removing opponent piece:
    1. remove piece in morris if the opponent has only morris -> +500p
    2. remove piece which can help form morris -> +600p
    3. remove piece which can block your morris -> +500p
    4. remove piece where there are 2 in a row -> +400p
    5. remove random piece -> +100p
    """

    def check_own_morris(self, board_state, row, col):
        # board_state = deepcopy(self.__game._board._data)
        board_state[row][col] = self.player
        return self.__game.check_mill(board_state, row, col, self.player)

    def check_opponent_morris(self, board_state, row, col):
        # board_state = deepcopy(self.__game._board._data)
        board_state[row][col] = 3 - self.player
        return self.__game.check_mill(board_state, row, col, 3 - self.player)

    def can_get_morris(self):
        """
        checks if the player can form a morris
        :return: position of the morris and the points
        """
        for pos in self.__game._VALID_POSITIONS:
            try:
                self.__game.can_place_piece(pos[0], pos[1])
                board_state = deepcopy(self.__game._board._data)
                ok = self.check_own_morris(board_state, pos[0], pos[1])
                if ok:
                    return pos, 500
            except (ValueError, AdjError, PlayerError):
                pass

        return 0, 0

    def can_block_opponent_morris_in_place(self):
        """
        checks if the player can block the opponent from forming a morris
        :return:
        """
        for pos in self.__game._VALID_POSITIONS:
            try:
                self.__game.can_place_piece(pos[0], pos[1])
                board_state = deepcopy(self.__game._board._data)
                ok = self.check_opponent_morris(board_state, pos[0], pos[1])
                if ok:
                    return pos, 600
            except (ValueError, AdjError, PlayerError):
                pass

        return 0, 0

    def can_get_2_pieces_in_a_row(self):
        """
        checks if the player can get 2 pieces in a row
        :return:
        """
        for pos in self.__game.black_pieces if self.player == 2 else self.__game.white_pieces:
            for adj in self.__game._ADJ[pos]:
                try:
                    self.__game.can_place_piece(adj[0], adj[1])
                    return adj, 200
                except (ValueError, AdjError, PlayerError):
                    pass
        return 0, 0

    def can_block_opponent_2_pieces_in_a_row(self):
        """
        checks if the player can block the opponent from getting 2 pieces in a row
        :return:
        """
        for pos in self.__game.black_pieces if self.player == 1 else self.__game.white_pieces:
            for adj in self.__game._ADJ[pos]:
                try:
                    self.__game.can_place_piece(adj[0], adj[1])
                    return adj, 300
                except (ValueError, AdjError, PlayerError):
                    pass
        return 0, 0

    def points_systems_place_stage(self):
        """
        the points system for the placing stage
        :return:
        """
        position = -1
        points = 0
        pos, p = self.can_get_morris()
        if p > points:
            points = p
            position = pos
        pos, p = self.can_block_opponent_morris_in_place()
        if p > points:
            points = p
            position = pos
        pos, p = self.can_get_2_pieces_in_a_row()
        if p > points:
            points = p
            position = pos
        pos, p = self.can_block_opponent_2_pieces_in_a_row()
        if p > points:
            points = p
            position = pos
        return position

    def check_all_pieces_in_mills(self, player):
        """
        checks if all the pieces are in mills
        :return:
        """
        for pos in self.__game.black_pieces if player == 2 else self.__game.white_pieces:
            board_state = deepcopy(self.__game._board._data)
            if not self.check_own_morris(board_state, pos[0], pos[1]):
                return False
        return True

    def remove_piece_from_mill(self, player):
        """
        removes a piece from a mill
        :return:
        """
        opponent = 3 - player
        check_mill = self.check_all_pieces_in_mills(opponent)
        if check_mill:
            pos = choice(self.__game.black_pieces if opponent == 2 else self.__game.white_pieces)
            # self.board[pos[0]][pos[1]] = 0
            if pos in self.__game.valid_remove_piece(player):
                return pos, 500
        return 0, 0

    def remove_piece_2_in_a_row(self, player):
        """
        removes a piece where there are 2 in a row
        :return:
        """
        for pos in self.__game.black_pieces if player == 1 else self.__game.white_pieces:
            for adj in self.__game._ADJ[pos]:
                if adj in self.__game.black_pieces if player == 1 else self.__game.white_pieces:
                    if adj in self.__game.valid_remove_piece(player):
                        return adj, 400
        return 0, 0

    def remove_piece_blocked_morris(self, player):
        """
        removes a piece which can block a morris
        :return:
        """
        for pos in self.__game.black_pieces if player == 1 else self.__game.white_pieces:
            for adj in self.__game._ADJ[pos]:
                if self.__game._board._data[adj[0]][adj[1]] == 3 - player:
                    if adj in self.__game.valid_remove_piece(player):
                        return adj, 500
        return 0, 0

    def remove_random_piece(self, player):
        """
        removes a random piece
        :return:
        """
        pos = choice(self.__game.black_pieces if player == 1 else self.__game.white_pieces)
        if pos in self.__game.valid_remove_piece(player):
            return pos, 100
        return 0, 0

    def points_removal(self):
        """
        the points system for the removal stage
        :return:
        """
        position = -1
        points = 0
        pos, p = self.remove_piece_from_mill(self.player)
        if p > points:
            points = p
            position = pos
        pos, p = self.remove_piece_2_in_a_row(self.player)
        if p > points:
            points = p
            position = pos
        pos, p = self.remove_piece_blocked_morris(self.player)
        if p > points:
            points = p
            position = pos
        pos, p = self.remove_random_piece(self.player)
        if p > points:
            points = p
            position = pos
        return position

    def remove_piece(self, player):
        """
        removes an opponent piece
        :return:
        """
        self.player = player
        pos = self.points_removal()
        # self.board[pos[0]][pos[1]] = 0
        return pos

    def place_piece(self, player):
        """
        moves a piece
        :return:
        """
        self.player = player
        pos = self.points_systems_place_stage()
        return pos
        # self.__game.place_piece(pos[0], pos[1], self.player, self.game_mode)

    """
    reward ai for move stage:
    1. if ai forms morris -> +500p
    2. if ai blocks opponent morris -> +600p
    3. if ai can block opponent 2 in a row -> +300p
    4. if ai can form 2 in a row -> +400p
    5. if you can move 1 piece randomly -> +100p
    6. the only remained valid move is to move from morris -> 50p
    """

    def can_form_morris(self, current_positon):
        """
        checks if the player can form a morris
        :return:
        """
        pos = self.__game._ADJ[current_positon]
        for adj in pos:
            # for adj in self.__game._ADJ[pos]:
            try:
                self.__game.can_place_piece(adj[0], adj[1])
                board_state = deepcopy(self.__game._board._data)
                board_state[current_positon[0]][current_positon[1]] = 0
                ok = self.check_own_morris(board_state, adj[0], adj[1])
                if ok:
                    return adj, 600
            except (ValueError, AdjError, PlayerError):
                pass
        return 0, 0

    def can_block_opponent_morris(self, current_position):
        """
        checks if the player can block the opponent from forming a morris
        :return:
        """
        pos = self.__game._ADJ[current_position]
        for adj in pos:
            #   for adj in self.__game._ADJ[pos]:
            try:
                self.__game.can_place_piece(adj[0], adj[1])
                board_state = deepcopy(self.__game._board._data)
                board_state[current_position[0]][current_position[1]] = 0
                ok = self.check_opponent_morris(board_state, adj[0], adj[1])
                if ok:
                    return adj, 500
            except (ValueError, AdjError, PlayerError):
                pass
        return 0, 0

    def can_block_opponent_2_in_a_row(self, current_position):
        """
        checks if the player can block the opponent from getting 2 in a row
        :return:
        """
        pos = self.__game._ADJ[current_position]
        for adj in pos:
            try:
                self.__game.can_place_piece(adj[0], adj[1])
                for adj2 in self.__game._ADJ[adj]:
                    if adj2 in self.__game.black_pieces if self.player == 1 else self.__game.white_pieces:
                        return adj2, 300
            except (ValueError, AdjError, PlayerError):
                pass
        return 0, 0

    def can_form_2_in_a_row(self, current_position):
        """
        checks if the player can get 2 in a row
        :return:
        """
        pos = self.__game._ADJ[current_position]
        for adj in pos:
            try:
                self.__game.can_place_piece(adj[0], adj[1])
                for adj2 in self.__game._ADJ[adj]:
                    if adj2 in self.__game.black_pieces if self.player == 2 else self.__game.white_pieces:
                        return adj2, 400
            except (ValueError, AdjError, PlayerError):
                pass
        return 0, 0

    def can_move_random_piece(self, current_position):
        """
        moves a random piece
        :return:
        """
        for adj in self.__game._ADJ[current_position]:
            try:
                self.__game.can_place_piece(adj[0], adj[1])
                return adj, 100
            except (ValueError, AdjError, PlayerError):
                pass
        return 0, 0

    def points_system_move_stage(self):
        """
        the points system for the move stage
        :return:
        """
        final_position = -1
        points = 0
        start_position = -1
        for i in self.__game.black_pieces if self.player == 2 else self.__game.white_pieces:
            current_position = i
            pos, p = self.can_form_morris(current_position)
            # print("current position: ", current_position, "points: ", points)
            # print(pos, p)
            try:
                if p > points and self.__game.valid_move(current_position[0], current_position[1], pos[0], pos[1],
                                                         self.player, can_fly=False):
                    points = p
                    final_position = pos
                    start_position = current_position
                    # print("form morris")
            except (ValueError, AdjError, PlayerError) as ve:
                # print(ve)
                pass
            pos, p = self.can_block_opponent_morris(current_position)
            # print(pos, p)
            try:
                if p > points and self.__game.valid_move(current_position[0], current_position[1], pos[0], pos[1],
                                                         self.player, can_fly=False):
                    points = p
                    final_position = pos
                    start_position = current_position
                    # print("block morris")
            except (ValueError, AdjError, PlayerError) as ve:
                # print(ve)
                pass
            pos, p = self.can_block_opponent_2_in_a_row(current_position)
            # print(pos, p)
            try:
                if p > points and self.__game.valid_move(current_position[0], current_position[1], pos[0], pos[1],
                                                         self.player, can_fly=False):
                    points = p
                    final_position = pos
                    start_position = current_position
                    # print("block 2 in a row")
            except (ValueError, AdjError, PlayerError) as ve:
                # print(ve)
                pass
            pos, p = self.can_form_2_in_a_row(current_position)
            # print(pos, p)
            try:
                if p > points and self.__game.valid_move(current_position[0], current_position[1], pos[0], pos[1],
                                                         self.player, can_fly=False):
                    points = p
                    final_position = pos
                    start_position = current_position
                    # print("2 in a row")
            except (ValueError, AdjError, PlayerError) as ve:
                # print(ve)
                pass
            pos, p = self.can_move_random_piece(current_position)
            # print(pos, p)
            try:
                if p > points and self.__game.valid_move(current_position[0], current_position[1], pos[0], pos[1],
                                                         self.player, can_fly=False):
                    points = p
                    final_position = pos
                    start_position = current_position
                    # print("random")
            except (ValueError, AdjError, PlayerError) as ve:
                # print(ve)
                pass
        # print(start_position, final_position)
        return start_position, final_position

    def move_piece(self, player):
        """
        moves a piece
        :return:
        """
        self.player = player
        start_position, final_position = self.points_system_move_stage()
        return start_position, final_position
        # self.__game.move_piece(start_position[0], start_position[1], final_position[0], final_position[1], self.player, self.game_mode)

    """
    reward ai for fly stage:
    1. if ai forms morris -> +500p
    2. if ai blocks opponent morris -> +400p
    3. if ai can block opponent 2 in a row -> +200p
    4. if ai can form 2 in a row -> +300p
    5. if you can move 1 piece randomly -> +100p
    """

    def points_system_fly_stage(self):
        """
        the points system for the fly stage
        :return:
        """
        player_pieces = self.__game.black_pieces if self.player == 2 else self.__game.white_pieces
        piece1 = player_pieces[0]
        piece2 = player_pieces[1]
        piece3 = player_pieces[2]

        for mill in self.__game._MILLS:
            if piece1 in mill:
                if piece2 in mill:
                    for pos in mill:
                        try:
                            if pos != piece1 and pos != piece2 and self.__game.can_place_piece(pos[0], pos[1]):
                                return piece3, pos, 500
                        except (ValueError, AdjError, PlayerError):
                            pass

                if piece3 in mill:
                    for pos in mill:
                        try:
                            if pos != piece1 and pos != piece3 and self.__game.can_place_piece(pos[0], pos[1]):
                                return piece2, pos, 500
                        except (ValueError, AdjError, PlayerError):
                            pass

            if piece2 in mill:
                if piece3 in mill:
                    for pos in mill:
                        if pos != piece2 and pos != piece3 and self.__game.can_place_piece(pos[0], pos[1]):
                            return piece1, pos, 500

        for pos in self.__game._VALID_POSITIONS:
            try:
                self.__game.can_place_piece(pos[0], pos[1])
                board_state = deepcopy(self.__game._board._data)
                ok = self.check_opponent_morris(board_state, pos[0], pos[1])
                if ok:
                    return piece1, pos, 500
            except (ValueError, AdjError, PlayerError):
                pass

        for mill in self.__game._MILLS:
            if piece1 in mill and piece2 not in mill and piece3 not in mill:
                count = 0
                new_pos = -1
                for pos in mill:
                    try:
                        self.__game.can_place_piece(pos[0], pos[1])
                        count += 1
                        new_pos = pos
                    except (ValueError, AdjError, PlayerError):
                        pass

                if count == 2:
                    return piece3, new_pos, 400

            if piece2 in mill and piece1 not in mill and piece3 not in mill:
                count = 0
                new_pos = -1
                for pos in mill:
                    try:
                        self.__game.can_place_piece(pos[0], pos[1])
                        count += 1
                        new_pos = pos
                    except (ValueError, AdjError, PlayerError):
                        pass

                if count == 2:
                    return piece1, new_pos, 400

            if piece3 in mill and piece1 not in mill and piece2 not in mill:
                count = 0
                new_pos = -1
                for pos in mill:
                    try:
                        self.__game.can_place_piece(pos[0], pos[1])
                        count += 1
                        new_pos = pos
                    except (ValueError, AdjError, PlayerError):
                        pass

                if count == 2:
                    return piece2, new_pos, 400

            for pos in self.__game._VALID_POSITIONS:
                try:
                    self.__game.can_place_piece(pos[0], pos[1])
                    return piece1, pos, 100
                except (ValueError, AdjError, PlayerError):
                    pass

    def fly_piece(self, player):
        """
        moves a piece in fly stage
        :return:
        """
        self.player = player
        start_pos, end_pos, points = self.points_system_fly_stage()
        return start_pos, end_pos
        # self.__game.move_piece(start_pos[0], start_pos[1],end_pos[0], end_pos[1], self.player, self.game_mode)
