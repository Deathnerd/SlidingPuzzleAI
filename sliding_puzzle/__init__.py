from copy import deepcopy

from PySide import QtGui, QtCore
from utils import *
import os


class GUI(QtGui.QMainWindow):
    grid_size = 3
    cell_size = 0
    actions = {}

    def __init__(self, grid_size=DIFFICULTY_EASY):
        super(GUI, self).__init__()
        self.grid_size = grid_size
        PuzzleBoard.BoardHeight = grid_size
        PuzzleBoard.BoardWidth = grid_size
        self.board = PuzzleBoard(self.grid_size)
        self.setup_window()
        self.show()

    def setup_window(self):
        self.setup_menu()
        self.statusBar()
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Main Window')
        label = QtGui.QLabel()
        label.setText(
            "To use this program, select a difficulty from the File menu above. \n\n"
            "Move pieces with the arrow keys. \n\n"
            "To solve, click Solve in the Puzzle menu. \n\n"
            "To reset the puzzle, click Reset in the Puzzle menu.")
        label.setGeometry(0, 0, 300, 300)
        self.setCentralWidget(label)

    def setup_menu(self):
        """
        Set up menus for the main window
        :return:
        """
        self.set_actions()

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.actions["set_easy_difficulty"])
        file_menu.addAction(self.actions["set_medium_difficulty"])
        file_menu.addAction(self.actions["set_hard_difficulty"])
        file_menu.addAction(self.actions["exit"])

        puzzle_menu = menu_bar.addMenu('&Puzzle')
        puzzle_menu.addAction(self.actions["solve"])
        puzzle_menu.addAction(self.actions["reset"])

    def set_actions(self):
        """
        Set all actions for the Main Window
        :return:
        """
        self.actions["exit"] = QtGui.QAction('Exit', self)
        self.actions["exit"].setShortcut('Ctrl+Q')
        self.actions["exit"].setStatusTip('Exit application')
        self.actions["exit"].triggered.connect(self.close)

        self.actions["solve"] = QtGui.QAction('Solve', self)
        self.actions["solve"].setShortcut('Ctrl+S')
        self.actions["solve"].setStatusTip('Solve the puzzle')
        self.actions["solve"].triggered.connect(self.solve)

        self.actions["reset"] = QtGui.QAction('Reset', self)
        self.actions["reset"].setShortcut('Ctrl+R')
        self.actions["reset"].setStatusTip('Reset the puzzle')
        self.actions["reset"].triggered.connect(self.reset)

        self.actions["set_easy_difficulty"] = QtGui.QAction('Easy Difficulty (3x3)', self)
        self.actions["set_easy_difficulty"].triggered.connect(self.set_easy)

        self.actions["set_medium_difficulty"] = QtGui.QAction('Medium Difficulty (5x5)', self)
        self.actions["set_medium_difficulty"].triggered.connect(self.set_medium)

        self.actions["set_hard_difficulty"] = QtGui.QAction('Hard Difficulty (8x8)', self)
        self.actions["set_hard_difficulty"].triggered.connect(self.set_hard)

    def set_easy(self):
        """
        Starts a new puzzle on easy difficulty
        :return:
        """
        self.grid_size = DIFFICULTY_EASY
        self.reset()

    def set_medium(self):
        """
        Starts a new puzzle on medium difficulty
        :return:
        """
        self.grid_size = DIFFICULTY_MEDIUM
        self.reset()

    def set_hard(self):
        """
        Starts a new puzzle on hard difficulty
        :return:
        """
        self.grid_size = DIFFICULTY_HARD
        self.reset()

    def solve(self):
        pass

    def reset(self):
        """
        Completely reset the puzzle board by destroying the object
        and creating it from scratch again
        :return:
        """
        self.board.close()
        del self.board
        self.board = PuzzleBoard(self.grid_size)
        self.board.show()


