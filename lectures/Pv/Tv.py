import operator as op

def edit_distance(fst, snd):
  """
  Compute the Levenshtein or edit distance between the given two strings.
  Function returns number of operations needed to traverse one string to another.
  """
  distances = [[0 for _ in range(len(snd) + 1)] for _ in range(len(fst) + 1)]
  
  for i in range(len(fst) + 1):
    distances[i][0] = i
  for j in range(len(snd) + 1):
    distances[0][j] = j

  for j in range(1, len(snd) + 1):
    for i in range(1, len(fst) + 1):
      if fst[i - 1] == snd[j - 1]:
        distances[i][j] = distances[i - 1][j - 1]
      else:
        distances[i][j] = min(distances[i - 1][j - 1], distances[i - 1][j], distances[i][j - 1]) + 1

  return distances[len(fst)][len(snd)]

# creates a list of names of characters in GoT kills network

characters = []
with open('got_kills.net', 'r') as file:
  for line in file:
    if line.startswith('*vertices'):
      continue
    elif line.startswith('*edges'):
      break
    else:
      characters.append(line.split('"')[1].split(' - ')[0].strip())
      
characters.sort()

# prints out most similar GoT character names due to edit distance

for character in characters:
  print("{0:>30s} | # | {1:s}".format("GoT character", "Like '" + character + "'"))
  
  distances = {}
  for other in characters:
    if character != other:
      distances[other] = edit_distance(character, other)

  for i, (other, distance) in enumerate(sorted(distances.items(), key = op.itemgetter(1))):
    if i < 8:
      print("{0:>30s} | {1:d} | {2:4.1f}% ({3:d})".format("'" + other + "'", i + 1, 100 - 100 * distance / max(len(character), len(other)), distance))
  print()
