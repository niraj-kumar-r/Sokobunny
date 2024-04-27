from collections import deque
from typing import TypeAlias

directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

import inspect

def vec_plus(v1, v2):
   x = []
   for i in range(len(v1)):
      x.append(v1[i]+v2[i])
   return x

class Board:
   def __init__(self, baseboard):
      self.brd = baseboard

   def is_valid_move(self, pos):
      x, y = pos
      return 0 <= x < len(self.brd) and \
             0 <= y < len(self.brd[0]) and \
             self.brd[x][y] != '#'

   def find_children(self):
      childs=[]
      pos, _, __ = self.find_OoIs()
      for ele in directions:
         new_pos = vec_plus(pos, directions[ele])
         
         if self.is_valid_move(new_pos):
            new_brd = list(self.brd)
            if self.brd[new_pos[0]][new_pos[1]] == 'X': #Pushing the box
               block_new_pos = vec_plus(new_pos, directions[ele])
               if not self.is_valid_move(block_new_pos):
                  continue
               new_brd[block_new_pos[0]][block_new_pos[1]]="X"
            new_brd[pos[0]][pos[1]]="."
            new_brd[new_pos[0]][new_pos[1]]="@"
            childs.append(Board(new_brd))
      return childs
   
   @staticmethod
   def newmann_walking_distance(p1, p2):
      (x1, y1) = p1
      (x2, y2) = p2
      return abs(x1 - x2) + abs(y1 - y2)
   
   def solved(self):
      for row in self.brd:
         for cell in row:
            if cell=='*':
               return False
      return True
      
   def find_OoIs(self):
      """
      Returns the player, box and target positions
      """
      boxes=[]
      target_positions=[]
      for i in range(len(self.brd)):
         for j in range(len(self.brd[0])):
            if self.brd[i][j] == '@':
               robot_pos = (i, j)
            elif self.brd[i][j] == 'X':
               boxes.append((i, j))
            elif self.brd[i][j] == '*':
               target_positions.append((i, j))
      return (robot_pos, boxes, target_positions)
   
   def lower_bound(self):
      """
      You have to move at least one box to its destination starting from where you pick up;
      We take max(over boxes) of { min(over targets) of distance }
      """
      total_distance = 0
      robot_pos, boxes, target_positions = self.find_OoIs()
      min_targets = map(lambda box: min([Board.newmann_walking_distance(box, target) for target in target_positions]), boxes)
      min_distance = max(min_targets)
      return min_distance

   def __repr__(self):
      return '\n'.join(''.join(row) for row in self.brd)

def soko_solver(board):
   board = [list(row) for row in board]
   bord = Board(board)
   return DFBnB(bord)


def DFBnB(board: Board):
   global U
   if len(inspect.stack())>U:
      return None
   if board.solved():
      U=min(U, len(inspect.stack()))
      return [board] 
   
   out=None
   for brd in board.find_children():
      soln = DFBnB(brd)
      if soln is not None:
         out=[board].extend(soln)
   
   return out

# Define the board configuration
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
    "    #.##",
    "    ####"
   ]]

for board in boards:
   U=20
   result = soko_solver(board)
   print(U)
   if result is not None:
      print("Solution found:")
      print(result)
   else:
      print("No solution found.")