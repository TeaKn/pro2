from Piii import *
from random import *
import operator as op
import requests

def DC(G):
  """
  Compute degree centrality of nodes in a graph represented by class Graph.
  Function returns a list of degree centralities of each node represented by its index.
  """
  DCs = [0.0] * G.get_n()
  
  for i in G.get_nodes():
    DCs[i] = G.get_degree(i) / G.get_n()
  
  return DCs

def EC(G):
  """
  Compute eigenvector centrality of nodes in a graph represented by class Graph.
  Function returns a list of eigenvector centralities of each node represented by its index.
  """
  ECs = [1.0 / G.get_n()] * G.get_n()
  
  for _ in range(100):
    nECs = [0.0] * G.get_n()
    for i in G.get_nodes():
      for j in G.get_neighbours(i):
        nECs[i] += ECs[j]
  
    sEC = sum(nECs)
    ECs = [ec / sEC for ec in nECs]
    
  return ECs

def PR(G, alpha = 0.85):
  """
  Compute PageRank centrality of nodes in a graph represented by class Graph.
  Function returns a list of PageRank centralities of each node represented by its index.
  """
  PRs = [1.0 / G.get_n()] * G.get_n()
  
  nodes = G.get_nodes()
  for _ in range(100):
    nPRs = [0.0] * G.get_n()
    shuffle(nodes)
    for i in nodes:
      for j in G.get_neighbours(i):
        nPRs[i] += PRs[j] * alpha / G.get_degree(j)
  
    sPR = sum(nPRs)
    PRs = [pr + (1.0 - sPR) / G.get_n() for pr in nPRs]

  return PRs

def tops(G, C, l = 'Centrality', n = 10):
  """
  Print out top centrality nodes in graph G represented by class Graph.
  Method prints out top n nodes according to centrality function C.
  """
  start = time()
  
  print("{0:>25s} | {1:s}".format('Node', l))
  for i, lc in enumerate(sorted({G.get_label(i): c for i, c in enumerate(C(G))}.items(), key = op.itemgetter(1), reverse = True)):
    if i < n:
      print("{0:>25s} | {1:e}".format("'" + lc[0] + "'", lc[1]))
  
  print("{0:>25s} | {1:.1f} sec\n".format('Time', time() - start))

def analysis(G):
  """
  Analyse node centrality of graph G represented by class Graph.
  Method prints out standard information of graph G and top centrality nodes.
  """
  print(G)

  tops(G, lambda G: DC(G), 'Degrees')
  tops(G, lambda G: EC(G), 'Eigenvectors')
  tops(G, lambda G: PR(G), 'PageRanks')

# analyzes node centralities of various real networks

analysis(Graph.read('dolphins'))
analysis(Graph.read('football'))
analysis(Graph.read('lovrosubelj'))
analysis(Graph.read('imdb'))

# parses GoT kills network from online source

G = Graph('got_kills')

indices = {}
for line in re.findall(r'<li>[^-]+\s-\s[^.]+.', requests.get('https://listofdeaths.fandom.com/wiki/Game_of_Thrones').text):
  killing = re.sub(r'<.*?>|\(.*?\)|"', '', line).strip()

  killed = killing.split(' - ')[0]
  if killed not in indices:
    indices[killed] = G.add_node(killed)

  killer = re.search(r' by(\s[A-Z][a-z]+)+', killing)
  if killer is None:
    G.add_edge(indices[killed], indices[killed])
  else:
    killer = killer.group().replace('by', '').strip()
    if killer not in indices:
      indices[killer] = G.add_node(killer)
    G.add_edge(indices[killed], indices[killer])

# writes GoT kills network to Pajek file

Graph.write(G)

# analyzes node centralities of GoT kills network

analysis(G)
