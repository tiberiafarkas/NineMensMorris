import pyfiglet

from services.ai import AIPLayer
from domain.board import Board
from domain.color import Color
from services.computer_player import SmartComputer
from services.game import Game, ComputerPlayer, AdjError, PlayerError

class UI:
    def __init__(self):
        self.board = Board()
        self.__game = Game(self.board, self, "ui")
        self.__computer_player = ComputerPlayer(self.__game, "ui")
        self.__ai_player = AIPLayer(self.__game, "ui")
        self.__smart_computer = SmartComputer(self.__game, "ui")
        self.__commands = {
            "1": self.human_vs_human,
            "2": self.human_vs_computer,
            "3": self.human_vs_ai
        }
        self.__coord = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
        }

    def remove_piece(self, player, game_mode):
        if player == 2:
            position = input("Enter the position of the white piece to be removed: ").strip()
            position = self.validate_move(position)
        else:
            position = input("Enter the position of the black piece to be removed: ").strip()
            position = self.validate_move(position)
        row = int(position[1])
        col = self.__coord[position[0].upper()]
        return row, col

    def validate_move(self, move):
        if len(move) != 2:
            raise ValueError("Input must have 2 characters!")

        try:
            if move[0].upper() not in self.__coord.keys():
                raise ValueError("The first character must be a letter between A and G!")

            try:
                if int(move[1]) < 1 or int(move[1]) > 7:
                    raise ValueError("The second character must be a number between 1 and 7!")
            except ValueError:
                raise ValueError("The second character must be a number between 1 and 7!")

        except ValueError as ve:
            try:
                if move[1].upper() not in self.__coord.keys():
                    raise ValueError("The second character must be a letter between A and G!")

                if int(move[0]) < 1 or int(move[0]) > 7:
                    raise ValueError("The first character must be a number between 1 and 7!")

                move = move.strip().upper()
                move = move[1] + move[0]

            except ValueError:
                raise ValueError("The first character must be a number between 1 and 7!")

        return move

    def print_menu(self):
        ascii_art = pyfiglet.figlet_format("Nine Men's Morris", font = "starwars")
        print(Color.BOLD + Color.YELLOW + ascii_art + Color.END + '\n')
        print(Color.GREEN + "How to play:" + Color.END)
        print(Color.BOLD + Color.RED + "Setup: " + Color.END + "Each player has nine pieces. The winner is the first player to align their three pieces on a line drawn on the board." + '\n')
        print(Color.BOLD + Color.RED + "Gameplay: " + Color.END +
              "The board is empty to begin the game. Players take turns placing their pieces on empty points, trying to create a row of three (a mill). \n"
              "If a player creates a mill, they remove 1 of their opponent’s pieces from the board, except any in a mill. \n"
              "If an opponent only has pieces in a mill, one can be captured. \n"
              "When all pieces are placed, players take turns moving to an open adjacent point on the board, trying to form a mill. \n"
              "Pieces cannot jump over other pieces. \n"
              "Each time a mill is formed, an opponent’s piece is removed. \n"
              "Play then passes back to the other player. \n"
              "Players can “break” and “remake” mills. \n"
              "When one player has three pieces left, they can “jump” their pieces to any vacant point on the board. \n"
              "Play ends when one player only has two pieces left." + '\n')
        print(Color.BOLD + Color.RED + "Note: " + Color.END + "The player with the white pieces goes first." + '\n')
        print(Color.CYAN + "Let's start the game" + Color.END + '\n')
        print(Color.BOLD + Color.YELLOW + "Choose the game mode: " + Color.END)
        print(Color.GREEN + "1. Human vs Human" + Color.END)
        print(Color.GREEN + "2. Human vs Computer" + Color.END)
        print(Color.GREEN + "3. human vs ai" + Color.END)

    def piece_to_place(self, player, game_mode):
        if player == 1:
            piece = "White"
        else:
            piece = "Black"

        while True:
            try:
                move = input("Where do you want to place the piece? "
                             f"{piece} piece: ")
                move = self.validate_move(move)
                move.strip()
                row = int(move[1])
                col = self.__coord[move[0].upper()]
                self.__game.place_piece(row, col, player, game_mode)
                break

            except ValueError as ve:
                print(ve)

        print('\n')
        print(self.board, '\n')

        # self.__game.is_mill(row, col, player, game_mode)

    def make_moves(self, player, game_mode):
        if player == 1:
            piece = "White"
        else:
            piece = "Black"
        while True:
            try:
                initial_piece = input(f"{piece} move the piece placed at the position: ")
                initial_piece = self.validate_move(initial_piece)
                final_piece = input("Position to be moved: ")
                final_piece = self.validate_move(final_piece)
                initial_piece.strip()
                final_piece.strip()
                self.__game.move_piece(int(initial_piece[1]), self.__coord[initial_piece[0].upper()], int(final_piece[1]), self.__coord[final_piece[0].upper()], player, game_mode)
                break
            except (ValueError, AdjError, PlayerError) as ve:
                print(ve)

        print('\n', self.board, '\n')

        # row = int(final_piece[1])
        # col = self.__coord[final_piece[0].upper()]
        # self.__game.is_mill(row, col, player, game_mode)

    def human_vs_human(self):
        whites = 9
        blacks = 9
        game_mode = "human_vs_human"

        #first stage - place the pieces
        print("---------FIRST STAGE---------")
        print("Place the pieces on the board")

        print('\n')
        print(self.board, '\n')

        while True:
            # print('\n')
            # print(self.board, '\n')

            #TODO implement validations for the input datas
            if whites > 0:
                self.piece_to_place(1, game_mode)
                whites -= 1

            # print('\n')
            # print(self.board, '\n')

            if blacks > 0:
                self.piece_to_place(2, game_mode)
                blacks -= 1

            if whites == 0 and blacks == 0:
                break
