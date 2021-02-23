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

    def traverse(self):
        return []

    def keys(self):
        return None

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

    def traverse(self):
        if (k:= not self._haskey__()): raise RuntimeError # key is None -> not a grown tree
        return [(self.key, self.value)] + self.left.traverse() + self.right.traverse()

    def keys(self):
        if (k:= not self._haskey__()): raise RuntimeError # key is None -> not a grown tree
        yield self.key
        if not isinstance(self.left, _Leaf):
            for k in self.left.keys():
                yield k
        if not isinstance(self.right, _Leaf):
            for k in self.right.keys():
                yield k

    def values(self):
        if (k:= not self._haskey__()): raise RuntimeError # key is None -> not a grown tree
        yield self.value
        if not isinstance(self.left, _Leaf):
            for v in self.left.values():
                yield v
        if not isinstance(self.right, _Leaf):
            for v in self.right.values():
                yield v

    def items(self):
        if (k:= not self._haskey__()): raise RuntimeError # key is None -> not a grown tree
        yield (self.key, self.value)
        if not isinstance(self.left, _Leaf):
            for k, v in self.left.items():
                yield k, v
        if not isinstance(self.right, _Leaf):
            for k, v in self.right.items():
                yield k, v

    def __iadd__(self, other, overwrite=True):
        for k, v in other.items():
            if k not in self or overwrite:
                self[k] = v
        return self

    def __add__(self, other, overwrite=True):
        new = Node()
        for k, v in self.items():
            new[k] = v
        for k, v in other.items():
            if k not in self or overwrite:
                new[k] = v
        return new

    def _haskey__(self):
        return hasattr(self,'key')

    def __str__(self):
        return f' ({str(self.left)} - {str(self.key)}: {str(self.value)} - {str(self.right)}) '

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
    T1 = Node()
    T1['b'] = 2
    T1['c'] = 3
    T1['d'] = 4
    T1['e'] = 5
    T1['n'] = 9
    T1['m'] = 8
    T1['l'] = 7
    T1['o'] = 10

    print(T1.traverse())

    T2 = Node()
    T2['g'] = 2
    T2['h'] = 3
    T2['i'] = 4
    T2['j'] = 5
    T2['k'] = 9
    T2['f'] = 8
    T2['z'] = 7
    T2['y'] = 10

    print(T1+T2)
