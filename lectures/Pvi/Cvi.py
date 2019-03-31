#!/usr/bin/python
# coding=utf8

from math import *

import matplotlib.pyplot as plt
import numpy as np

def normalize_data(instances):
  """
  Compute standardized normalized values of the data values for the specified instances.
  Function returns data values holding distances from the mean in units of standard deviation.
  """
  normals = np.zeros((len(instances[0]), 2))
  for j in range(len(instances[0])):
    values = [instances[i][j] for i in range(len(instances))]
    normals[j] = [np.mean(values), np.std(values)]
  data = np.zeros((len(instances), len(normals)))
  for i in range(len(data)):
    for j in range(len(data[i])):
      data[i, j] = (instances[i][j] - normals[j, 0]) / normals[j, 1]
  return data

def k_means(data, centroids = None, k = 5, s = 1):
  """
  Compute the specified number of clusters of instances using k-means clustering algorithm.
  Function returns cluster labels of data instances represented by instance indicies.
  """
  if centroids is None:
    centroids = np.array([values for values in data[:k]])
  else:
    k = len(centroids)
  clusters = [-1 for _ in range(len(data))]
  for _ in range(s):
    for i in range(len(data)):
      minimum = float('inf')
      for cluster in range(len(centroids)):
        distance = np.linalg.norm(data[i] - centroids[cluster])
        if distance < minimum:
          minimum = distance
          clusters[i] = cluster
    for cluster in range(len(centroids)):
      centroids[cluster] = np.average([data[i] for i, c in enumerate(clusters) if c == cluster], axis = 0)
  return ([cluster + 1 for cluster in clusters], centroids)

def plot_cities(longitudes, latitudes, clusters, colors, palette, label):
  """
  Plot longitudes and latitudes of cities as a scatter plot with specified symbol colors.
  Method stores the scatter plot including cluster annotations to a file in PNG format.
  """
  fig = plt.figure()
  gca = plt.gca()
  plt.scatter(longitudes, latitudes, marker = 'o', s = 25, c = colors, cmap = palette)
  plt.colorbar(ticks = range(1, len(clusters) + 1))
  for i, cluster in enumerate(clusters):
    plt.scatter(clusters[cluster][0], clusters[cluster][1], marker = '*', s = 250, c = [[0, 0, 0]])
    plt.annotate(cluster, xy = clusters[cluster], xytext = (5, 5), textcoords = 'offset points', fontweight = 'bold', fontsize = 20)
  plt.title('Slovenian cities (' + str(len(clusters)) + ' clusters)', fontweight = 'bold')
  plt.xlabel('Normalized city longitude')
  plt.ylabel('Normalized city latitude')
  plt.xlim(-2.5, 2.5)
  plt.ylim(-2.5, 2.5)
  fig.savefig(label + '.png', bbox_inches = 'tight')
  plt.close()

# reads attribute names and instance values of Slovenian cities

attributes = None
instances = []

with open('cities.tab', 'r') as file:
  for i, line in enumerate(file):
    if i == 0:
      attributes = [attribute.strip() for attribute in line.split('\t')[1:4]]
    else:
      instances.append([float(value) for value in line.split('\t')[1:4]])

# computes standardized normalized values of Slovenian cities

data = normalize_data(instances)

# computes longitudes and latitudes of Slovenian cities

longitudes = [values[1] for values in data]
latitudes = [values[2] for values in data]

# computes clusterings of cities and plots cities with centroids

k = 9
centroids = None

for i in range(15):
  (clusters, centroids) = k_means(data, centroids, k)
  plot_cities(longitudes, latitudes, {str(i + 1): centroid[1:] for i, centroid in enumerate(centroids)}, clusters, 'Paired', 'cities_' + str(i + 1))
