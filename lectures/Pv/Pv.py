#!/usr/bin/python
# coding=utf8

import os

from Piv import *
from time import *
from random import *

import matplotlib.image as im
import matplotlib.pyplot as plt
import numpy as np

def read_image(name, path = '.'):
  """
  Read a bitmap image from the specified file in PNG format.
  Function returns an array of arrays storing RGB values for each pixel.
  """
  return im.imread(os.path.join(path, name + '.png'))

def save_image(img, name, path = '.'):
  """
  Write a bitmap image to the specified file in PNG format.
  Method also creates the specified folder if does not exist.
  """
  if not os.path.exists(path):
    os.makedirs(path)
  fig = plt.figure()
  plt.imshow(img)
  fig.savefig(os.path.join(path, name + '.png'), bbox_inches = 'tight')

def get_grayscale(img):
  """
  Creates a grayscale bitmap image from the given color bitmap image.
  Function returns an array of arrays storing RGB values for each pixel.
  """
  gs = np.ones(img.shape)
  (h, w) = gs.shape[:2]
  for i in range(h):
    for j in range(w):
      gs[i][j][:3] = sum(img[i][j][:3]) / 3
  return gs

def get_graph(img, name, thres = 0.05):
  """
  Creates a graph from a bitmap image with pixels as nodes linked according to the specified threshold.
  Function returns an undirected graph represented by class Graph.
  """
  G = Graph(name)
  (h, w) = img.shape[:2]
  for i in range(h):
    for j in range(w):
      G.add_node()
  for i in range(h):
    for j in range(w):
      if j + 1 < w and np.linalg.norm(img[i][j] - img[i][j + 1]) < thres:
        G.add_edge(i * w + j, i * w + j + 1)
      if i + 1 < h and np.linalg.norm(img[i][j] - img[i + 1][j]) < thres:
        G.add_edge(i * w + j, (i + 1) * w + j)
      if j + 1 < w and i + 1 < h and np.linalg.norm(img[i][j] - img[i + 1][j + 1]) < thres:
        G.add_edge(i * w + j, (i + 1) * w + j + 1)
      if j - 1 >= 0 and i + 1 < h and np.linalg.norm(img[i][j] - img[i + 1][j - 1]) < thres:
        G.add_edge(i * w + j, (i + 1) * w + j - 1)
  return G

def get_segments(G, C, shape, thres = 0.0005):
  """
  Creates a bitmap image from the specified undirected graph and node clusters.
  Function returns a segmented image with pixels from a cluster being assigned the same color.
  """
  seg = np.ones(shape)
  for c in C:
    clr = [random(), random(), random()] if len(c) > thres * G.get_n() else [1, 1, 1]
    for i in c:
      seg[i / shape[1]][i % shape[1]][:3] = clr
  return seg

def get_inverted(img):
  """
  Creates an inverted bitmap image from the specified color bitmap image.
  Function returns a grayscale image with white (non-white) pixels being assigned black (white) color.
  """
  inv = np.ones(img.shape)
  (h, w) = inv.shape[:2]
  for i in range(h):
    for j in range(w):
      if np.prod(img[i][j]) == 1:
        inv[i][j] = [0, 0, 0, 1]
  return inv

# creates segmented and inverted images for various real images

start = time()

for name in os.listdir('figs'):
  if name.endswith('.png'):
    name = name.split('.')[0]
    
    # reads image from a given file
  
    img = read_image(name, 'figs')
    save_image(img, name + '_img', 'imgs')
    
    # creates grayscale image from color image
    
    gs = get_grayscale(img)
    save_image(gs, name + '_gs', 'imgs')
    
    # creates an undirected graph from color image

    G = get_graph(img, name, 0.033)
    
    # creates segmented image from graph components

    cc = get_segments(G, Graph.components(G), img.shape)
    save_image(cc, name + '_cc', 'ccs')

    # creates inverted image from segmented image

    icc = get_inverted(cc)
    save_image(icc, name + '_icc', 'ccs')
    
    # prints out standard graph information
    
    Graph.write(G, 'ccs')
    print(G)
    
    # creates an undirected graph from color image
    
    G = get_graph(img, name, 0.1)
    
    # creates segmented image from graph communities

    cd = get_segments(G, clusters(LP(G)), img.shape)
    save_image(cd, name + '_cd', 'cds')
    
    # creates inverted image from segmented image

    icd = get_inverted(cd)
    save_image(icd, name + '_icd', 'cds')
    
    # prints out standard graph information

    Graph.write(G, 'cds')
    print(G)

print("{0:>12s} | {1:.1f} sec\n".format('Time', time() - start))
