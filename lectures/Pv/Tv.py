#!/usr/bin/python
# coding=utf8

import re
import operator as op

def edit_distance(fst, snd):
  """
  Compute the Levenshtein or edit distance between the given two strings.
  Function returns the number of operations needed to traverse one string to another.
  """
  d = [[0 for _ in range(len(snd) + 1)] for _ in range(len(fst) + 1)]
  for i in range(len(fst) + 1):
    d[i][0] = i
  for j in range(len(snd) + 1):
    d[0][j] = j
  for j in range(1, len(snd) + 1):
    for i in range(1, len(fst) + 1):
      if fst[i - 1] == snd[j - 1]:
        d[i][j] = d[i - 1][j - 1]
      else:
        d[i][j] = min(d[i - 1][j - 1], d[i - 1][j], d[i][j - 1]) + 1
  return d[len(fst)][len(snd)]

# creates a list of names of GoT characters in GoT kills network

characters = []
with open('got_kills.net', 'r') as file:
  for line in file:
    if re.match(r'^\*vertices', line):
      continue
    elif re.match(r'^\*edges', line):
      break
    else:
      characters.append(re.split('"', line)[1])

# prints out most similar GoT character names due to edit distance

for character in characters:
  distances = {}
  for other in characters:
    if character != other:
      distances[other] = edit_distance(character, other)
  if min(distances.values()) <= 5:
    print("{0:>30s} | {1:s}".format('GoT character', 'Distance'))
    print("{0:>30s} | {1:d}".format("'" + character + "'", 0))
    for i, (character, distance) in enumerate(sorted(distances.items(), key = op.itemgetter(1))):
      if i < 5:
        print("{0:>30s} | {1:d}".format("'" + character + "'", distance))
    print
