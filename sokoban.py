from __future__ import annotations
import inspect
from collections import deque
import copy
from typing import TypeAlias, List, Dict, Tuple, Optional

directions: Dict[str, Vector] = {
    'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


Vector: TypeAlias = Tuple[int, int]
BaseBoard: TypeAlias = list[list[str]]
Vectors: TypeAlias = list[Vector]

def vec_plus(v1: Vector, v2: Vector):
    x: List[int] = []
    for i in range(len(v1)):
        x.append(v1[i]+v2[i])
    return (x[0], x[1])


class Board:
    def __init__(self, baseboard: BaseBoard):
        self.brd = baseboard
        self.targets: Vectors = []
        self.find_OoIs()

    def is_valid_move(self, pos: Vector) -> bool:
        x, y = pos
        return 0 <= x < len(self.brd) and \
            0 <= y < len(self.brd[0]) and \
            self.brd[x][y] != '#'

    def find_children(self) -> List[Board]:
        children: List[Board] = []
        pos, _, __ = self.find_OoIs()
        for ele in directions:
            new_pos = vec_plus(pos, directions[ele])

            if self.is_valid_move(new_pos):
                new_brd = copy.deepcopy(self.brd)
                if new_brd[new_pos[0]][new_pos[1]] == 'X':  # Pushing the box
                    block_new_pos = vec_plus(new_pos, directions[ele])
                    if not self.is_valid_move(block_new_pos):
                        continue
                    new_brd[block_new_pos[0]][block_new_pos[1]] = "X"
                new_brd[pos[0]][pos[1]] = "."
                new_brd[new_pos[0]][new_pos[1]] = "@"
                children.append(Board(new_brd))
        return children

    def solved(self) -> bool:
        for row in self.brd:
            for cell in row:
                if cell == '*':
                    return False
        return True
    
    def find_OoIs(self) -> Tuple[Vector, Vectors, Vectors]:
        """
        Returns the player, box and target positions
        """
        boxes: Vectors = []
        target_positions: Vectors = []
        for i in range(len(self.brd)):
            for j in range(len(self.brd[0])):
                if self.brd[i][j] == '@':
                    robot_pos: Vector = (i, j)
                elif self.brd[i][j] == 'X':
                    boxes.append((i, j))
                elif self.brd[i][j] == '*':
                    target_positions.append((i, j))
        if len(self.targets)==0:
            self.targets=target_positions
        else:
            target_positions=self.targets
        return (robot_pos, boxes, target_positions)

    def solved(self) -> bool:
        _, boxes, trgts = self.find_OoIs()
        return set(boxes) == set(trgts)

    def __repr__(self):
        return '\n'.join(''.join(row) for row in self.brd)+'\n'


def soko_solver(board: list[str]):
    board1 = [list(row) for row in board]
    board2 = Board(board1)
    return DFBnB(board2)


def DFBnB(board: Board) -> Optional[List[Board]]:
    global U
    if len(inspect.stack()) > U:
        return None
    if board.solved():
        U = min(U, len(inspect.stack()))
        return [board]

    out = None
    for brd in board.find_children():
        soln = DFBnB(brd)
        if soln is not None:
            out = [board] + soln

    return out


# Define the board configuration
# @ - player
# X - box
# * - target
# # - wall
boards = [
    [
        ".@.",
        ".X.",
        ".*."
    ],
    [
        "X##",
        "#@#",
        "##*"
    ],
    [
        "########",
        "#..#@.#.",
        "#....X.#",
        "#...#.X.",
        "#####**#",
        "....#.##",
        "....####"
    ]]

for board in boards:
   U=12+len(inspect.stack())
   result = soko_solver(board)
   print(U)
   if result is not None:
      print("Solution found:")
      print(result)
   else:
      print("No solution found.")
