#from game import Game

inf = 1000000000

class AIPLayer:
    def __init__(self, game, graphic):
        self.__game = game
        self.__game_mode = "human_vs_ai"
        self.graphic = graphic

    def place_on_board(self):
        # Use minimax to decide placement during the placement phase
        best_move = self.minimax_decision(placing = True)
        # print("best move:", best_move)
        row = best_move[0]
        col = best_move[1]
        #self.__game.place_piece(row, col, 2)  # 2 is the AI player
        self.__game.place_piece(row, col, 2, self.__game_mode)  # 2 is the AI player
        # print(f"AI placed piece at {self.__game._inv_coord[col]}{row}")
        self.__game.is_mill(row, col, 2, self.__game_mode)
        # self.__game.is_mill(row, col, 2, self.__game_mode)
        return row, col

    def move_piece(self):
        # Use minimax to decide a move during the moving phase
        best_move = self.minimax_decision(placing = False)
        if best_move == None:
            # print("AI could not find a move")
            return
        start, end = best_move
        #self.__game.move_piece(start[0], start[1], end[0], end[1], 2)  # 2 is the AI player
        self.__game.move_piece(start[0], start[1], end[0], end[1], 2, self.__game_mode)  # 2 is the AI player
        # print(f"AI moved piece from {self.__game._inv_coord[start[1]]}{start[0]} to {self.__game._inv_coord[end[1]]}{end[0]}")
        self.__game.is_mill(end[0], end[1], 2, self.__game_mode)
        # self.__game.is_mill(end[0], end[1], 2, self.__game_mode)
        return start, end

    def minimax_decision(self, placing):
        # Perform minimax decision-making to return the optimal move (row, col)
        # board_state = self.__game._board._data
        # board_state = self.__game._board._data
        board_state = [row[:] for row in self.__game._board._data]
        depth = 3  # Example depth for minimax
        maximizing_player = True
        best_value, best_move = self.minimax(board_state, depth, maximizing_player, float(-inf), float(inf), placing)
        return best_move

    def minimax(self, board_state, depth, maximizing_player, alpha, beta, placing):
        # Implement the minimax algorithm with alpha-beta pruning
        # print("yes")
        if depth == 0 or (self.is_terminal_state(board_state) and not placing):
            # print("terminal state ", self.is_terminal_state(board_state))
            # print("depth", depth)
            return self.evaluate_board(board_state, placing), None

        # print("no")
        if maximizing_player:
            max_eval = float(-inf)
            best_move = None
            # print("maxi")
            generating_moves = self.generate_moves(board_state, player=2, placing=placing)
            # print("generate moves - maximazing phase ", generating_moves)
            for move in generating_moves:  # Assuming player 2 is the AI
                # print("gets in")
                new_state = [row[:] for row in board_state]
                new_state = self.simulate_move(new_state, move, player=2, placing=placing)
                eval = self.minimax(new_state, depth - 1, False, alpha, beta, placing)[0]
                # print(eval)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                    # print(type(move))
                    # print(move)
                    # print(best_move)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float(inf)
            best_move = None
            # print("mini")
            generating_moves = self.generate_moves(board_state, player=1, placing=placing)
            # print("generate moves - minimazing phase ", generating_moves)
            for move in generating_moves:  # Assuming player 1 is human
                # print("gets in")
                new_state = [row[:] for row in board_state]
                new_state = self.simulate_move(new_state, move, player=1, placing=placing)
                eval = self.minimax(new_state, depth - 1, True, alpha, beta, placing)[0]
                # print(eval)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def is_fly_phase(self, board_state):
        return self.__game._black_pieces == 3

    def is_terminal_state(self, board_state):
        # Determine if the game is in a terminal state
        return not self.__game.check_moves_left(player=1) or not self.__game.check_moves_left(player=2)

    def evaluate_board(self, board_state, placing):
        # Initialize score
        score = 0

        # Evaluate mills (existing logic)
        score += 200 * self.evaluate_mills(board_state)

        # Evaluate piece positions (center control, safe pieces, etc.)
        score += 150 * self.evaluate_piece_positions(board_state, placing)

        # Evaluate piece mobility (number of available moves)
        score += 100 * self.evaluate_mobility(board_state)

        # Optional: Consider piece counts
        score += 50 * self.evaluate_piece_count(board_state)

        # Evaluate blocking opponent mills
        score +=  300 * self.evaluate_block_opponent_mill(board_state, placing)

        return score

    def evaluate_piece_positions(self, board_state, placing):
        score = 0
        if placing:
            # Prioritize forming mills or blocking opponent’s mill during placement phase
            for row in range(len(board_state)):
                for col in range(len(board_state[row])):
                    if board_state[row][col] == 2:  # AI's pieces (player 2)
                        # Check if the AI can complete a mill
                        if self.__game.check_mill(board_state, row, col, 2):
                            score += 150  # Forming a mill should be highly rewarded
                    elif board_state[row][col] == 1:  # Opponent's pieces (player 1)
                        # Check if the opponent is one move away from completing a mill
                        if self.__game.check_mill(board_state, row, col, 1):
                            score -= 200  # Penalize AI for letting opponent form a mill
        else:
            # In the movement phase, prioritize making a mill or blocking the opponent
            for row in range(len(board_state)):
                for col in range(len(board_state[row])):
                    if board_state[row][col] == 2:  # AI's pieces (player 2)
                        # 1. Check if moving the AI piece can form a mill
                        if self.__game.check_mill(board_state, row, col, 2):
                            score += 100  # Reward for forming a mill during movement phase
                            # 2. Look for opponent pieces forming a potential mill
                            for adj in self.__game._ADJ[(row, col)]:
                                if board_state[adj[0]][adj[1]] == 1:  # Opponent’s piece adjacent
                                    # Check for a potential third piece to form a mill
                                    for neighbor in self.__game._ADJ[(adj[0], adj[1])]:
                                        if board_state[neighbor[0]][neighbor[1]] == 0:  # Empty spot
                                            # Check if this empty spot completes a mill for the opponent
                                            temp_board = [row[:] for row in board_state]
                                            temp_board[neighbor[0]][neighbor[1]] = 1  # Simulate opponent's move
                                            if self.__game.check_mill(temp_board, neighbor[0], neighbor[1], 1):
                                                # Block this mill by moving AI’s piece to the empty spot
                                                temp_board[neighbor[0]][neighbor[1]] = 2  # Simulate AI's move

                                                # 3. Reward the AI for blocking the mill
                                                score += 120  # Arbitrary reward for blocking

                                                # 4. Check if this blocking move also forms a mill for the AI
                                                if self.__game.check_mill(temp_board, neighbor[0], neighbor[1], 2):
                                                    score += 50  # Additional reward for forming a mill
                                                break  # No need to check further for this position
        return score

    def evaluate_mobility(self, board_state):
        # Calculate mobility for both players
        ai_mobility = self.calculate_mobility(board_state, 2)
        human_mobility = self.calculate_mobility(board_state, 1)
        return ai_mobility - human_mobility  # More mobility is better for the AI

    def evaluate_block_opponent_mill(self, board_state, placing):
        score = 0
        for row in range(len(board_state)):
            for col in range(len(board_state[row])):
                if board_state[row][col] == 1:  # Opponent's pieces (player 1)
                    # Check if the opponent is one move away from forming a mill
                    for adj in self.__game._ADJ[(row, col)]:
                        if board_state[adj[0]][adj[1]] == 0:  # Empty spot adjacent to the piece
                            new_board_state = [row[:] for row in board_state]
                            new_board_state[adj[0]][adj[1]] = 1  # Place the opponent's piece
                            if self.__game.check_mill(new_board_state, adj[0], adj[1], 1):
                                if placing:
                                    # During placing, prioritize preventing the opponent's mill
                                    score -= 200  # Deduct points if we let the opponent form a mill
                                else:
                                    # During moving, only block if there's an actual threat
                                    score += 300  # Reward the AI for blocking the opponent’s mill
                elif board_state[row][col] == 2:  # AI's pieces (player 2)
                    if not placing:  # In movement phase
                        # Check if moving AI piece can block the opponent’s mill
                        for adj in self.__game._ADJ[(row, col)]:
                            if board_state[adj[0]][adj[1]] == 1:  # If the opponent’s piece is adjacent
                                for neighbor in self.__game._ADJ[(adj[0], adj[1])]:
                                    if board_state[neighbor[0]][neighbor[1]] == 0:  # Empty spot
                                        # Check if this empty spot completes a mill for the opponent
                                        temp_board = [row[:] for row in board_state]
                                        temp_board[neighbor[0]][neighbor[1]] = 1  # Simulate opponent's move
                                        if self.__game.check_mill(temp_board, neighbor[0], neighbor[1], 1):
                                            # Block this mill by moving AI’s piece to the empty spot
                                            temp_board[neighbor[0]][neighbor[1]] = 2  # Simulate AI's move

                                            # 3. Reward the AI for blocking the mill
                                            score += 100  # Arbitrary reward for blocking

                                            # 4. Check if this blocking move also forms a mill for the AI
                                            if self.__game.check_mill(temp_board, neighbor[0], neighbor[1], 2):
                                                score += 50  # Additional reward for forming a mill
                                            break  # No need to check further for this position
        return score

    def evaluate_piece_count(self, board_state):
        # Count the number of pieces for both players
        ai_pieces = sum(row.count(2) for row in board_state)
        human_pieces = sum(row.count(1) for row in board_state)
        return ai_pieces - human_pieces  # More pieces is better for the AI

    def position_value(self, row, col):
        # Center positions are more valuable (value them higher)
        center_positions = [(2, 4), (3, 4), (4, 3), (4, 6)]
        if (row, col) in center_positions:
            return 1  # Center positions have a high value
        elif (row == 0 or row == 6) and (col == 0 or col == 6):
            return -1  # Corners are less valuable
        return 0  # Otherwise, default value for position

    def calculate_mobility(self, board_state, player):
        # Calculate the number of valid moves for a player
        mobility = 0
        pieces = self.__game.black_pieces if player == 2 else self.__game.white_pieces
        for piece in pieces:
            for adj in self.__game._ADJ[piece]:  # Assuming ADJ is the list of adjacent positions
                if board_state[adj[0]][adj[1]] == 0:  # If position is empty
                    mobility += 10
        return mobility

    def evaluate_mills(self, board_state):
        # Check for mills and assign score
        score = 0
        # Loop through the pieces (either AI's or the opponent's)
        for row in range(len(board_state)):
            for col in range(len(board_state[row])):
                if board_state[row][col] == 2:  # AI's pieces (player 2)
                    if self.__game.check_mill(board_state, row, col, 2):  # Check if it's part of a mill
                        score += 100  # +10 for each mill the AI has
                        score += self.evaluate_mill_removal(board_state, row, col, 2)  # Update for piece removal strategy
                elif board_state[row][col] == 1:  # Human's pieces (player 1)
                    if self.__game.check_mill(board_state, row, col, 1):  # Check if it's part of a mill
                        score -= 200  # -10 for each mill the human has
        return score

    def best_piece_to_remove(self, player):
        # Get the board state
        board_state = self.__game._board._data
        possible_moves = self.__game.valid_remove_piece(player)

        # Evaluate the best piece for removal using the evaluate_mill_removal function
        best_value = float(-inf)
        best_piece = None

        block_prevention = self.prevent_opponent_block(board_state, player)

        for move in possible_moves:
            current_pos = move

            new_board_state = [row[:] for row in board_state]
            new_board_state[current_pos[0]][current_pos[1]] = 2

            # Check if this move results in a mill for the AI
            if self.__game.check_mill(new_board_state, current_pos[0], current_pos[1], 2):
                return move

            # Check if the move prevents the opponent from blocking a mill
            # if block_prevention and new_pos == block_prevention:
            #     return move  # Prioritize preventing opponent's block

            value = self.evaluate_mill_removal(board_state, move[0], move[1], player)
            if value > best_value:
                best_value = value
                best_piece = move

        # print(best_piece)
        return best_piece

    def prevent_opponent_block(self, board_state, player):
        """Evaluates potential opponent block scenarios and avoids them."""
        opponent = 1 if player == 2 else 2  # If placing, we’re worried about blocking player 1
        for row in range(len(board_state)):
            for col in range(len(board_state[row])):
                if board_state[row][col] == opponent:  # Opponent’s pieces
                    for adj in self.__game._ADJ[(row, col)]:
                        if board_state[adj[0]][adj[1]] == 0:  # Empty spot adjacent to the piece
                            new_board_state = [row[:] for row in board_state]
                            new_board_state[adj[0]][adj[1]] = opponent  # Place the opponent's piece
                            if self.__game.check_mill(new_board_state, adj[0], adj[1], opponent):
                                # prioritize preventing the opponent’s mill
                                return adj  # This is where the opponent might
        return None

    def evaluate_mill_removal(self, board_state, row, col, player):
        opponent = 1 if player == 2 else 2
        removable_pieces = self.__game.valid_remove_piece(player)
        # print(removable_pieces)

        if len(removable_pieces) == 0:
            return 0  # No pieces can be removed, so no reward

        best_value = float(-inf)
        best_piece = None

        # Iterate over all removable pieces to determine the best piece to remove
        for piece in removable_pieces:
            piece_row, piece_col = piece

            # Priority 1: Check if the piece can help the opponent form a mill in the next step
            if self.can_form_mill_in_next_move(board_state, piece_row, piece_col, opponent):
                # This piece should be prioritized for removal
                value = 50  # Arbitrary high value to prioritize this piece
            # Priority 2: Check if the piece can ruin an AI mill (by blocking the AI)
            elif self.can_block_ai_mill(board_state, piece_row, piece_col, player):
                value = 30  # Arbitrary value to prioritize blocking the AI's mill
            # Priority 3: Check the proximity of the piece to the AI’s pieces
            else:
                value = self.calculate_distance_to_ai(board_state, piece_row, piece_col)

            # Update best piece based on the value
            if value > best_value:
                best_value = value
                best_piece = piece

        if best_piece:
            # Returning a value for removing this piece (e.g., 5 for successfully removing a piece)
            return best_value  # Example value for removing the best piece
        return 0  # No significant piece to remove

    def can_form_mill_in_next_move(self, board_state, row, col, player):
        # Check if removing this piece will enable the opponent to form a mill in the next move
        # We need to check if the opponent can form a mill by placing a piece on an empty spot
        for adjacent in self.__game._ADJ[(row, col)]:
            if board_state[adjacent[0]][adjacent[1]] == 0:  # Adjacent empty spot
                # Simulate placing the opponent's piece in this spot
                new_board_state = [row[:] for row in board_state]  # Create a copy of the board
                new_board_state[adjacent[0]][adjacent[1]] = player  # Opponent's piece
                if self.__game.check_mill(new_board_state, adjacent[0], adjacent[1], player):
                    return True  # Opponent can form a mill by placing a piece here
        return False

    def can_block_ai_mill(self, board_state, row, col, player):
        # Check if the opponent's piece is part of a potential AI mill
        # We need to check if removing this piece would block the AI from completing a mill
        for adjacent in self.__game._ADJ[(row, col)]:
            if board_state[adjacent[0]][adjacent[1]] == 2:  # AI's piece
                # Simulate placing the player's piece here
                new_board_state = [row[:] for row in board_state]  # Create a copy of the board
                new_board_state[row][col] = player  # Player’s piece
                if self.__game.check_mill(new_board_state, row, col, player):
                    return True  # Placing this piece would block an AI mill
        return False

    def calculate_distance_to_ai(self, board_state, row, col):
        # Calculate the Manhattan distance between the opponent's piece and the AI’s pieces
        ai_pieces = self.__game.black_pieces  # Assuming player 2 is AI
        min_distance = float(inf)

        for ai_piece in ai_pieces:
            ai_row, ai_col = ai_piece
            distance = abs(ai_row - row) + abs(ai_col - col)
            min_distance = min(min_distance, distance)

        return -min_distance  # A shorter distance means higher priority for removal

    def generate_moves(self, board_state, player, placing):
        valid_moves = []
        pieces = self.__game.black_pieces if player == 2 else self.__game.white_pieces
        # print(pieces)
        if placing:  # During the placement phase
            for row in range(len(board_state)):
                for col in range(len(board_state[row])):
                    if board_state[row][col] == 0 and (row, col) in self.__game._VALID_POSITIONS:  # If the position is empty
                        valid_moves.append((row, col))
        else:  # During the movement phase
            if len(pieces) != 3:
                for piece in pieces:
                    for adj in self.__game._ADJ[piece]:
                        # print(adj)
                        # print(board_state[adj[0]][adj[1]])
                        # print(board_state)
                        if board_state[adj[0]][adj[1]] == 0 and adj in self.__game._VALID_POSITIONS:  # If position is empty
                            # print("we put the piece in the valid moves", adj)
                            valid_moves.append((piece, adj))
            else:
                for piece in pieces:
                    for row in range(len(board_state)):
                        for col in range(len(board_state[row])):
                            if board_state[row][col] == 0 and (row, col) in self.__game._VALID_POSITIONS:
                                valid_moves.append((piece, (row, col)))

                # print("flying_phase:", valid_moves)
        return valid_moves

    # def simulate_move(self, board_state, move, player, placing):
    #     new_state = [row[:] for row in board_state]
    #     if placing:
    #         (row, col) = move
    #         new_state[row][col] = player
    #     else:
    #         (start, end) = move
    #         new_state[start[0]][start[1]] = 0
    #         new_state[end[0]][end[1]] = player
    #
    #         # Remove an opponent's piece if a mill is formed
    #         if self.__game.check_mill(new_state, end[0], end[1], player):
    #             # opponent = 1 if player == 2 else 2
    #             # Remove an opponent's piece (find one to remove)
    #             pieces = self.__game.valid_remove_piece(player)
    #             for piece in pieces:
    #                 new_state[piece[0]][piece[1]] = 0
    #                 break
    #
    #     return new_state

    # def simulate_move(self, board_state, move, player, placing):
    #     new_state = [row[:] for row in board_state]
    #     if placing:
    #         row, col = move
    #         board_state[row][col] = player
    #     else:
    #         start, end = move
    #         board_state[start[0]][start[1]] = 0
    #         board_state[end[0]][end[1]] = player
    #
    #         # if self.__game.check_mill(board_state, end[0], end[1], player):
    #         #     opponent = 1 if player == 2 else 2
    #         #     removable_pieces = [piece for piece in
    #         #                         (self.__game.white_pieces if opponent == 1 else self.__game.black_pieces) if
    #         #                         not self.__game.check_mill(board_state, piece[0], piece[1], opponent)]
    #         #     if not removable_pieces:
    #         #         removable_pieces = self.__game.white_pieces if opponent == 1 else self.__game.black_pieces
    #         #     piece_to_remove = removable_pieces[0]
    #         #     board_state[piece_to_remove[0]][piece_to_remove[1]] = 0
    #         #     # pieces = self.__game.valid_remove_piece(player)
    #         #     # for piece in pieces:
    #         #     #     board_state[piece[0]][piece[1]] = 0
    #         #     #     break
    #
    #     if not placing and self.__game.check_mill(new_state, end[0], end[1], player):
    #         opponent_pieces = (
    #             self.__game.white_pieces if player == 2 else self.__game.black_pieces
    #         )
    #         for piece in opponent_pieces:
    #             new_state[piece[0]][piece[1]] = 0  # Simulate removing a piece
    #             break
    #
    #     return new_state

    def simulate_move(self, board_state, move, player, placing):
        new_state = [row[:] for row in board_state]
        # Directly modify the board for simulation
        from copy import deepcopy
        new_state = deepcopy(board_state)
        # new_state = [row[:] for row in board_state]
        if placing:
            (row, col) = move
            new_state[row][col] = player
        else:
            (start, end) = move
            new_state[start[0]][start[1]] = 0  # Remove from start
            new_state[end[0]][end[1]] = player  # Place at end

            # Remove an opponent's piece if a mill is formed
            # Simulate removal if a mill is formed
            if self.__game.check_mill(new_state, end[0], end[1], player):
                # opponent = 1 if player == 2 else 2
                # Remove an opponent's piece (find one to remove)
                # pieces = self.__game.valid_remove_piece(player)
                # for piece in pieces:
                #     new_state[piece[0]][piece[1]] = 0
                #     break
                best_piece = self.best_piece_to_remove(player)
                new_state[best_piece[0]][best_piece[1]] = 0


        return new_state

#TODO: fix the removing piece logic, it is not working properly -> gets stuck in a loop of invalid moves
#TODO: implement the fly phase
#TODO: Ai still moves a piece after it remains with 2 pieces
#TODO: in removing phase to check which pieces are not blocked and can still move to remove them
#TODO: cand genereaza mutarile si mai are vreo una sau doua mutari pe care le poate face, genereaza cumva boardul si e ca si cum le pune acolo si atunci apare in board state ca fiind ocupat cand de fapt e liber si de aia ai-ul nu mai gaseste mutari
