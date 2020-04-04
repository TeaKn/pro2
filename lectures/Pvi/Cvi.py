import os
from random import randint

from scipy.spatial import ConvexHull

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def normalize(data):
  """
  Compute standardized normalized data values of attributes of given data instances.
  Function returns data values holding distances from the mean in units of standard deviation.
  """
  normals = np.zeros((len(data[0]), 2))
  for j in range(len(data[0])):
    values = [data[i][j] for i in range(len(data))]
    normals[j] = [np.mean(values), np.std(values)]

  for i in range(len(data)):
    for j in range(len(data[i])):
      data[i][j] = (data[i][j] - normals[j, 0]) / normals[j, 1]

  return data

def k_means(data, k = 3, centroids = None, iters = 1):
  """
  Cluster data instances into to the specified number of clusters using k-means algorithm.
  Function returns cluster labels of data instances represented by instance indicies.
  """
  if centroids is None:
    centroids = np.array([data[randint(0, k - 1)] for _ in range(k)])
  else:
    k = len(centroids)

  clusters = [randint(0, k - 1) for _ in range(len(data))]
  clusters[:k] = range(k)

  for _ in range(iters):
    for i in range(len(data)):
      distance = np.linalg.norm(data[i] - centroids[clusters[i]])

      for c in range(len(centroids)):
        d = np.linalg.norm(data[i] - centroids[c])

        if d < distance:
          distance = d
          clusters[i] = c

    for c in range(len(centroids)):
      centroids[c] = np.average([data[i] for i, cluster in enumerate(clusters) if cluster == c], axis = 0)

  return clusters, centroids

def plot_cities(longitudes, latitudes, clusters, centroids, palette, label):
  """
  Plot longitudes and latitudes of cities as a scatter plot with the specified symbol colors.
  Method stores the scatter plot of cities with centroid annotations to a file in PDF format.
  """
  fig = plt.figure()
  gca = plt.gca()

  plt.scatter(longitudes, latitudes, marker = 'o', s = 32, c = clusters, cmap = palette, edgecolors = [[0, 0, 0]], zorder = 1)
  
  for c, centroid in enumerate(centroids):
    plt.scatter(centroid[0], centroid[1], marker = '*', s = 320, c = [[1, 1, 1]], edgecolors = [[0, 0, 0]], zorder = 2)
    
    points = np.array([[longitudes[i], latitudes[i]] for i in range(len(longitudes)) if clusters[i] == c])
    if len(points) > 1:
      hull = ConvexHull(points)
      plt.fill(points[hull.vertices, 0], points[hull.vertices, 1], color = [0.66, 0.66, 0.66, 0.5], zorder = 0)

  plt.axis('off')
  plt.close()
  
  fig.savefig(label + '.png', bbox_inches = 'tight')

# reads attribute names and data values of Slovenian cities

data = []
with open('cities.tab', 'r') as file:
  for i, line in enumerate(file):
    if i > 0:
      data.append([float(value) for value in line.split('\t')[2:4]])

# computes standardized normalized data values of Slovenian cities

data = normalize(data)

# stores longitudes and latitudes of Slovenian cities

longitudes = [values[0] for values in data]
latitudes = [values[1] for values in data]

# visualizes clusterings of cities during k-means algorithm

centroids = None
for i in range(24):
  clusters, centroids = k_means(data, 7, centroids)
  plot_cities(longitudes, latitudes, clusters, centroids, 'tab10', 'cities-' + str(i + 1))

os.system('ffmpeg -r 1 -i cities-%d.png -vf fps=24 cities.mp4')
