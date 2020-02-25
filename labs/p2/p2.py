from Pii import *
from math import *
import operator as op
import requests
import re
import os

"""
p2.1 - Writing and reading graphs
"""

def write(G, path = '.'):
  (name, A, L) = G
  with open(os.path.join(path, name + '.adj'), 'w') as file:
    for i in range(len(A)):
      file.write('"{0:s}"'.format(L[i] if L is not None and L[i] is not None else ''))
      for j in A[i]:
        file.write(',{0:d}'.format(j))
      file.write('\n')
  return G

def read(name, path = '.'):
  A = []
  L = None
  with open(os.path.join(path, name + '.adj'), 'r') as file:
    for line in file:
      A.append([])
      if L is not None:
        L.append(None)
      adj = re.split(r',', line.rstrip())
      if re.match(r'"\w+"', adj[0]):
        if L is None:
          L = [None] * len(A)
        L[len(L) - 1] = adj[0][1:-1]
      for j in range(1, len(adj)):
        A[len(A) - 1].append(int(adj[j]))
  return (name, A, L)

G = ('demo', [[1], [0, 2, 2], [1, 1], []], ['foo', 'bar', 'baz', None])
assert(write(G) == read(G[0]))
G = gnp(1000, 0.1)
assert(write(G) == read(G[0]))

"""
p2.2 - Summarizing famous novels
"""

def freqs(name, path = '.'):
  terms = {}
  with open(os.path.join(path, name + '.txt'), 'r') as file:
    for line in file:
      for term in re.split(r'\W+', line.lower()):
        if len(term) == 0:
          continue
        if term not in terms:
          terms[term] = 0
        terms[term] += 1
  return terms

def tf(doc):
  tfs = {}
  mtf = max(doc[1].values())
  for term in doc[1]:
    tfs[term] = 0.5 + 0.5 * doc[1][term] / mtf
  return tfs

def idf(docs):
  terms = set()
  for doc in docs:
    terms.update(doc[1].keys())
  idfs = {}
  for term in terms:
    idfs[term] = log(len(docs) / len([0 for doc in docs if term in doc[1]]))
  return idfs

def tfidf(doc, docs):
  tfs = tf(doc)
  idfs = idf(docs)
  tfidfs = {}
  for term in tfs:
    tfidfs[term] = tfs[term] * idfs[term]
  return tfidfs

def doc(name):
  return (name, freqs(name))

docs = [doc("adventures_of_huckleberry_finn"), doc("alice's_adventures_in_wonderland"), doc("dracula"), doc("frankenstein"), doc("grimms'_fairy_tales"), doc("iliad"), doc("metamorphosis"), doc("moby_dick"), doc("peter_pan"), doc("war_and_peace")]

for doc in docs:
  print("{0:>12s} | '{1:s}'".format('Novel', doc[0]))
  for term in [term for i, term in enumerate(reversed(sorted(tfidf(doc, docs).items(), key = op.itemgetter(1)))) if i < 10]:
    print("{0:>12.4f} | '{1:s}'".format(term[1], term[0]))
  print()

"""
p2.3 - Game of Thrones characters
"""

chars = [re.sub(r'<.*?>', '', re.sub(r'<sup>\d</sup>', '', char)) for char in re.findall(r'<td><a href="/wiki/.+" title=".+">.+</a>.*</td>', re.split(r'<span class="mw-headline" id="Recurring_/_Guest_cast">Recurring / Guest cast</span>', requests.get('https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_characters').text)[0])]

print("{0:>30s} | {1:s}".format('Character', 'Actor/Actress'))
for i in range(0, len(chars), 2):
  print("{0:>30s} | {1:s}".format("'" + chars[i + 1] + "'", "'" + chars[i] + "'"))
print()

"""
p2.4 - Movies and OMDb API
"""

OMBD_KEY = 'cd9ba7d7'

def omdb(tit):
  movie = requests.get('http://www.omdbapi.com/?t=' + re.sub(r'\s', '+', tit) + '&apikey=' + OMBD_KEY).json()
  print("{0:>12s} | '{1:s}' ({2:d})".format('Title', movie['Title'], int(movie['Year'])))
  print("{0:>12s} | '{1:s}'".format('Genre', movie['Genre']))
  print("{0:>12s} | {1:.1f} ({2:,d} votes)".format('IMDb', float(movie['imdbRating']), int(movie['imdbVotes'].replace(',', ''))))
  print("{0:>12s} | '{1:s}'".format('Language', movie['Language']))
  print("{0:>12s} | '{1:s}'".format('Country', movie['Country']))
  print("{0:>12s} | {1:s}\n".format('Runtime', movie['Runtime']))

omdb('Bohemian Rhapsody')
omdb('Guardians of the Galaxy')
omdb('The Godfather')
