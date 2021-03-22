class tmp():
    def _getgen(self):
        self.gen = range(1,5)
    def __init__(self):
        self._getgen()
    def getval(self):
        for g in self.gen:
            print(g)
            if g > 2:
                break

t = tmp() # init the object; including the range within the object

t.getval() # As expected numbers 1,2,3

t.getval() # Expect Number 4; but get again 1,2,3