#print after the white removed a piece because of a mill
#mention what piece must be moved
        # print(self.board, '\n')

        #second stage - move the pieces
        print("-----------------SECOND STAGE--------------------")
        print("Players take turns moving the pieces on the board")

        while True:
            #white moves

            if self.__game.check_moves_left(1):
                self.make_moves(1, game_mode)
            else:
                print("White has no moves left! Black wins!")
                break

            if len(self.__game._black_pieces) < 3:
                print("White wins!")
                break

            # black moves

            if self.__game.check_moves_left(2):
                self.make_moves(2, game_mode)
            else:
                print("Black doesn't have any moves left! White wins!")
                break

            if len(self.__game._white_pieces) < 3:
                print("Black wins!")
                break


    def human_vs_computer(self):
        whites = 9
        blacks = 9
        game_mode = "human_vs_computer"

        #first stage - place the pieces
        print("---------FIRST STAGE---------")
        print("Place the pieces on the board")

        while True:
            print('\n')
            print(self.board, '\n')

            # TODO implement validations for the input datas
            if whites > 0:
                self.piece_to_place(1, game_mode)
                whites -= 1

            if blacks > 0:
                #self.__computer_player.place_on_board()
                row, col = self.__smart_computer.place_piece(2)
                self.__game.place_piece(row, col, 2, game_mode)
                blacks -= 1

            if whites == 0 and blacks == 0:
                break

        print(self.board, '\n')

        #second stage - move the pieces
        print("-----------------SECOND STAGE--------------------")
        print("Players take turns moving the pieces on the board")

        while True:
            #white moves

            if self.__game.check_moves_left(1):
                self.make_moves(1, game_mode)
            else:
                print("You have no moves left! Computer wins!")
                break

            # black moves

            if self.__game.check_moves_left(2):
                #self.__computer_player.move_computer()
                start_position, final_position = self.__smart_computer.move_piece(2)
                self.__game.move_piece(start_position[0], start_position[1], final_position[0], final_position[1], 2, game_mode)

                print(f"Computer placed from {start_position}, to {final_position}")
                print('\n')
                print(self.board, '\n')
            else:
                print("Computer doesn't have any moves left! You win!")
                break

            if len(self.__game._white_pieces) < 3:
                print("Computer wins!")
                break

            if len(self.__game._black_pieces) < 3:
                print("You win!")
                break

    def human_vs_ai(self):
        whites = 9
        blacks = 9
        game_mode = "human_vs_ai"

        # first stage - place the pieces
        print("---------FIRST STAGE---------")
        print("Place the pieces on the board")

        while True:
            print('\n')
            print(self.board, '\n')

            # TODO implement validations for the input datas
            if whites > 0:
                self.piece_to_place(1, game_mode)
                whites -= 1

            if blacks > 0:
                self.__ai_player.place_on_board()
                blacks -= 1

            if whites == 0 and blacks == 0:
                break

        print(self.board, '\n')

        # second stage - move the pieces
        print("-----------------SECOND STAGE--------------------")
        print("Players take turns moving the pieces on the board")

        while True:
            # white moves

            if self.__game.check_moves_left(1):
                self.make_moves(1, game_mode)
            else:
                print("You have no moves left! Computer wins!")
                break

            # black moves

            if self.__game.check_moves_left(2):
                self.__ai_player.move_piece()

                print('\n')
                print(self.board, '\n')
            else:
                print("Computer doesn't have any moves left! You win!")
                break

            if len(self.__game._white_pieces) < 3:
                print("Computer wins!")
                break

            if len(self.__game._black_pieces) < 3:
                print("You win!")
                break



    def start(self):
        # whites = 9
        # blacks = 9
        self.print_menu()

        while True:
            option = input(">>>")
            if option in self.__commands:
                self.__commands[option]()
                break
            else:
                print("Invalid option!!")

ui = UI()
ui.start()
