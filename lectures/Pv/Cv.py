#!/usr/bin/python
# coding=utf8

from random import *

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def k_means(data, k = 3):
  """
  Compute the specified number of clusters of instances using k-means clustering algorithm.
  Function returns cluster labels of data instances represented by instance indicies.
  """
  centroids = np.array([values for values in data[:k]])
  clusters = [-1 for _ in range(len(data))]
  for _ in range(1000):
    stopping = True
    for i in range(len(data)):
      minimum = float('inf')
      for cluster in range(len(centroids)):
        distance = np.linalg.norm(data[i] - centroids[cluster])
        if distance < minimum:
          minimum = distance
          if clusters[i] != cluster:
            stopping = False
          clusters[i] = cluster
    if stopping:
      break
    for cluster in range(len(centroids)):
      centroids[cluster] = np.average([data[i] for i, c in enumerate(clusters) if c == cluster], axis = 0)
  return ([cluster + 1 for cluster in clusters], centroids)

def plot_events(longitudes, latitudes, annotations, victims, sizes, colors, palette, label, k = None):
  """
  Plot longitudes and latitudes of events as a scatter plot with specified symbol sizes and colors.
  Method stores the scatter plot including annotations and a legend to a file in PNG format.
  """
  fig = plt.figure()
  gca = plt.gca()
  plt.scatter(longitudes, latitudes, marker = 'o', s = [s + 50 for s in sizes], c = colors, cmap = palette)
  plt.colorbar(ticks = (None if k is None else range(1, k + 1)))
  for annotation in annotations:
    plt.scatter(annotations[annotation][1], annotations[annotation][0], marker = '*', s = 200, c = [0, 0, 0])
    plt.annotate(annotation, xy = annotations[annotation][::-1], xytext = (5, 5), textcoords = 'offset points')
  for i, victim in enumerate(victims):
    plt.scatter(-5, 20 - 3.33 * i, marker = 'o', s = victim + 50, c = [1, 1, 1])
    plt.annotate(str(victim) + ' victims', xy = (-5, 20 - 3.33 * i), xytext = (20, -5), textcoords = 'offset points')
  plt.title('Terrorism attacks (' + ('date' if k is None else str(k) + ' clusters') + ')', fontweight = 'bold')
  plt.xlabel('Attack longitude')
  plt.ylabel('Attack latitude')
  fig.savefig(label + ('' if k is None else '_k' + str(k)) + '.png', bbox_inches = 'tight')

def plot_clusters(centroids, attributes, palette, markers, label, k):
  """
  Plot cluster centriods as a horizontal histogram with specified symbol markers and colors.
  Method stores the histogram including a legend to a file in PNG format.
  """
  fig = plt.figure()
  gca = plt.gca()
  cmap = cm.get_cmap(palette)
  for i, centroid in enumerate(centroids):
    for j, value in enumerate(centroid):
      plt.plot([0, value], [len(centroid) - j - 1 + 0.1 * i, len(centroid) - j - 1 + 0.1 * i], c = cmap(i / (len(centroids) - 1.0)), linewidth = 3, zorder = 0)
  m = min([min(centroid) for centroid in centroids])
  for i, centroid in enumerate(centroids):
    plt.scatter(centroid, [value + 0.1 * i for value in list(range(len(centroid)))[::-1]], marker = markers[i], c = cmap(i / (len(centroids) - 1.0)), s = 200, linewidth = 2, zorder = 1)
    plt.scatter(m - 1.5, i * 0.4, marker = markers[i], c = cmap(i / (len(centroids) - 1.0)), s = 200, linewidth = 2, zorder = 2)
    plt.annotate(str(i + 1) + ('st' if i == 0 else 'nd' if i == 1 else 'rd' if i == 2 else 'th') + ' cluster', xy = (m - 1.5, i * 0.4), xytext = (20, -5), textcoords = 'offset points', zorder = 2)
  plt.plot([0, 0], [-1, len(attributes) - 1], c = [0, 0, 0])
  plt.title('Terrorism attacks (' + str(k) + ' centroids' + ')', fontweight = 'bold')
  plt.xlabel('Normalized centroid value')
  plt.yticks(list(range(len(attributes) - 1)), [attribute.title() for attribute in attributes[1:][::-1]])
  plt.xlim(m - 2, max([max(centroid) for centroid in centroids]) + 1.5)
  plt.ylim(-0.5, len(attributes) - 1.5 + 0.1 * len(centroids))
  fig.savefig(label + '_c' + str(k) + '.png', bbox_inches = 'tight')

# reads attribute names and instance values of terrorism attacks

attributes = None
instances = []

with open('terrorism.tab', 'r') as file:
  for i, line in enumerate(file):
    if i == 0:
      attributes = [attribute.strip() for attribute in line.split('\t')]
    else:
      label = line[:line.find('\t')]
      instances.append([label] + [float(value) for value in line.split('\t')[1:]])

# computes longitudes and latitudes of terrorism attacks

longitudes = [instance[3] for instance in instances]
latitudes = [instance[2] for instance in instances]

# defines sizes and colors of symbols representing terrorism attacks

sizes = [instance[4] + instance[5] for instance in instances]
colors = [instance[1] for instance in instances]

# defines annotations for terrorism attacks as selected longitudes and latitudes

annotations = {'Madrid': (40.416775, -3.703790), 'Paris': (48.864716, 2.349014), 'Berlin': (52.520008, 13.404954), 'Ljubljana': (46.056946, 14.505751), 'Athens': (37.983810, 23.727539), 'Jerusalem': (31.771959, 35.217018)}

# plots terrorism attacks showing their location, date of attack and number of victims

plot_events(longitudes, latitudes, annotations, [250, 100, 10], sizes, colors, 'Greens', 'terrorism')

# computes normalizations of attribute values representing terrorism attacks

normals = np.zeros((len(instances[0]) - 1, 2))
for j in range(1, len(instances[0])):
  values = [instances[i][j] for i in range(len(instances))]
  normals[j - 1] = [np.mean(values), np.std(values)]

# computes standard normalized instance values of terrorism attacks

data = np.zeros((len(instances), len(normals)))
for i in range(len(data)):
  for j in range(len(data[i])):
    data[i, j] = (instances[i][j + 1] - normals[j, 0]) / normals[j, 1]
# data = [instance[1:3] for instance in data]

# computes clusterings of terrorism attacks and plots events and cluster centroids

for k in range(2, 7):
  (clusters, centroids) = k_means(data, k)
  plot_events(longitudes, latitudes, annotations, [250, 100, 10], sizes, clusters, 'Paired', 'terrorism', k)
  plot_clusters(centroids, attributes, 'Paired', ['o', 's', '^', 'v', '<', '>'], 'terrorism', k)
