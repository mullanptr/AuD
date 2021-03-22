import numpy as np

class Error(Exception):
    pass
class UnsolvableError(Error):
    def __init__(self, meassage):
        self.message = message

class board():

    def __init__(self, h=3, w=3):
        self.h = h
        self.w = w
        self.empty_symbol = 0
        self.minval = 1
        self.maxval = h * w + 1
        self.possible_vals = set(range(self.minval, self.maxval))

        self.board = np.array(
                    [[5,3,0,0,7,0,0,0,0],
                    [6,0,0,1,9,5,0,0,0],
                    [0,9,8,0,0,0,0,6,0],
                    [8,0,0,0,6,0,0,0,3],
                    [4,0,0,8,0,3,0,0,1],
                    [7,0,0,0,2,0,0,0,6],
                    [0,6,0,0,0,0,2,8,0],
                    [0,0,0,4,1,9,0,0,5],
                    [0,0,0,0,8,0,0,7,9]])

        self.unsolved = list(zip(*np.where(self.board == 0)))

    def __str__(self):

        s = ''
        for r, row in enumerate(self.board):

            if r%3==0:
                s += '-' * (10 * 2 + 2)
                s += '\n'
            for c, col in enumerate(row):
                if c % 3==0:
                    s += '|'
                if col == 0:
                    s += '  '
                else:
                    s += str(col) + ' '
            else:
                s += '|'

            s += '\n'

        # dash on last line
        else:
            s += '-' * (10 * 2 + 2)
            s += '\n'

        return s

    def _getQuater(self, coords):
        x = (coords[1] // self.w) * self.w
        y = (coords[0] // self.h) * self.h
        tri = self.board[y:y+self.h, x:x+self.w].ravel()
        assert len(tri) == self.h * self.w
        return tri

    def _check(self, val, arr):
        return not val in arr

    def checker(self, coords, val):
        row = self.board[coords[0],:]
        col = self.board[:,coords[1]]
        tri = self._getQuater(coords)
        return self._check(val, row) and self._check(val,col) and self._check(val,tri)

    def set_value(self, coords, val):
        assert self.checker(coords=coords, val=val), f'Can not set {val} at {coords}.'
        self.board[coords] = val
        return True

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

if __name__ == '__main__':
        b = board()
        print(b)
        S = Solver(b)
        S.fit()
        print(b)
