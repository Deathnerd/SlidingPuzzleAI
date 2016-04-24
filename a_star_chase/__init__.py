import os

from astar import AStar
from utils import render_board, get_path, resource_root
from random import randint


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        ########################################
        # Store tiles as tuples of coordinates #
        ########################################
        self.player = (1, 1)
        self.enemy = (8, 8)
        self.walls = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0),
                      (0, 1), (9, 1),
                      (0, 2), (3, 2), (6, 2), (9, 2),
                      (0, 3), (2, 3), (3, 3), (6, 3), (7, 3), (9, 3),
                      (0, 4), (9, 4),
                      (0, 5), (9, 5),
                      (0, 6), (2, 6), (3, 6), (6, 6), (7, 6), (9, 6),
                      (0, 7), (3, 7), (6, 7), (9, 7),
                      (0, 8), (9, 8),
                      (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9),
                      ]
        self.goal = (8, 8)
        self.graph = [(i, j) for i in range(0, width) for j in range(0, height)]
        # Each passable tile will have a random weight from 3 to 15
        self.weights = {tile: randint(3, 15) for tile in self.graph}

    def move_entity(self, tile_type, x, y):
        if tile_type == "player" and (x, y) not in self.walls:
            self.player = (x, y)
        elif tile_type == "enemy":
            self.enemy = (x, y)

    def in_bounds(self, coords):
        """
        Check if the coordinates requested are in bounds of the board
        :param coords:
        :return:
        """
        (x, y) = coords
        return 0 <= x < self.width and 0 <= y < self.height

    def nodes_to_visit(self, tile):
        """
        Given a tuple of x,y coordinates, return the neighbors of the node that are visitable (passable and in range)
        :param tile: The node to get neighbors from
        :return: A list of 0 to 4 neighbors that are visitable
        """
        (x, y) = tile
        return [t for t in [(x + 1, y), (x, y - 1),
                            (x - 1, y), (x, y + 1)] if self.in_bounds(t) and t not in self.walls]

    def cost(self, to_node):
        return self.weights.get(to_node, 1)


def run():
    board = Board(10, 10)

    inp = ""
    astar = AStar(board.graph, board)
    while inp.lower() not in ("quit", "q", "exit", "e"):
        if inp.lower() in ("help", "h"):
            with open(os.path.join(resource_root, "maze", "help.txt"), "rb") as help_file:
                print(help_file.read())
            inp = raw_input("Next move? (enter h or help for help)")
            continue
        if inp.lower() in ("up", "u"):
            (x, y) = board.player
            board.move_entity("player", x, y - 1)
        elif inp.lower() in ("down", "d"):
            (x, y) = board.player
            board.move_entity("player", x, y + 1)
        elif inp.lower() in ("left", "l"):
            (x, y) = board.player
            board.move_entity("player", x - 1, y)
        elif inp.lower() in ("right", "r"):
            (x, y) = board.player
            board.move_entity("player", x + 1, y)

        come_from, cost_so_far = astar.search(board.enemy, board.player, board.graph)
        path = get_path(come_from, board.enemy, board.player)
        board.move_entity("enemy", path[1][0], path[1][1])
        path = path[2:-1]
        render_board(board, start=board.enemy, end=board.player, width=2, path=path)
        if board.enemy == board.player:
            print("You lost!")
            break
        if board.player == board.goal:
            print("You escaped death! Huzzah!")
            break
        inp = raw_input("Next move? (enter h or help for help) ")


if __name__ == "__main__":
    run()
