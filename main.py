from __future__ import annotations
from enum import Enum

import random as rd
import sys


class IntVector():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, vec: IntVector) -> IntVector:
        newX: int = self.x + vec.x
        newY: int = self.y + vec.y
        return IntVector(newX, newY)


    def __floordiv__(self, divisor: int) -> IntVector:
        newX: int = self.x // divisor
        newY: int = self.y // divisor
        return IntVector(newX, newY)


    def __truediv__(self, divisor: int) -> IntVector:
        return self.__floordiv__(divisor)



class States(Enum):
    FREE = 0   # not visited
    WALL = 1   # you won't believe it
    VIS  = 2   # visited



class Direction(Enum):
    N = IntVector( 0, -2)
    E = IntVector( 2,  0)
    S = IntVector( 0,  2)
    W = IntVector(-2,  0)



class MazeConstructor():
    def __init__(self, height: int, width: int) -> None:
        self.width  =  width if  width % 2 == 1 else  width + 1
        self.width  = self.width + 4

        self.height = height if height % 2 == 1 else height + 1
        self.height = self.height + 4

        self.maze   = self.__init_maze_grid()


    def create_maze(self) -> None:
        startX: int = rd.randint(1, self.width  // 2 - 1) * 2
        startY: int = rd.randint(1, self.height // 2 - 1) * 2

        start = IntVector(startX, startY)

        self.__make_path(start)
        self.__clean_maze()


    def get_maze(self) -> list[list[int]]:
        new_maze = list()
        for i in range(len(new_maze)):
            for j in range(len(new_maze[i])):
                new_maze[i][j] = new_maze[i][j].value

        return new_maze


    def __make_path(self, cell: IntVector) -> None:
        self.maze[cell.y][cell.x] = States.VIS

        if self.__all_surrounding_visited(cell):
            return

        directions: list = [
            Direction.N,
            Direction.E,
            Direction.S,
            Direction.W,
        ]

        while directions:
            direction = rd.choice(directions)
            directions.remove(direction)

            if not self.__direction_free(cell, direction):
                continue

            wall_between, next_cell = self.__go_from_to(cell, direction)
            self.maze[wall_between.y][wall_between.x] = States.VIS
            self.__make_path(next_cell)


    def __clean_maze(self) -> None:
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == States.VIS:
                    self.maze[i][j] = States.FREE

        new_maze = list()
        for i in range(1, len(self.maze) - 1):
            row_len = len(self.maze[i])
            new_maze.append(self.maze[i][1:row_len - 1])

        self.maze = new_maze


    def __go_from_to(self, cell: IntVector, direction: Direction) -> tuple[IntVector, IntVector]:
        next_cell: IntVector    = cell + direction.value
        wall_between: IntVector = cell + (direction.value / 2)
        return wall_between, next_cell


    def __direction_free(self, cell: IntVector, direction: Direction) -> bool:
        next_cell: IntVector = cell + direction.value
        return (self.maze[next_cell.y][next_cell.x] == States.FREE)


    def __all_surrounding_visited(self, cell: IntVector) -> bool:
        all_visited = True
        for move in Direction:
            next_cell: IntVector = cell + move.value
            cell_is_visited: bool = (self.maze[next_cell.y][next_cell.x] == States.VIS)
            all_visited = all_visited and cell_is_visited

        return all_visited


    def __init_maze_grid(self) -> list[list[States]]:
        maze = list()
        for i in range(self.height):
            row = list()
            for j in range(self.width):
                edge_case = (i == 0 or j == 0 or
                             i == self.height - 1 or 
                             j == self.width - 1)
                if   edge_case:
                    row.append(States.VIS)
                elif i % 2 == 0 and j % 2 == 0:
                    row.append(States.FREE)
                else:
                    row.append(States.WALL)

            maze.append(row)
        return maze


    def __repr__(self) -> str:
        repr: str = ""
        for row in self.maze:
            for cell in row:
                if   cell == States.FREE:
                    repr += " "
                elif cell == States.VIS:
                    repr += "X"
                elif cell == States.WALL:
                    repr += "█" 
                else:
                    repr += "?"
            repr += "\n"

        return repr


def __parse_args() -> tuple[int, int]:
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--width',  type=int, default=1,
                        help="width of the labirynth in cells")
    parser.add_argument('--height', type=int, default=1,
                        help="height of the labirynth in cells")

    args = parser.parse_args()

    return args.width, args.height


def __main() -> None:
    width, height = __parse_args()

    sys.setrecursionlimit((width + 4) * (height + 4))

    mazer = MazeConstructor(height, width)
    mazer.create_maze()
    print(mazer)


if __name__ == "__main__":
    __main()
