from random import choice

import pygame
import sys
import time

from services.ai import AIPLayer
from domain.board import Board
from services.computer_player import SmartComputer
from services.game import Game, ComputerPlayer
from services.game_exceptions import AdjError, PlayerError

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
INDIGO = (75, 0, 130)
PINK = (251, 84, 144)
GOLDEN = (255, 251, 0)
AQUAMARINE = (127, 255, 212)
AZURE = (0, 242, 255, 0.7)
BROWN = (168, 130, 64)
BEIGE = (186, 182, 162)
CORAL = (186, 142, 95)
MISTY = (24, 84, 115)

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

class GUI:
    def __init__(self):
        self.board = Board()
        self.__game = Game(self.board, self, "gui")
        self.__computer_player = ComputerPlayer(self.__game, "gui")
        self.__ai_player = AIPLayer(self.__game, "gui")
        self.__smart_computer = SmartComputer(self.__game, "gui")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nine Men's Morris")
        self.TITLE_FONT = pygame.font.SysFont('cambria', 72)
        self.BUTTON_FONT = pygame.font.SysFont('cambria', 36)
        self.TEXT_FONT = pygame.font.SysFont('georgia', 28)
        self.game_mode = {
            "human_vs_human": self.human_vs_human,
            "human_vs_computer": self.human_vs_easy_computer,
            "human_vs_ai": self.human_vs_hard_computer
        }
        self.valid_intersections = [
            (100, 100), (400, 100), (700, 100),
            (200, 200), (400, 200), (600, 200),
            (300, 300), (400, 300), (500, 300),
            (100, 400), (200, 400), (300, 400), (500, 400), (600, 400), (700, 400),
            (300, 500), (400, 500), (500, 500),
            (200, 600), (400, 600), (600, 600),
            (100, 700), (400, 700), (700, 700)
        ]
        self.intersection_to_coords = {
            (100, 100): "11", (400, 100): "41", (700, 100): "71",
            (200, 200): "22", (400, 200): "42", (600, 200): "62",
            (300, 300): "33", (400, 300): "43", (500, 300): "53",
            (100, 400): "14", (200, 400): "24", (300, 400): "34", (500, 400): "54", (600, 400): "64", (700, 400): "74",
            (300, 500): "35", (400, 500): "45", (500, 500): "55",
            (200, 600): "26", (400, 600): "46", (600, 600): "66",
            (100, 700): "17", (400, 700): "47", (700, 700): "77"
        }
        self.occupied_positions = set()
        self.intersection_lines = {
            # Outer square
            (100, 100): [((100, 100), (400, 100)), ((100, 100), (100, 400))],  # Top-left corner
            (400, 100): [((100, 100), (700, 100)), ((400, 100), (400, 300))],  # Top-center
            (700, 100): [((400, 100), (700, 100)), ((700, 100), (700, 400))],  # Top-right corner
            (100, 400): [((100, 100), (100, 700)), ((100, 400), (300, 400))],  # Left-center
            (700, 400): [((700, 100), (700, 700)), ((500, 400), (700, 400))],  # Right-center
            (100, 700): [((100, 400), (100, 700)), ((100, 700), (400, 700))],  # Bottom-left corner
            (400, 700): [((100, 700), (700, 700)), ((400, 500), (400, 700))],  # Bottom-center
            (700, 700): [((400, 700), (700, 700)), ((700, 400), (700, 700))],  # Bottom-right corner

            # Middle square
            (200, 200): [((200, 200), (400, 200)), ((200, 200), (200, 400))],  # Top-left middle
            (400, 200): [((200, 200), (600, 200)), ((400, 200), (400, 300))],  # Top-center middle
            (600, 200): [((400, 200), (600, 200)), ((600, 200), (600, 400))],  # Top-right middle
            (200, 400): [((200, 200), (200, 600)), ((200, 400), (300, 400))],  # Left-center middle
            (600, 400): [((600, 200), (600, 600)), ((500, 400), (600, 400))],  # Right-center middle
            (200, 600): [((200, 400), (200, 600)), ((200, 600), (400, 600))],  # Bottom-left middle
            (400, 600): [((200, 600), (600, 600)), ((400, 500), (400, 600))],  # Bottom-center middle
            (600, 600): [((400, 600), (600, 600)), ((600, 400), (600, 600))],  # Bottom-right middle

            # Inner square
            (300, 300): [((300, 300), (400, 300)), ((300, 300), (300, 400))],
            (400, 300): [((300, 300), (500, 300))],  # Only horizontal line
            (500, 300): [((400, 300), (500, 300)), ((500, 300), (500, 400))],
            (300, 400): [((300, 300), (300, 500))],  # Only vertical line
            (500, 400): [((500, 300), (500, 500))],  # Only vertical line
            (300, 500): [((300, 400), (400, 500)), ((300, 500), (300, 400))],  # Corner lines
            (400, 500): [((300, 500), (500, 500))],  # Only horizontal line
            (500, 500): [((400, 500), (500, 500))],  # Only corner liner
        }
        self.black_positions = set()
        self.white_positions = set()

    def draw_text(self, surface, text, font, color, x, y, center=False):
        """Helper function to draw text on the screen."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    def display_title(self):
        """Display the animated title."""
        self.screen.fill(BEIGE)
        title = "Nine Men's Morris"
        for i in range(len(title) + 1):
            self.screen.fill(BEIGE)
            self.draw_text(self.screen, title[:i], self.TITLE_FONT, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            pygame.display.flip()
            time.sleep(0.1)

        time.sleep(1)

    def wrap_and_justify_text(self, text, font, max_width):
        """Wrap and justify text to fit within a given width."""
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word, True, BLACK)
            word_width = word_surface.get_width()
            if current_width + word_width + (len(current_line) * 10) <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(current_line)
                current_line = [word]
                current_width = word_width
        if current_line:
            lines.append(current_line)

        justified_lines = []
        for i, line in enumerate(lines):
            if i == len(lines) - 1:  # Don't justify the last line
                justified_lines.append(" ".join(line))
            else:
                line_width = sum(font.render(word, True, BLACK).get_width() for word in line)
                space_width = (max_width - line_width) // (len(line) - 1) if len(line) > 1 else 0
                justified_line = ""
                for j, word in enumerate(line):
                    justified_line += word
                    if j < len(line) - 1:
                        justified_line += " " * (space_width // 5)  # Adjust space scaling as needed
                justified_lines.append(justified_line)

        return justified_lines

    def display_indications(self):
        """Display game indications with text wrapping, justified alignment, and start button."""
        self.screen.fill(BEIGE)

        indications = [
            {"text": "How to play:", "color": MISTY},
            {"text": "Setup: Each player has nine pieces. The winner is the first player to align their three pieces on a line drawn on the board.\n", "color": BLACK},
            {"text": "Gameplay:", "color": MISTY},
            {"text": "Players take turns placing pieces, trying to form mills (three in a row). Forming a mill lets you remove an opponent's piece. After placement, move pieces to adjacent positions to form mills. When a player has three pieces left, they can jump to any position. The game ends when a player has only two pieces left.\n", "color": BLACK},
            {"text": "Note: White goes first.\n", "color": MISTY},
            {"text": "Let's start the game!", "color": PINK},
        ]

        y = 50
        max_text_width = SCREEN_WIDTH - 100
        for section in indications:
            lines = self.wrap_and_justify_text(section["text"], self.TEXT_FONT, max_text_width)
            for line in lines:
                self.draw_text(self.screen, line, self.TEXT_FONT, section["color"], 50, y)
                y += 30  # Space between lines
            # self.draw_text(self.screen, ' ', self.TEXT_FONT, section["color"], 50, y)
            y += 30

        start_button = {
            "text": "Start",
            "x": SCREEN_WIDTH // 2,
            "y": SCREEN_HEIGHT - 100,
            "mode": "start_game"
        }

        pygame.draw.rect(self.screen, CORAL, (start_button["x"] - 75, start_button["y"] - 25, 150, 50))
        self.draw_text(self.screen, start_button["text"], self.BUTTON_FONT, BLACK, start_button["x"], start_button["y"], center=True)
        pygame.display.flip()

        self.wait_for_button_click([start_button])

    def display_buttons(self):
        """Display game mode selection buttons."""
        self.screen.fill(BEIGE)
        self.draw_text(self.screen, "Choose the game mode:", self.BUTTON_FONT, BLACK, SCREEN_WIDTH // 2, 100, center=True)

        buttons = [
            {"text": "Human vs Human", "x": SCREEN_WIDTH // 2, "y": 250, "mode": "human_vs_human"},
            {"text": "Human vs Easy Computer", "x": SCREEN_WIDTH // 2, "y": 350, "mode": "human_vs_computer"},
            {"text": "Human vs Hard Computer", "x": SCREEN_WIDTH // 2, "y": 450, "mode": "human_vs_ai"},
        ]

        for button in buttons:
            pygame.draw.rect(self.screen, BROWN, (button["x"] - 250, button["y"] - 25, 500, 50))
            self.draw_text(self.screen, button["text"], self.BUTTON_FONT, BLACK, button["x"], button["y"], center=True)

        pygame.display.flip()
        return buttons

    def wait_for_button_click(self, buttons):
        """Wait for the user to click one of the buttons."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for button in buttons:
                        button_x = button["x"]
                        button_y = button["y"]
                        button_width = 500
                        button_height = 50
                        if button_x - button_width // 2 < x < button_x + button_width // 2 and \
                                button_y - button_height // 2 < y < button_y + button_height // 2:
                            return button["mode"]

    def display_board(self):
        """Display the game board."""
        self.screen.fill(BEIGE)
        pygame.draw.rect(self.screen, BLACK, (100, 100, 600, 600), 2)
        pygame.draw.rect(self.screen, BLACK, (200, 200, 400, 400), 2)
        pygame.draw.rect(self.screen, BLACK, (300, 300, 200, 200), 2)
        pygame.draw.line(self.screen, BLACK, (400, 100), (400, 300), 2)
        pygame.draw.line(self.screen, BLACK, (400, 500), (400, 700), 2)
        pygame.draw.line(self.screen, BLACK, (100, 400), (300, 400), 2)
        pygame.draw.line(self.screen, BLACK, (500, 400), (700, 400), 2)

        turn_text = "Player 1's Turn"
        self.draw_text(self.screen, turn_text, self.TEXT_FONT, BLACK, SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH // 2 + 110, 20), 15)

        pieces_left_text = "Player 1 - 9     Player 2 - 9"
        self.draw_text(self.screen, pieces_left_text, self.TEXT_FONT, BLACK, SCREEN_WIDTH // 2, 760, center=True)
        pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH // 2 - 200, 760), 15)
        pygame.draw.circle(self.screen, BLACK, (SCREEN_WIDTH // 2 + 200, 760), 15)
        pygame.display.flip()

    def update_status_text(self, player, whites_left, blacks_left):
        """Update the status text with the current player's turn and pieces left."""
        # Clear the previous text
        self.screen.fill(BEIGE, (0, 10, SCREEN_WIDTH, 50))  # Top part for player's turn
        self.screen.fill(BEIGE, (0, 750, SCREEN_WIDTH, 50))  # Bottom part for pieces left

        # Display player's turn at the top
        turn_text = f"Player {player}'s Turn"
        color = WHITE if player == 1 else BLACK
        self.draw_text(self.screen, turn_text, self.TEXT_FONT, BLACK, SCREEN_WIDTH // 2, 20, center=True)
        pygame.draw.circle(self.screen, color, (SCREEN_WIDTH // 2 + 110, 20), 15)

        # Display pieces left at the bottom
        pieces_left_text = f"Player 1 - {whites_left}     Player 2 - {blacks_left}"
        self.draw_text(self.screen, pieces_left_text, self.TEXT_FONT, BLACK, SCREEN_WIDTH // 2, 760, center=True)
        pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH // 2 - 200, 760), 15)
        pygame.draw.circle(self.screen, BLACK, (SCREEN_WIDTH // 2 + 200, 760), 15)

        pygame.display.flip()

    def draw_placement(self, ix, iy, whites_left, blacks_left, player, game_mode):
        # Place the piece on the board
        color = WHITE if player == 1 else BLACK
        pygame.draw.circle(self.screen, color, (ix, iy), 20)
        pygame.display.flip()
        self.occupied_positions.add((ix, iy))
        game_coord = self.intersection_to_coords[(ix, iy)]
        row = int(game_coord[1])
        col = int(game_coord[0])
        if game_mode == "human_vs_human" or player == 1:
            self.__game.place_piece(row, col, player, game_mode)
        self.update_status_text(2 if player == 1 else 1, whites_left, blacks_left)
        # return  # Exit the function after placing the piece

    def piece_placement(self, player, whites_left, blacks_left, game_mode):
        """Handle the placement of a piece on the board."""
        # color = WHITE if player == 1 else BLACK

        if game_mode == "human_vs_human" or player == 1:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        # Check if the click is within the board boundaries
                        for ix, iy in self.valid_intersections:
                            if ix - 25 <= x <= ix + 25 and iy - 25 <= y <= iy + 25 and (ix, iy) not in self.occupied_positions:
                                if player == 1:
                                    self.white_positions.add((ix, iy))
                                    # self.__game._white_pieces.append((ix, iy))
                                else:
                                    self.black_positions.add((ix, iy))

                                self.draw_placement(ix, iy, whites_left, blacks_left, player, game_mode)
                                return

        else:
            if game_mode == "human_vs_computer":
                # print("we are here")
                #ix, iy = self.__computer_player.place_on_board()
                ix, iy = self.__smart_computer.place_piece(player)
                self.__game.place_piece(ix, iy, 2, game_mode)
                print(ix, iy)

            elif game_mode == "human_vs_ai":
                ix, iy = self.__ai_player.place_on_board()

            coords = self.board_to_gui_coords([(ix, iy)])
            ix = int(coords[0])
            iy = int(coords[1])
            # print(ix, iy)
            self.black_positions.add((ix, iy))
            self.draw_placement(ix, iy, whites_left, blacks_left, player, game_mode)

    def display_move(self, initial_x, initial_y, final_x, final_y, player):
        selected_piece = (initial_x, initial_y)
        self.occupied_positions.remove(selected_piece)
        self.occupied_positions.add((final_x, final_y))
        if player == 1:
            self.white_positions.remove(selected_piece)
            self.white_positions.add((final_x, final_y))
        else:
            self.black_positions.remove(selected_piece)
            self.black_positions.add((final_x, final_y))
        self.redraw_board()
        # self.__game.move_piece(initial_x, initial_y, final_x, final_y, player, self.game_mode)
        self.update_status_text(2 if player == 1 else 1, len(self.__game.white_pieces), len(self.__game.black_pieces))
        self.screen.fill(BEIGE, (0, 720, SCREEN_WIDTH, 100))  # Clear the previous text

    def move_piece(self, player, game_mode):
        """Handle the movement of a piece on the board by dragging."""
        color = WHITE if player == 1 else BLACK
        selected_piece = None
        initial_pos = None

        if game_mode == "human_vs_human" or player == 1:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        # Check if the click is on one of the player's pieces
                        for ix, iy in self.occupied_positions:
                            if ix - 25 <= x <= ix + 25 and iy - 25 <= y <= iy + 25:
                                if (ix, iy) in (self.white_positions if player == 1 else self.black_positions):
                                    selected_piece = (ix, iy)
                                    initial_pos = (int(self.intersection_to_coords[(ix, iy)][0]), int(self.intersection_to_coords[(ix, iy)][1]))
                                    break
                    if event.type == pygame.MOUSEBUTTONUP and selected_piece:
                        x, y = event.pos
                        # Check if the release is within the board boundaries
                        for ix, iy in self.valid_intersections:
                            if ix - 25 <= x <= ix + 25 and iy - 25 <= y <= iy + 25:
                                final_pos = (int(self.intersection_to_coords[(ix, iy)][0]), int(self.intersection_to_coords[(ix, iy)][1]))
                                try:
                                    can_fly = True if len(self.white_positions) == 3 and player == 1 or len(self.black_positions) == 3 and player == 2 else False
                                    self.__game.valid_move(initial_pos[1], initial_pos[0], final_pos[1], final_pos[0], player, can_fly)

                                    self.display_move(selected_piece[0], selected_piece[1], ix, iy, player)
                                    self.__game.move_piece(initial_pos[1], initial_pos[0], final_pos[1], final_pos[0], player, game_mode)

                                    return  # Exit the function after moving the piece
                                except (ValueError, AdjError, PlayerError):
                                    pass

        else:
            if game_mode == "human_vs_computer":
                #initial_x, initial_y, final_x, final_y = self.__computer_player.move_computer()
                if len(self.white_positions) == 3 and player == 1 or len(self.black_positions) == 3 and player == 2:
                    initial_position, final_position = self.__smart_computer.fly_piece(player)
                    initial_x, initial_y = initial_position
                    final_x, final_y = final_position

                else:
                    initial_position, final_position = self.__smart_computer.move_piece(player)
                    initial_x, initial_y = initial_position
                    final_x, final_y = final_position
                self.__game.move_piece(initial_x, initial_y, final_x, final_y, player, game_mode)

            elif game_mode == "human_vs_ai":
                initial, final = self.__ai_player.move_piece()
                initial_x = int(initial[0])
                initial_y = int(initial[1])
                final_x = int(final[0])
                final_y = int(final[1])

            ix, iy = self.board_to_gui_coords([(initial_x, initial_y)])
            fx, fy = self.board_to_gui_coords([(final_x, final_y)])
            self.display_move(ix, iy, fx, fy, player)


    def redraw_board(self):
        """Redraw the entire board, including all pieces except the removed one."""
        # Clear the screen
        self.screen.fill(BEIGE)

        # Draw the board (lines and intersections)
        self.display_board()

        # Re-draw all remaining pieces
        for (x, y) in self.occupied_positions:
            piece_color = BLACK if (x, y) in self.black_positions else WHITE
            pygame.draw.circle(self.screen, piece_color, (x, y), 20)

        # Update the display
        pygame.display.flip()

    def board_to_gui_coords(self, board_coords):
        """Convert board coordinates (e.g., A1) to GUI coordinates (x, y)."""
        gui_coords = []

        for board_coord in board_coords:
            # print(board_coord)
            col = board_coord[1]
            row = board_coord[0]

            mapping = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600, 7: 700}

            x = mapping[col]
            y = mapping[row]

            gui_coords.append((x, y))

        # print(gui_coords)
        if len(gui_coords) == 1:
            return gui_coords[0]

        return gui_coords

    def draw_remove(self, ix, iy, player):
        game_coord = self.intersection_to_coords[(ix, iy)]
        print("fcking the coordinate", int(game_coord[1]))
        row = int(game_coord[1])
        col = int(game_coord[0])

        print(row, col)
        # Remove the piece by updating the occupied positionsz
        self.occupied_positions.remove((ix, iy))
        self.white_positions.remove((ix, iy)) if player == 2 else self.black_positions.remove((ix, iy))

        # Redraw the board and pieces
        self.redraw_board()
        pygame.display.flip()

        return row, col  # Exit the function after removing the piece

    def remove_piece(self, player, game_mode):
        """Handle the removal of an opponent's piece from the board."""
        opponent = 2 if player == 1 else 1
        color = BLACK if player == 1 else WHITE

        # Display the text indicating the player should remove a piece
        self.screen.fill(BEIGE, (0, 0, SCREEN_WIDTH, 70))  # Top part for player's turn
        remove_text = f"Player {player}, remove a piece"
        self.draw_text(self.screen, remove_text, self.TEXT_FONT, BLACK, SCREEN_WIDTH // 2, 20, center=True)
        pygame.display.flip()

        valid_pieces = self.__game.valid_remove_piece(player)
        valid_pieces = self.board_to_gui_coords(valid_pieces)

        # print("these are the valid_pieces", valid_pieces)

        if game_mode == "human_vs_human" or player == 1:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        # Check if the click is on an opponent's piece
                        for ix, iy in self.valid_intersections:
                            if ix - 25 <= x <= ix + 25 and iy - 25 <= y <= iy + 25 and ((ix, iy) in valid_pieces or (ix, iy) == valid_pieces):
                                row, col = self.draw_remove(ix, iy, player)
                                # print(row, col)
                                return row, col  # Exit the function after removing the piece

        else:
            if game_mode == "human_vs_computer":
                #ix, iy = choice(valid_pieces)
                ix, iy = self.__smart_computer.remove_piece(player)
                ix, iy = self.board_to_gui_coords([(ix, iy)])
                print(ix, iy)

            elif game_mode == "human_vs_ai":
                ix, iy = self.__ai_player.best_piece_to_remove(player)
                ix, iy = self.board_to_gui_coords([(ix, iy)])

            row, col = self.draw_remove(ix, iy, player)
            print("piece to remove", row, col)
            print(self.__game.white_pieces)
            return row, col

    def restart_game(self, play_again_button, exit_button):
        """Handle the restart of the game."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if play_again_button["x"] <= x <= play_again_button["x"] + play_again_button["width"] and play_again_button["y"] <= y <= play_again_button["y"] + play_again_button["height"]:
                        self.display_indications()
                        buttons = self.display_buttons()
                        game_mode = self.wait_for_button_click(buttons)
                        self.game_mode[game_mode]()
                        return
                    if exit_button["x"] <= x <= exit_button["x"] + exit_button["width"] and exit_button["y"] <= y <= exit_button["y"] + exit_button["height"]:
                        pygame.quit()
                        sys.exit()

    def display_winner(self, player):
        self.screen.fill(BEIGE, (0, 0, SCREEN_WIDTH, 70))
        self.screen.fill(BEIGE, (0, 720, SCREEN_WIDTH, 100))
        #YOU STOPPED HERE
        text = f"Player {player} wins!"
        self.draw_text(self.screen, text, self.TITLE_FONT, BLACK, SCREEN_WIDTH // 2,  30, center=True)

        # Draw the "PLAY AGAIN" button
        play_again_button = {"text": "PLAY AGAIN", "x": SCREEN_WIDTH // 2 - 300, "y": 730, "width": 200, "height": 40}
        pygame.draw.rect(self.screen, GREEN, (play_again_button["x"], play_again_button["y"], play_again_button["width"], play_again_button["height"]))
        self.draw_text(self.screen, play_again_button["text"], self.BUTTON_FONT, BLACK,
                       play_again_button["x"] + play_again_button["width"] // 2,
                       play_again_button["y"] + play_again_button["height"] // 2, center=True)

        # Draw the "EXIT GAME" button
        exit_button = {"text": "EXIT GAME", "x": SCREEN_WIDTH // 2 + 100, "y": 730, "width": 200, "height": 40}
        pygame.draw.rect(self.screen, RED,(exit_button["x"], exit_button["y"], exit_button["width"], exit_button["height"]))
        self.draw_text(self.screen, exit_button["text"], self.BUTTON_FONT, BLACK,
                       exit_button["x"] + exit_button["width"] // 2,
                       exit_button["y"] + exit_button["height"] // 2, center=True)

        pygame.display.flip()

        self.restart_game(play_again_button, exit_button)

    def human_vs_human(self):
        self.display_board()
        whites = 9
        blacks = 9
        game_mode = "human_vs_human"

        #placement_phase
        while True:
            if whites > 0:
                self.piece_placement(1, whites - 1, blacks, game_mode)
                whites -= 1

            if blacks > 0:
                self.piece_placement(2, whites, blacks - 1, game_mode)
                blacks -= 1

            if whites == 0 and blacks == 0:
                break

        #moving_phase
        while True:

            # white moves
            if self.__game.check_moves_left(1):
                self.move_piece(1, game_mode)
            else:
                self.display_winner(2)

            if len(self.__game.black_pieces) < 3:
                self.display_winner(1)

            #black moves
            if self.__game.check_moves_left(2):
                self.move_piece(2, game_mode)
            else:
                self.display_winner(1)

            if len(self.__game.white_pieces) < 3:
                self.display_winner(2)


    def human_vs_easy_computer(self):
        self.display_board()
        whites = 9
        blacks = 9
        game_mode = "human_vs_computer"

        #placement_phase
        while True:
            if whites > 0:
                self.piece_placement(1, whites - 1, blacks, game_mode)
                whites -= 1

            if blacks > 0:
                self.piece_placement(2, whites, blacks - 1, game_mode)
                blacks -= 1

            if whites == 0 and blacks == 0:
                break

        #moving_phase
        while True:

            #white moves
            if self.__game.check_moves_left(1):
                self.move_piece(1, game_mode)
            else:
                self.display_winner(2)


            if len(self.__game.black_pieces) < 3:
                self.display_winner(1)

            #black moves
            if self.__game.check_moves_left(2):
                self.move_piece(2, game_mode)
            else:
                self.display_winner(1)

            if len(self.__game.white_pieces) < 3:
                self.display_winner(2)

    def human_vs_hard_computer(self):
        self.display_board()
        whites = 9
        blacks = 9
        game_mode = "human_vs_ai"

        # placement_phase
        while True:
            if whites > 0:
                self.piece_placement(1, whites - 1, blacks, game_mode)
                whites -= 1

            if blacks > 0:
                self.piece_placement(2, whites, blacks - 1, game_mode)
                blacks -= 1

            if whites == 0 and blacks == 0:
                break

        # moving_phase
        while True:

            # white moves
            if self.__game.check_moves_left(1):
                self.move_piece(1, game_mode)
            else:
                self.display_winner(2)

            if len(self.__game.black_pieces) < 3:
                self.display_winner(1)

            # black moves
            if self.__game.check_moves_left(2):
                self.move_piece(2, game_mode)
            else:
                self.display_winner(1)

            if len(self.__game.white_pieces) < 3:
                self.display_winner(2)


    def main(self):
        self.display_title()
        self.display_indications()
        buttons = self.display_buttons()
        game_mode = self.wait_for_button_click(buttons)
        self.game_mode[game_mode]()
        # self.display_board()

if __name__ == "__main__":
    gui = GUI()
    gui.main()
