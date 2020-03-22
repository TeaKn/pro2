from random import *
from math import sqrt

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def k_means(data, k = 3):
  """
  Cluster data instances into to the specified number of clusters using k-means algorithm.
  Function returns cluster labels of data instances represented by instance indicies.
  """
  data = np.array(data)
  clusters = [randint(0, k - 1) for _ in range(len(data))]
  centroids = np.array([instance for instance in data[:k]])

  for _ in range(1000):
    stopping = True

    for i in range(len(data)):
      distance = np.linalg.norm(data[i] - centroids[clusters[i]])

      for c in range(len(centroids)):
        d = np.linalg.norm(data[i] - centroids[c])

        if d < distance:
          distance = d
          clusters[i] = c
          stopping = False

    if stopping:
      break

    for c in range(len(centroids)):
      centroids[c] = np.average([data[i] for i, cluster in enumerate(clusters) if cluster == c], axis = 0)

  return ([cluster + 1 for cluster in clusters], centroids)

def plot_attacks(longs, lats, annots, sizes, colors, palette, file, k = None):
  """
  Plot longitudes and latitudes of attacks as a scatter plot using the specified symbol sizes and colors.
  Method stores the scatter plot of attacks with annotations to the specified file in PNG format.
  """
  fig = plt.figure()
  gca = plt.gca()
  
  plt.scatter(longs, lats, marker = 'o', s = [24 * sqrt(s) + 32 for s in sizes], c = colors, cmap = palette, edgecolors = [[0, 0, 0]])
  
  for annot in annots:
    plt.scatter(annots[annot][1], annots[annot][0], marker = '*', s = 200, c = [[0, 0, 0]])
    plt.annotate(annot, xy = annots[annot][::-1], xytext = (5, 5), textcoords = 'offset points', fontweight = 'bold', fontsize = 12)

  for i, v in enumerate([100, 10, 2]):
    plt.scatter(-5, 20 - 3.33 * i, marker = 'o', s = 24 * sqrt(v) + 32, c = [[1, 1, 1]], edgecolors = [[0, 0, 0]])
    plt.annotate(str(v) + ' victims', xy = (-5, 20 - 3.33 * i), xytext = (20, -5), textcoords = 'offset points')

  plt.title('Terrorism attacks ' + ('over time' if k is None else 'by clusters') + ' (color)')
  plt.xlabel('Attack longitude')
  plt.ylabel('Attack latitude')

  fig.savefig(file + ('' if k is None else '_k' + str(k)) + '.png', bbox_inches = 'tight')

def plot_clusters(centroids, names, palette, markers, label, k):
  """
  Plot cluster values of attacks as a horizontal histogram using the specified symbol markers and colors.
  Method stores the histogram of cluster values of attacks to the specified file in PNG format.
  """
  cmap = cm.get_cmap(palette)
  fig = plt.figure()
  gca = plt.gca()

  for i, centroid in enumerate(centroids):
    for j, value in enumerate(centroid):
      plt.plot([0, value], [len(centroid) - j - 1 + 0.1 * i] * 2, c = cmap(i / (len(centroids) - 1.0)), linewidth = 3, zorder = 0)
      plt.scatter(centroid, [value + 0.1 * i for value in range(len(centroid) - 1, -1, -1)], marker = markers[i], c = [cmap(i / (len(centroids) - 1))], s = 150, linewidth = 2, zorder = 1)

  m = min([min(c) for c in centroids])
  for i, centroid in enumerate(centroids):
    plt.scatter(m - 1.5, i * 0.4, marker = markers[i], c = [cmap(i / (len(centroids) - 1))], s = 150, linewidth = 2, zorder = 2)
    plt.annotate(str(i + 1) + ('st' if i == 0 else 'nd' if i == 1 else 'rd' if i == 2 else 'th') + ' cluster', xy = (m - 1.5, i * 0.4), xytext = (15, -5), textcoords = 'offset points', zorder = 2)

  plt.plot([0, 0], [-1, len(names)], c = [0, 0, 0])

  plt.title('Terrorism attacks by clusters (colors)')
  plt.yticks(list(range(len(names))), [name.title() for name in names[:][::-1]])
  plt.xlabel('Normalized cluster value')

  plt.xlim(m - 2, max([max(c) for c in centroids]) + 2)
  plt.ylim(-0.5, len(names) - 0.5)

  fig.savefig(label + '_c' + str(k) + '.png', bbox_inches = 'tight')
