"""
Nine men's morris board

The board consists of a grid with twenty-four intersections, or points.
Each player has nine pieces, or men, usually coloured black and white.
"""
from enum import Enum
from texttable import Texttable

from domain.color import Color


class Directions(Enum):
    """
    Enum class for directions on the board
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


""" 
how should the board look like?

        A      B     C    D    E      F     G
        1      2     3    4    5      6     7

1       *-----------------*-----------------*
        |                 |                 |
2       |      *----------*----------*      |
        |      |          |          |      |
3       |      |     *----*----*     |      |
        |      |     |         |     |      |  
4       *------*-----*         *-----*------*
        |      |     |         |     |      |
5       |      |     *----*----*     |      |  
        |      |          |          |      |
6       |      *----------*----------*      |
        |                 |                 |
7       B-----------------W-----------------* 

Computer plays with B (black piece) and human with W (white piece)

"""

from tabulate import tabulate
from domain.color import Color


class Board:
    def __init__(self):
        self._data = []

        for i in range(8):
            self._data.append([0] * 8)

    def update(self, row, col, player):
        self._data[row][col] = player

    def __str__(self):
        headers = ["/", "A", "B", "C", "D", "E", "F", "G"]
        table = []

        for row in range(1, 8):
            row_data = [f"{row}"]
            for col in range(1, 8):
                if self._data[row][col] == 1:
                    row_data.append(Color.CYAN + 'W' + Color.END)
                elif self._data[row][col] == 2:
                    row_data.append(Color.YELLOW + 'B' + Color.END)
                elif row == 1 or row == 7:
                    if col == 1 or col == 7 or col == 4:
                        row_data.append(Color.GREEN + '*' + Color.END)
                    else:
                        row_data.append(Color.PURPLE + '-' + Color.END)
                elif row == 2 or row == 6:
                    if col == 1 or col == 7:
                        row_data.append(Color.PURPLE + '|' + Color.END)
                    elif col == 2 or col == 4 or col == 6:
                        row_data.append(Color.GREEN + '*' + Color.END)
                    elif col == 3 or col == 5:
                        row_data.append(Color.PURPLE + '-' + Color.END)
                    else:
                        row_data.append(' ')
                elif row == 3 or row == 5:
                    if col < 3 or col > 5:
                        row_data.append(Color.PURPLE + '|' + Color.END)
                    else:
                        row_data.append(Color.GREEN + '*' + Color.END)
                elif row == 4:
                    if col != 4:
                        row_data.append(Color.GREEN + '*' + Color.END)
                    else:
                        row_data.append(Color.PURPLE + ' ' + Color.END)
            table.append(row_data)

        headers_str = tabulate([headers], tablefmt="grid")
        board_str = headers_str + "\n"

        for row in table:
            board_str += f"| {row[0]} |"
            for col in row[1:]:
                board_str += f" {col:<12}"  # Ensure each cell has a width of 3
            board_str += "\n"

        return board_str

#
# board = Board()
# print(board)






