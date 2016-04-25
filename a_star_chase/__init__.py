from __future__ import print_function
import os

from astar import AStar
from utils import resource_root
from random import randint


class Board:
    """
    Contains most of the logic for maintaining a board for the A* algorithm game
    """
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        ########################################
        # Store tiles as tuples of coordinates #
        ########################################
        # Player is in the top-left of the map
        self.player = (1, 1)
        # While the enemy is in the bottom-right
        self.enemy = (8, 8)
        self.walls = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (0, 1), (9, 1),
                      (0, 2), (3, 2), (6, 2), (9, 2), (0, 3), (2, 3), (3, 3), (6, 3), (7, 3), (9, 3), (0, 4), (9, 4),
                      (0, 5), (9, 5), (0, 6), (2, 6), (3, 6), (6, 6), (7, 6), (9, 6), (0, 7), (3, 7), (6, 7), (9, 7),
                      (0, 8), (9, 8), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)}
        # Oh, and he's sitting on the goal at the beginning. Awesome.
        self.goal = (8, 8)
        # Don't need to try and calculate antyhing we can't visit, so
        # generate width*height tuples and do a set difference from them
        # with the walls because we can't walk through walls...
        self.graph = set([(i, j) for i in range(0, width) for j in range(0, height)]) - self.walls
        # Each passable tile will have a random weight from 3 to 15.
        # This simulates a randomly overgrown grassy stage.
        # Also, I love hash tables. So awesome!
        self.weights = {tile: randint(5, 20) for tile in self.graph}

    def move_entity(self, tile_type, x, y):
        """
        Move an entity (player or enemy) on the board
        :param tile_type: player or enemy as string
        :param x: The new x position
        :param y: The new y position
        :return:
        """
        # We can't walk through walls, Felicia!
        if tile_type.lower() == "player" and (x, y) not in self.walls:
            self.player = (x, y)
        # We didn't code the enemy to do so either...
        # If it does though, call an exorcist!
        elif tile_type.lower() == "enemy":
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
        # It's possible that we can visit all 4 nodes surrounding our current one
        possible_nodes = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        # How many times do I have to say it? We can't walk through walls!
        return [t for t in possible_nodes if self.in_bounds(t) and t not in self.walls]

    def cost(self, to_node):
        """
        Through the magic of hash tables, we can look up a weight (cost)
        for a node in O(1) time!
        :param to_node:
        :return:
        """
        return self.weights[to_node]

    def render_tile(self, tile, path=list(), width=3):
        """
        Determines how to render a tile while rendering the board
        :param tile: The tile coordinates
        :param path: A list of tiles to illustrate as a path
        :param width: The width of a tile
        :return: The tile!
        """
        if tile == self.player:
            # There's a potty humor joke here, but I'm tired
            return "P"
        elif tile == self.enemy:
            # Python strings do not support evil, maniacal laughter,
            # so this will have to do for the enemy
            return "E"
        elif tile in path:
            # A path tile should be surprising! It's how you die!
            return "!"
        elif tile in self.walls:
            # Render a wall as something pretty solid
            return "#" * width
        else:
            # Okay! So this is a traversable tile! Get the weight because
            # it'll determine how heavy the grass is
            weight = self.weights[tile]
            if 5 <= weight <= 10:
                # Freshly manicured
                return "."
            elif 11 <= weight <= 15:
                # A week or so without trimming
                return ","
            # Fire the gardener
            return ";"

    def render(self, width=2, path=list()):
        """
        Render the board
        :param width: The width of a tile
        :param path: The path the evil guy will take!
        :return:
        """
        for y in range(self.height):
            for x in range(self.width):
                print("%%-%ds" % width % self.render_tile((x, y), path, width), end="")
            print()


def run():
    # Initialize a 10x10 stage. No other stage sizes are
    # coded yet, but these constructor arguments exist in
    # case we want to later on
    board = Board()

    # Initialize the A-Star algorithm class with our
    # current graph and reference to the board because
    # I'm lazy. It shouldn't have a dependency on a board,
    # but it's been 8 hours already and I'm tired.
    astar = AStar(board.graph, board)
    # Render the board to show where we stand
    board.render()
    inp = get_input()
    while inp[0].lower() not in "qe":
        if inp[0].lower() in "h":
            # Players is babies and wants helps!
            with open(os.path.join(resource_root, "maze", "help.txt"), "rb") as help_file:
                print(help_file.read())
            board.render()
            inp = raw_input("Next move? (enter h or help for help)").strip()
            if inp == "":
                inp = " "
            continue
        # Try to move the player. Run, Forrest! Run!
        if inp[0].lower() == "u":
            (x, y) = board.player
            board.move_entity("player", x, y - 1)
        elif inp[0].lower() == "d":
            (x, y) = board.player
            board.move_entity("player", x, y + 1)
        elif inp[0].lower() == "l":
            (x, y) = board.player
            board.move_entity("player", x - 1, y)
        elif inp[0].lower() == "r":
            (x, y) = board.player
            board.move_entity("player", x + 1, y)

        # The enemy is a greedy bastard and moves every chance he can
        path = astar.get_path(astar.search(board.enemy, board.player)[0], board.enemy, board.player)
        board.move_entity("enemy", *path[1])
        board.render(path=path[2:-1])
        if board.enemy == board.player:
            print("You lost!")
            exit()
        if board.player == board.goal:
            print("You escaped death! Huzzah!")
            exit()
        inp = get_input()
    print("Scaredy-cat!")


def get_input():
    inp = raw_input("Next move? (enter h or help for help) ").strip()
    return " " if inp == "" else inp


if __name__ == "__main__":
    run()
