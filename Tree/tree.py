from abc import ABC, abstractmethod

class _AbstractNode(ABC):

    @abstractmethod
    def __contains__(self):
        pass

    @abstractmethod
    def __getitem__(self):
        pass

    @abstractmethod
    def __setitem__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

class _Leaf(_AbstractNode):

    def __init__(self):
        pass

    def __contains__(self, key):
        return False

    def __getitem__(self, key):
        raise ValueError(f'Element "{key}" not in Datastructure.')

    def __setitem__(self, *args):
        raise Error('Something went fundamentally wrong!\nReached __setitem__() of class _Leaf; Should never happen.')

    def __str__(self):
        return '_'

    def __len__(self):
        return 0

class Node(_AbstractNode):

    def __init__(self, key=None, value=None):

        if key:
            self.key = key
        self.value = value
        self.left = _Leaf()
        self.right = _Leaf()

    def _haskey__(self):
        return hasattr(self,'key')

    def __str__(self):
        return f' ({str(self.left)}-{str(self.value)}-{str(self.right)}) '

    def __contains__(self, key):
        if (k:= not self._haskey__()): return k # key is None -> not a grown tree
        return self.key == key or (key in self.left) or (key in self.right)

    def __getitem__(self, key):
        if (k:= not self._haskey__()): raise ValueError # key is None -> not a grown tree
        if self.key==key: return self.value
        if self.key < key:
            return self.left[key]
        if self.key > key:
            return self.right[key]

    def __setitem__(self, key, value):
        if (k:= not self._haskey__()): self.key=key; self.value=value; return # override default init with None
        if self.key == key: self.value = value; return

        if self.key < key:
            if isinstance(self.left, _Leaf):
                self.left = Node(key=key, value=value)
            else:
                self.left[key] = value
            return
        if self.key > key:
            if isinstance(self.right, _Leaf):
                self.right = Node(key=key, value=value)
            else:
                self.right[key] = value
            return

    def __len__(self):
        return 1 + len(self.left) + len(self.right)

if __name__ == '__main__':
    T = Node()
    T['b'] = 2
    T['c'] = 3
    T['d'] = 4
    T['e'] = 5
    T['n'] = 9
    T['m'] = 8
    T['l'] = 7
    T['o'] = 10
    print(T)

    print(T['n'])
    print(T['b'])
    print(T['l'])

