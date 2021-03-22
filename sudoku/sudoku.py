import numpy as np
from board import board
from Solver import Solver

if __name__ == '__main__':
    b = board()
    print(b)
    S = Solver(b)
    S.fit()
    print(b)