class PuzzleBoard(QtGui.QFrame):
    PieceSizes = {DIFFICULTY_EASY: 480 / DIFFICULTY_EASY,
                  DIFFICULTY_MEDIUM: 480 / DIFFICULTY_MEDIUM,
                  DIFFICULTY_HARD: 480 / DIFFICULTY_HARD}
    BoardHeight = 3
    BoardWidth = 3
    PieceSize = 0
    BeingSolved = False

    def __init__(self, grid_size, *args, **kwargs):
        super(PuzzleBoard, self).__init__(*args, **kwargs)
        self.difficulty = grid_size
        PuzzleBoard.BoardHeight = grid_size
        PuzzleBoard.BoardWidth = grid_size
        PuzzleBoard.PieceSize = self.PieceSizes[grid_size]
        self.setWindowTitle("Sliding Puzzle")
        self._layout = QtGui.QGridLayout()
        self.empty_piece_position = [grid_size - 1, grid_size - 1]
        self.pieces = self.set_pieces([[None for _ in range(grid_size)] for _ in range(grid_size)])

        # Set the
        for i, row in enumerate(self.pieces):
            for j, widget in enumerate(row):
                self._layout.addWidget(widget, i + 1, j + 1)
        self.setLayout(self._layout)

    def update_board(self):
        """
        A really hack-y way to force an update of the board. Remove all puzzle pieces from the
        layout and then add them back in to force an update.
        :return:
        """
        for row in self.pieces:
            for widget in row:
                self._layout.removeWidget(widget)
                widget.setParent(None)
        for i, row in enumerate(self.pieces):
            for j, widget in enumerate(row):
                self._layout.addWidget(widget, i + 1, j + 1)
        self.check_win()

    def keyPressEvent(self, event):
        if self.BeingSolved:
            QtGui.QWidget.keyPressEvent(self, event)
            return
        key = event.key()

        if key == QtCore.Qt.Key_Up:
            self.try_move_up(*self.empty_piece_position)
        elif key == QtCore.Qt.Key_Down:
            self.try_move_down(*self.empty_piece_position)
        elif key == QtCore.Qt.Key_Left:
            self.try_move_left(*self.empty_piece_position)
        elif key == QtCore.Qt.Key_Right:
            self.try_move_right(*self.empty_piece_position)
        else:
            QtGui.QWidget.keyPressEvent(self, event)

    def set_pieces(self, piece_list):
        if self.difficulty == DIFFICULTY_EASY:
            folder = "easy"
        elif self.difficulty == DIFFICULTY_MEDIUM:
            folder = "medium"
        else:
            folder = "hard"
        piece_size = self.PieceSizes[self.difficulty]
        left, upper, right, lower = 0, 0, piece_size, piece_size
        for row in range(self.difficulty):
            for column in range(self.difficulty):
                piece_list[row][column] = PuzzlePiece(os.path.join(resource_root, folder,
                                                                   "{row}{column}.jpg".format(row=row, column=column)),
                                                      left, upper, right, lower)
                left, upper, right, lower = left + piece_size, upper, right + piece_size, lower
            left, upper, right, lower = 0, upper + piece_size, piece_size, lower + piece_size
        return piece_list

    def try_move_up(self, empty_piece_x, empty_piece_y):
        """Attempt to move the block below the empty space up
        :param empty_piece_x:
        :param empty_piece_y:
        """
        if empty_piece_y < self.difficulty - 1:
            empty_piece = self.pieces[empty_piece_y][empty_piece_x]
            other_piece = self.pieces[empty_piece_y + 1][empty_piece_x]
            other_piece.move_up()
            empty_piece.move_down()
            self.pieces[empty_piece_y][empty_piece_x] = other_piece
            self.pieces[empty_piece_y + 1][empty_piece_x] = empty_piece
            self.empty_piece_position[1] += 1
            self.update_board()

    def try_move_down(self, empty_piece_x, empty_piece_y):
        """Attempt to move the block above the empty space down
        :param empty_piece_x:
        :param empty_piece_y:
        """
        if empty_piece_y >= 1:
            empty_piece = self.pieces[empty_piece_y][empty_piece_x]
            other_piece = self.pieces[empty_piece_y - 1][empty_piece_x]
            other_piece.move_down()
            empty_piece.move_up()
            self.pieces[empty_piece_y][empty_piece_x] = other_piece
            self.pieces[empty_piece_y - 1][empty_piece_x] = empty_piece
            self.empty_piece_position[1] -= 1
            self.update_board()

    def try_move_left(self, empty_piece_x, empty_piece_y):
        """Attempt to move the block to the right of the empty space to the left
        :param empty_piece_x:
        :param empty_piece_y:
        """
        if empty_piece_x < self.difficulty - 1:
            empty_piece = self.pieces[empty_piece_y][empty_piece_x]
            other_piece = self.pieces[empty_piece_y][empty_piece_x + 1]
            other_piece.move_left()
            empty_piece.move_right()
            self.pieces[empty_piece_y][empty_piece_x] = other_piece
            self.pieces[empty_piece_y][empty_piece_x + 1] = empty_piece
            self.empty_piece_position[0] += 1
            self.update_board()

    def try_move_right(self, empty_piece_x, empty_piece_y):
        """Attempt to move the block to the left of the empty space to the right
        :param empty_piece_x:
        :param empty_piece_y:
        """
        if empty_piece_x >= 1:
            empty_piece = self.pieces[empty_piece_y][empty_piece_x]
            other_piece = self.pieces[empty_piece_y][empty_piece_x - 1]
            other_piece.move_right()
            empty_piece.move_left()
            self.pieces[empty_piece_y][empty_piece_x] = other_piece
            self.pieces[empty_piece_y][empty_piece_x - 1] = empty_piece
            self.empty_piece_position[0] -= 1
            self.update_board()

    def check_win(self):
        """
        Iterates through each puzzle piece to and determines if they're all in the correct place.
        If they are, opens a message box telling the user they've correctly solved the puzzle
        :return: win True if there's a win condition, false if otherwise
        """
        win = all(all(piece.is_correct for piece in row) for row in self.pieces)
        if win:
            msgbox = QtGui.QMessageBox()
            msgbox.setText("That's correct!")
            msgbox.setWindowTitle("Sliding Puzzle")
            msgbox.exec_()
        return win


