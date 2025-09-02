import unittest
from domain.board import Board
from services.computer_player import SmartComputer
from services.game import Game
from services.ai import AIPLayer
from services.game_exceptions import AdjError


class MockGraphicMode:
    def remove_piece(self, player, game_mode):
        # Return a dummy position to remove
        return 3, 3  # Example coordinates


class TestNineMensMorris(unittest.TestCase):

    def setUp(self):
        """Initialize the board, game, and AI for testing."""
        self.board = Board()
        self.mock_graphic_mode = MockGraphicMode()  # Use the mock object
        self.game = Game(self.board, graphic_mode=self.mock_graphic_mode, graphic="gui")
        self.ai = AIPLayer(self.game, graphic="gui")
        self.smart_computer = SmartComputer(self.game, "human_vs_computer")

    def test_board_initialization(self):
        """Test if the board initializes correctly."""
        self.assertEqual(len(self.board._data), 8)
        self.assertTrue(all(len(row) == 8 for row in self.board._data))
        self.assertTrue(all(cell == 0 for row in self.board._data for cell in row))

    def test_place_piece(self):
        """Test placing pieces on the board."""
        self.game.place_piece(1, 1, 1, "human_vs_human")  # Player 1 places at (1, 1)
        self.assertEqual(self.board._data[1][1], 1)
        self.game.place_piece(7, 7, 2, "human_vs_human")  # Player 2 places at (7, 7)
        self.assertEqual(self.board._data[7][7], 2)

    def test_invalid_place_piece(self):
        """Test invalid piece placement."""
        self.game.place_piece(1, 1, 1, "human_vs_human")
        with self.assertRaises(ValueError):
            self.game.place_piece(1, 1, 2, "human_vs_human")  # Spot already taken

    def test_move_piece(self):
        """Test moving a piece."""
        self.game.place_piece(1, 1, 1, "human_vs_human")
        self.game.move_piece(1, 1, 4, 1, 1, "human_vs_human")
        self.assertEqual(self.board._data[4][1], 1)
        self.assertEqual(self.board._data[1][1], 0)

    def test_invalid_move(self):
        """Test invalid moves."""
        self.game.place_piece(1, 1, 1, "human_vs_human")
        with self.assertRaises(AdjError):
            self.game.move_piece(1, 1, 2, 2, 1, "human_vs_human")  # Invalid destination

    def test_place_piece_human_vs_computer(self):
        """Test placing pieces in human vs computer mode."""
        self.game.place_piece(1, 1, 1, "human_vs_computer")  # Player 1 places at (1, 1)
        self.assertEqual(self.board._data[1][1], 1)
        # Simulate AI's random placement
        row, col = self.smart_computer.place_piece(2)
        self.game.place_piece(row, col, 2, "human_vs_computer")
        computer_placed = False
        for r in range(1, 8):
            for c in range(1, 8):
                if self.board._data[r][c] == 2:
                    computer_placed = True
                    break
            if computer_placed:
                break
        self.assertTrue(computer_placed)

    def test_move_piece_human_vs_computer(self):
        """Test moving a piece in human vs computer mode."""
        self.game.place_piece(1, 1, 1, "human_vs_computer")
        self.game.place_piece(4, 2, 2, "human_vs_computer")
        self.game.move_piece(1, 1, 4, 1, 1, "human_vs_computer")
        self.assertEqual(self.board._data[4][1], 1)
        self.assertEqual(self.board._data[1][1], 0)
        start, end = self.smart_computer.move_piece(2)
        self.game.move_piece(start[0], start[1], end[0], end[1], 2, "human_vs_computer")
        self.assertEqual(self.board._data[start[0]][start[1]], 0)
        self.assertEqual(self.board._data[end[0]][end[1]], 2)


    def test_check_mill(self):
        """Test mill formation."""
        self.game.place_piece(7, 1, 1, "human_vs_human")
        self.game.place_piece(7, 4, 1, "human_vs_human")
        assert self.game.check_mill(self.board._data, 7, 7, 1) == False

    def test_pieces_outside_mill(self):
        """Test if pieces are correctly identified as outside mills."""
        self.game.place_piece(3, 3, 2, "human_vs_human")
        self.game.place_piece(7, 1, 1, "human_vs_human")
        self.game.place_piece(7, 4, 1, "human_vs_human")
        self.game.place_piece(7, 7, 1, "human_vs_human")
        assert self.game.pieces_outside_mill(1) == False  # All pieces are in mills
    #
    def test_ai_decision_making(self):
        """Test AI piece placement."""
        self.ai.place_on_board()
        placed_positions = [(r, c) for r in range(1, 8) for c in range(1, 8) if self.board._data[r][c] == 2]
        self.assertEqual(len(placed_positions), 1)  # AI should have placed one piece

    def test_ai_remove_piece(self):
        """Test AI removing a piece."""
        self.game.place_piece(3, 3, 1, "human_vs_ai")
        self.game.place_piece(3, 4, 1, "human_vs_ai")
        self.game.place_piece(1, 1, 2, "human_vs_ai")
        self.game.place_piece(1, 4, 2, "human_vs_ai")
        self.game.place_piece(1, 7, 2, "human_vs_ai")
        self.ai.place_on_board()
        self.assertEqual(len(self.game.white_pieces), 1)  # AI should have removed a white piece

if __name__ == "__main__":
    unittest.main()
