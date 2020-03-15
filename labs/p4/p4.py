from Piv import *

"""
p4.1 - Personalized PageRank algorithm
"""

def PPR(G, root, alpha = 0.85):
  PPRs = [1 / G.get_n()] * G.get_n()

  nodes = G.get_nodes()
  for _ in range(100):
    nPPRs = [0] * G.get_n()
    
    shuffle(nodes)
    for i in nodes:
      for j in G.get_neighbours(i):
        nPPRs[i] += PPRs[j] * alpha / G.get_degree(j)

    nPPRs[root] += 1.0 - sum(nPPRs)
    PPRs = nPPRs

  return PPRs

def get_i(G, label):
  for i in G.get_nodes():
    if G.get_label(i) == label:
      return i

  return -1

G = Graph.read('imdb_actors')

print(G)

tops(G, lambda G: PPR(G, get_i(G, 'Hanks, Tom')), "Like 'Hanks, Tom'")
tops(G, lambda G: PPR(G, get_i(G, 'Marcus, Mr.')), "Like 'Marcus, Mr.'")