class PuzzlePiece(QtGui.QLabel):
    x_pos = 0
    y_pos = 0

    def __init__(self, image_path, left, upper, right, lower):
        super(PuzzlePiece, self).__init__()
        self.setScaledContents(True)
        self.setPixmap(QtGui.QPixmap(image_path))
        self.setGeometry(QtCore.QRect(left, upper, right, lower))
        self.x_pos = left
        self.y_pos = upper
        self.original_x = left
        self.original_y = upper
        self.left = left
        self.upper = upper
        self.right = right
        self.lower = lower

    @property
    def is_correct(self):
        return self.x_pos == self.original_x and self.y_pos == self.original_y

    def move_up(self):
        self.y_pos -= PuzzleBoard.PieceSize

    def move_down(self):
        self.y_pos += PuzzleBoard.PieceSize

    def move_left(self):
        self.x_pos -= PuzzleBoard.PieceSize

    def move_right(self):
        self.x_pos += PuzzleBoard.PieceSize


# TODO: Add AI to solve
class AI:
    timer = QtCore.QBasicTimer

    def __init__(self, board):
        self.board = board
        PuzzleBoard.BeingSolved = True

    def solve(self):
        pass

    def feasability_check(self, move):
        pieces = deepcopy(self.board.pieces)
        if move == "up":
            pass
        elif move == "down":
            pass
        elif move == "left":
            pass
        elif move == "right":
            pass
        return score