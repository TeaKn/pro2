from Piii import *
from random import *
import operator as op
import requests

def DC(G):
  """
  Compute degree centrality of nodes in a graph represented by class Graph.
  Function returns a list of degree centralities of each node represented by its index.
  """
  DCs = [0] * G.get_n() # degree centralities
  
  for i in G.get_nodes():
    DCs[i] = G.get_degree(i) / (G.get_n() - 1)
  
  return DCs

def EC(G):
  """
  Compute eigenvector centrality of nodes in a graph represented by class Graph.
  Function returns a list of eigenvector centralities of each node represented by its index.
  """
  ECs = [1 / G.get_n()] * G.get_n() # eigenvector centralities
  
  for _ in range(100):
    nECs = [0] * G.get_n() # new/updated centralities
    
    for i in G.get_nodes():
      for j in G.get_neighbours(i):
        nECs[i] += ECs[j]
  
    sEC = sum(nECs)
    ECs = [ec / sEC for ec in nECs] # normalized centralities
    
  return ECs

def C(G, i):
  """
  Compute closeness centrality of given node in a graph represented by class Graph.
  Function returns the closeness centrality of given node represented by its index.
  """
  D = [0] * G.get_n() # node distances
  
  Q = [i] # queue of nodes
  while Q:
    i = Q.pop(0)
    
    for j in G.get_neighbours(i):
      if i != j and D[j] == 0:
        D[j] = D[i] + 1 # computing distances
        Q.append(j)

  return sum([1 / d if d > 0 else 0 for d in D]) / (G.get_n() - 1) # closeness centrality

def CC(G):
  """
  Compute closeness centrality of nodes in a graph represented by class Graph.
  Function returns a list of closeness centralities of each node represented by its index.
  """
  return [C(G, i) for i in G.get_nodes()] # closeness centralities

def PR(G, alpha = 0.85):
  """
  Compute PageRank score of nodes in a graph represented by class Graph.
  Function returns a list of PageRank scores of each node represented by its index.
  """
  PRs = [1 / G.get_n()] * G.get_n() # PageRank scores
  
  nodes = G.get_nodes()
  for _ in range(100):
    nPRs = [0] * G.get_n() # new/updated scores
    
    shuffle(nodes)
    for i in nodes:
      for j in G.get_neighbours(i):
        nPRs[i] += PRs[j] * alpha / G.get_degree(j)
  
    sPR = sum(nPRs)
    PRs = [pr + (1 - sPR) / G.get_n() for pr in nPRs] # normalized scores

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
  tops(G, lambda G: CC(G), 'Closenesses')
  tops(G, lambda G: PR(G), 'PageRanks')

# analyzes node centralities of different real networks

analysis(Graph.read('bottlenose_dolphins'))
analysis(Graph.read('lovro_subelj'))
analysis(Graph.read('imdb_actors'))

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
