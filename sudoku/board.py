import numpy as np

class board():

    def __init__(self, np2darr):

        self.h, self.w = np2darr.shape
        assert self.h == self.w, f'Only rectangular boards allowed; Board has shape: {np2darr.shape}'
        self.quaterLen = int(np.sqrt(self.h))
        self.board = np2darr

        self.empty_symbol = 0
        self.minval = 1
        self.maxval = self.h

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
        x = (coords[1] // self.quaterLen) * self.quaterLen
        y = (coords[0] // self.quaterLen) * self.quaterLen
        tri = self.board[y:y+self.quaterLen, x:x+self.quaterLen].ravel()
        assert len(tri) == self.quaterLen * self.quaterLen
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

