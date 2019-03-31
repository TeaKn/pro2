#!/usr/bin/python
# coding=utf8

from time import *
import re
import os

class GraphException(Exception):
  """
  Class storing a graph exception raised when the graph is empty.
  """
  def __init__(self):
    Exception.__init__(self, "graph is empty since it contains no nodes")

class NodeException(GraphException):
  """
  Class storing a node exception raised when the node does not exist.
  """
  def __init__(self, i):
    GraphException.__init__(self, "node with index {0:d} does not exist".format(i))

class EdgeException(GraphException):
  """
  Class storing an edge exception raised when the edge does not exist.
  """
  def __init__(self, i, j):
    GraphException.__init__(self, "edge between nodes with indices {0:d} and {1:d} does not exist".format(i, j))

class UnsupportedException(Exception):
  """
  Class storing an exception raised when unsupported function is called.
  """
  def __init__(self):
    Exception.__init__(self, "unsupported operation for this class")

class Graph:
  """
  Class storing an undirected graph represented by its name, adjacency list A and node labels L.
  Class contains standard functions for accessing the graph and adding nodes or edges.
  """
  def __init__(self, name, n = 0):
    self.A = [[] for _ in range(n)]
    self.name = name
    self.L = None
    self.n = n
    self.m = 0

  def __str__(self):
    start = time()
    C = Graph.components(self)
    return "{0:>12s} | '{1:s}'\n{2:>12s} | '{3:s}'\n{4:>12s} | {5:,d} ({6:,d})\n{7:>12s} | {8:,d} ({9:,d})\n{10:>12s} | {11:.4f}\n{12:>12s} | {13:.1f}% ({14:,d})\n{15:>12s} | {16:.1f} sec\n".format('Graph', self.name, 'Type', ('x' if self.is_labeled() else '0') + ('--' if self.is_simple() else '==') + ('y' if self.is_labeled() else '1'), 'Nodes', self.n, self.get_s(), 'Edges', self.m, self.get_l(), 'Degree', self.get_k(), 'LCC', 100.0 * max([len(c) for c in C]) / self.n, len(C), 'Time', time() - start)

  def get_name(self):
    return self.name

  def get_n(self):
    return self.n
  
  def get_m(self):
    return self.m
  
  def get_k(self):
    if self.n == 0:
      raise GraphException()
    return 2.0 * self.get_m() / self.get_n()
  
  def get_s(self):
    s = 0
    for i in range(self.n):
      if self.get_degree(i) == 0:
        s += 1
    return s
  
  def get_l(self):
    l = 0
    for i in range(self.n):
      l += self.A[i].count(i) / 2
    return l
  
  def get_nodes(self):
    return list(range(self.n))
  
  def get_edges(self):
    return [(i, j) for i in range(self.n) for j in self.get_neighbours(i) if i < j] + [(i, i) for i in range(self.n) for _ in range(self.get_neighbours(i).count(i) / 2)]

  def is_simple(self):
    for a in self.A:
      if len(set(a)) < len(a):
        return False
    return True

  def is_multi(self):
    return not self.is_simple()
  
  def is_labeled(self):
    return self.L is not None
  
  def is_node(self, i):
    return i < self.n
  
  def is_edge(self, i, j):
    if not self.is_node(i):
      raise NodeException(i)
    elif not self.is_node(j):
      raise NodeException(j)
    return self.get_degree(i) < self.get_degree(j) and j in self.get_neighbours(i) or self.get_degree(i) >= self.get_degree(j) and i in self.get_neighbours(j)

  def add_node(self, label = None):
    self.n += 1
    self.A.append([])
    if label is not None:
      if self.L is None:
        self.L = [None for _ in range(self.n)]
      else:
        self.L.append(None)
      self.L[self.n - 1] = label
    return self.n - 1

  def add_edge(self, i, j):
    if not self.is_node(i):
      raise NodeException(i)
    elif not self.is_node(j):
      raise NodeException(j)
    self.A[i].append(j)
    self.A[j].append(i)
    self.m += 1

  def add_loop(self, i):
    self.add_edge(i, i)
  
  def remove_edge(self, i, j):
    if not self.is_edge(i, j):
      raise EdgeException(i, j)
    self.A[i].remove(j)
    self.A[j].remove(i)
    self.m -= 1

  def set_label(self, i, label = None):
    if not self.is_node(i):
      raise NodeException(i)
    if self.L is None:
        self.L = [None for _ in range(self.n)]
    self.L[i] = label

  def get_label(self, i):
    if not self.is_node(i):
      raise NodeException(i)
    return None if self.L is None else self.L[i]

  def get_degree(self, i):
    return len(self.get_neighbours(i))

  def get_neighbours(self, i):
    if not self.is_node(i):
      raise NodeException(i)
    return self.A[i]
  
  @staticmethod
  def component(G, N, i):
    """
    Find connected component of node i in graph G represented by class Graph considering nodes in list N.
    Function returns a list of node indices C in connected component of node i and removes them from list N.
    """
    C = []
    S = []
    N.remove(i)
    S.append(i)
    while S:
      i = S.pop(0)
      C.append(i)
      for j in G.get_neighbours(i):
        if j in N:
          N.remove(j)
          S.insert(0, j)
    return C

  @staticmethod
  def components(G):
    """
    Find connected components of graph G represented by class Graph.
    Function returns a list of lists C of node indices in connected components computed by `component(G, N, i)`.
    """
    C = []
    N = G.get_nodes()
    while N:
      C.append(Graph.component(G, N, N[0]))
    return C

  @staticmethod
  def pajek(name, path = '.'):
    """
    Read a graph from the specified file in Pajek format.
    Function returns graph G represented by class Graph.
    """
    G = None
    with open(os.path.join(path, name + '.net'), 'r') as file:
      for line in file:
        if re.match(r'^\*vertices', line):
          G = Graph(name, int(re.split('\s+', line)[1]))
        elif re.match(r'^\*(edges|arcs)', line):
          break
        else:
          node = re.split('"', line)
          if len(node) > 1 and len(node[1]):
            G.set_label(int(node[0]) - 1, node[1])
      for line in file:
        edge = re.split('\s+', line)
        G.add_edge(int(edge[0]) - 1, int(edge[1]) - 1)
    return G

  @staticmethod
  def write(G, path = '.'):
    """
    Write graph G to the default file in Pajek format.
    Function returns graph G represented by class Graph.
    """
    with open(os.path.join(path, G.get_name() + '.net'), 'w') as file:
      file.write('*vertices {0:d}\n'.format(G.get_n()))
      for i in G.get_nodes():
        file.write('{0:d}{1:s}\n'.format(i + 1, ' "' + G.get_label(i) + '"' if G.is_labeled() else ''))
      file.write('*edges {0:d}\n'.format(G.get_m()))
      for i in G.get_nodes():
        for _ in range(G.get_neighbours(i).count(i) / 2):
          file.write('{0:d} {0:d}\n'.format(i + 1))
        for j in G.get_neighbours(i):
          if i < j:
            file.write('{0:d} {1:d}\n'.format(i + 1, j + 1))
    return G

class Path(Graph):
  """
  Class storing an undirected path graph represented by its name, adjacency list A and node labels L.
  Class contains standard functions for accessing the path graph and adding nodes with edges.
  """
  def __init__(self, name, n = 0):
    Graph.__init__(self, name, n)
    for i in range(n - 1):
      Graph.add_edge(self, i, i + 1)

  def add_node(self, label = None):
    Graph.add_node(self, label)
    Graph.add_edge(self, self.n - 2, self.n - 1)
    return self.n - 1

  def add_edge(self, i, j):
    raise UnsupportedException()

class Cycle(Graph):
  """
  Class storing an undirected cycle graph represented by its name, adjacency list A and node labels L.
  Class contains standard functions for accessing the cycle graph and adding nodes with edges.
  """
  def __init__(self, name, n = 0):
    Graph.__init__(self, name, n)
    for i in range(n):
      Graph.add_edge(self, i, (i + 1) % n)
    
  def add_node(self, label = None):
    Graph.add_node(self, label)
    Graph.add_edge(self, self.n - 2, self.n - 1)
    Graph.add_edge(self, 0, self.n - 1)
    Graph.remove_edge(self, 0, self.n - 2)
    return self.n - 1

  def add_edge(self, i, j):
    raise UnsupportedException()
