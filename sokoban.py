from __future__ import annotations
import inspect
import copy
from typing import TypeAlias, List, Dict, Tuple, Optional

directions: Dict[str, Vector] = {
    'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


Vector: TypeAlias = Tuple[int, int]
BaseBoard: TypeAlias = list[list[str]]
Vectors: TypeAlias = list[Vector]


def vec_plus(v1: Vector, v2: Vector) -> Vector:
    x: List[int] = []
    for i in range(len(v1)):
        x.append(v1[i]+v2[i])
    return (x[0], x[1])


class Board:
    def __init__(self, baseboard: BaseBoard, targets: Vectors):
        self.brd = baseboard
        self.targets: Vectors = targets

    def is_valid_move(self, pos: Vector) -> bool:
        x, y = pos
        return 0 <= x < len(self.brd) and \
            0 <= y < len(self.brd[0]) and \
            self.brd[x][y] != '#'

    def find_children(self) -> List[Board]:
        children: List[Board] = []
        pos, _ = self.find_OoIs()
        for ele in directions:
            new_pos = vec_plus(pos, directions[ele])

            if self.is_valid_move(new_pos):
                new_brd = copy.deepcopy(self.brd)
                block_new_pos = [(-1, -1)]
                if new_brd[new_pos[0]][new_pos[1]] == 'X':  # Pushing the box
                    block_new_pos = vec_plus(new_pos, directions[ele])
                    if not self.is_valid_move(block_new_pos):
                        continue
                    new_brd[block_new_pos[0]][block_new_pos[1]] = "X"
                new_brd[pos[0]][pos[1]] = "."
                new_brd[new_pos[0]][new_pos[1]] = "@"
                for pos2 in self.targets:
                    if not (pos2 == new_pos or pos2 == block_new_pos):
                        new_brd[pos2[0]][pos2[1]] = "*"
                children.append(Board(new_brd, self.targets))
        return children

    def find_OoIs(self) -> Tuple[Vector, Vectors]:
        """
        Returns the player, box and target positions
        """
        boxes: Vectors = []
        for i in range(len(self.brd)):
            for j in range(len(self.brd[0])):
                if self.brd[i][j] == '@':
                    robot_pos: Vector = (i, j)
                elif self.brd[i][j] == 'X':
                    boxes.append((i, j))
        return (robot_pos, boxes)

    def solved(self) -> bool:
        # breakpoint()
        _, boxes = self.find_OoIs()
        return set(boxes) == set(self.targets)

    def __str__(self):
        # symbol_mapping = {
        #     '.': '-',  # Empty space
        #     '#': '█',  # Wall
        #     'X': 'X',  # Box
        #     '@': '☺',  # Player
        #     '*': '★'  # Target
        # }\
        # ⬛🟦🟫📦🚶🎯

        symbol_mapping = {
            '.': '⬛',  # Empty space
            '#': '🟦',  # Wall
            ' ': '🟥',  # Outer space
            'X': '🟫',  # Box
            '@': '🚶',  # Player
            '*': '🎯'  # Target
        }

        return '\n'.join(''.join(symbol_mapping.get(cell, '  ') for cell in row) for row in self.brd)+'\n'


def soko_solver(board: list[str]):
    board1 = [list(row) for row in board]

    targets = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '*':
                targets.append((i, j))
    board2 = Board(board1, targets)
    return DFBnB(board2)


def DFBnB(board: Board) -> Optional[List[str]]:
    global U
    if len(inspect.stack()) > U:
        return None
    if board.solved():
        U = min(U, len(inspect.stack()))
        return [str(board)]

    out = None
    for brd in board.find_children():
        soln = DFBnB(brd)
        if soln is not None:
            out = [str(board)] + soln

    return out


# Define the board configuration
# @ - player
# X - box
# * - target
# # - wall
boards = [
    [
        ".@.",
        "X..",
        "*.."
    ],
    [
        "X..",
        "*@.",
        "..."
    ],
    [
        "@....",
        ".X...",
        "####.",
        "   #*"
    ],
    [
        "..#@.##",
        "....X.#",
        "...#.X.",
        "####**#",
        "   #.##",
        "   ####"
    ],
    [
        "########",
        "#..#@...",
        "#...#XX#",
        "#...#..#",
        "####*.*#",
        "....#.##",
        "....####"
    ]]

for board in boards:
    U = len(board)**2+len(inspect.stack())
    result = soko_solver(board)
    print(U-len(inspect.stack()))
    if result is not None:
        print("Solution found:")
        for brd in result:
            print(brd, end='\n')
    else:
        print("No solution found.")
