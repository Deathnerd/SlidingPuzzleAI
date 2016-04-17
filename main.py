from sliding_puzzle import GUI
import sys
from PySide import QtGui
from utils import *

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = GUI(grid_size=DIFFICULTY_HARD)
    sys.exit(app.exec_())