from Cv import *
from math import *

"""
p5.1 - Clustering Slovenian cities
"""

def plot_cities(longs, lats, annots, sizes, colors, palette, file, k = None):
  fig = plt.figure()
  gca = plt.gca()
  
  plt.scatter(longs, lats, marker = 'o', s = [0.66 * sqrt(s) + 16 for s in sizes], c = colors, cmap = palette, edgecolors = [[0, 0, 0]])
  
  for annot in annots:
    plt.scatter(annots[annot][1], annots[annot][0], marker = '*', s = 200, c = [[0, 0, 0]])
    plt.annotate(annot, xy = annots[annot][::-1], xytext = (5, 5), textcoords = 'offset points', fontweight = 'bold', fontsize = 12)

  plt.title('Slovenian cities by ' + ('ZIP' if k is None else 'clusters') + ' (color)')
  plt.xlabel('City longitude')
  plt.ylabel('City latitude')

  fig.savefig(file + ('' if k is None else '_k' + str(k)) + '.png', bbox_inches = 'tight')

data = []
with open('cities.tab', 'r') as file:
  for i, line in enumerate(file):
    if i > 0:
      data.append([float(value) for j, value in enumerate(line.split('\t')) if j > 0])

longs = [instance[1] for instance in data]
lats = [instance[2] for instance in data]

views = [instance[3] for instance in data]
zips = [instance[0] for instance in data]

annots = {'Ljubljana': (46.056946, 14.505751), 'Maribor': (46.55472, 15.64667), 'Kranj': (46.23887, 14.35561), 'Koper': (45.54694, 13.72944), 'Novo mesto': (45.80397, 15.16886)}

plot_cities(longs, lats, annots, views, zips, 'Accent', 'cities')

norms = np.zeros((len(data[0]), 2))
for j in range(len(data[0])):
  d = [data[i][j] for i in range(len(data))]
  norms[j] = [np.mean(d), np.std(d)]

for i in range(len(data)):
  data[i] = [(data[i][j] - norms[j, 0]) / norms[j, 1] for j in range(len(data[i])) if j < 3]

for k in range(2, 9):
  plot_cities(longs, lats, annots, views, k_means(data, k)[0], 'Accent', 'cities', k)
