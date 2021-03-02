# Collection of Algorithms and Data Structures

## Purpose:

* Started to implement fundamental algorithms and data structures to **recap and enhance** my python skills. The
  software packages should do their jobs -- I tested them on small scales.
  However, this is more of a ''practice notebook'' for me.
* Besides recapping algorithms and data structures, I also code
  granularized and object-oriented, to **exercise a good coding habit**, as well.

## Content:

### Binarized Search-Tree

Binarized Search-Trees help to find objects rapidly.
They are realized to work with `key-value-pairs`.
That is, each object is a value and can be addressed by a unique key.
This results in an interface, which is similar to the dictionaries (`dict`) data structure in python.
However, the on-board python dictionaries are implemented as hash-maps.

I overwrote magic methods like `__getitem__()` or `__setitem__()` which enables writing and 
reading elements in a tree `t` with `t[key] = value`, making them behave like dictionaries
as close as possible.

### Information Gain

Splitting a tree according to the highest information gain possible

Will be used in an implementaion of a single random tree -> Will be used in an implementation of a random forest

