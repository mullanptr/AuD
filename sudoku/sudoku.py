import numpy as np

class board():

    def __init__(self, h=3, w=3):
        self.h = h
        self.w = w
        self.empty_symbol = 0
        self.minval = 1
        self.maxval = h * w + 1
        self.possible_vals = set(range(self.minval, self.maxval+1))
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

    def get_next_unsolved(self):
        unsolved = list(zip(*np.where(self.board == 0)))
        for u in unsolved:
            yield u

    def try_next_val(self, shuffle=False):
        for p in self.possible_vals:
            yield p

    def _check(self, val, arr):
        if val in arr:
            return False
        return True

    def _gettri(self, coords):
        x = (coords[1] // self.w) * self.w
        y = (coords[0] // self.h) * self.h
        tri = self.board[y:y+self.h, x:x+self.w].ravel()
        assert len(tri) == self.h * self.w
        return tri

    def checker(self, coords, val):
        row = self.board[coords[0],:]
        col = self.board[:,coords[1]]
        tri = self._gettri(coords)
        return self._check(val, row) and self._check(val,col) and self._check(val,tri)

    def fit(self):
        backtrack_solved = []
        for u in self.get_next_unsolved():
            pass


if __name__ == '__main__':
        b = board()
        print(b)
        b.fit()
        print(b.checker(coords=(1,1),val=3))
        print(b.checker(coords=(3,1),val=2))
        print(b.checker(coords=(8,8),val=2))
        print(b.checker(coords=(5,5),val=2))

