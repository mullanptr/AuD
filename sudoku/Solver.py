import numpy as np
from board import board
from UnsolvableError import UnsolvableError

class _SingleSolver():

    def __init__(self, coords):
        self.coords = coords

    def _solve(self, board):

        if not hasattr(self, 'gen'):
            self.gen = iter(range(board.minval, board.maxval))

        for val in self.gen:
            if board.checker(coords=self.coords, val=val):
                return board.set_value(coords=self.coords, val=val)
        return False

    def _resetVal(self, board):
        board.board[(self.coords)] = board.empty_symbol

    def _resetAll(self, board):
        self._resetVal(board=board)
        del self.gen

class Solver():

    def _get_unsolved(self):
        coordss = np.where(self.board.board==0)
        return [_SingleSolver(coords) for coords in zip(*coordss)]

    def __init__(self, board):
        self.board=board
        self.unsolved = self._get_unsolved()
        self.ptr = 0

    def fit(self):
        forward_steps = 0
        backward_steps = 0
        while self.ptr != len(self.unsolved):
            if self.unsolved[self.ptr]._solve(self.board):
                self.ptr += 1
                forward_steps += 1
            else:
                self.unsolved[self.ptr]._resetAll(self.board)
                self.ptr -= 1
                self.unsolved[self.ptr]._resetVal(self.board)
                backward_steps += 1

            if self.ptr < 0:
                raise UnsolvableError('Could not determine a solution for the board.')

        print(f'Needed {forward_steps} forward and {backward_steps} backward steps.')

