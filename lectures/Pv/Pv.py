import os

from Piv import *
from time import *
from random import *

import numpy as np
import matplotlib.image as im
import matplotlib.pyplot as plt

def read_image(name, path = '.'):
  """
  Read a bitmap image from the specified file in PNG format.
  Function returns an array of arrays storing RGB values for each pixel.
  """
  return im.imread(os.path.join(path, name + '.png'))

def save_image(img, name, path = '.'):
  """
  Write the specified bitmap image to file in PNG format.
  Method also creates the specified folder if does not exist.
  """
  if not os.path.exists(path):
    os.makedirs(path)
  
  fig = plt.figure()
  plt.axis('off')

  plt.imshow(img)

  fig.savefig(os.path.join(path, name + '.png'), bbox_inches = 'tight')
  plt.close(fig)

def get_grayscale(img):
  """
  Creates a grayscale bitmap image from the specified color bitmap image.
  Function returns an array of arrays storing RGB values for each pixel.
  """
  (h, w) = img.shape[:2]
  
  gs = np.ones(img.shape)
  for i in range(h):
    for j in range(w):
      gs[i][j][:3] = sum(img[i][j][:3]) / 3

  return gs

def get_inverted(img):
  """
  Creates an inverted bitmap image from the specified color bitmap image.
  Function returns a black & white image with non-white pixels of color image
  being assigned white color and white pixels being assigned black color.
  """
  (h, w) = img.shape[:2]
  
  inv = np.ones(img.shape)
  for i in range(h):
    for j in range(w):
      if np.prod(img[i][j]) == 1:
        inv[i][j] = [0, 0, 0, 1]

  return inv

def get_corrected(img):
  """
  Creates a corrected bitmap image from the specified black & white bitmap image.
  Function returns a copy of black & white image, but with black pixels
  surrounded by only black pixels being assigned white color.
  """
  (h, w) = img.shape[:2]
  
  corr = np.copy(img)
  for i in range(1, h - 1):
    for j in range(1, w - 1):
      if np.sum(img[i - 1:i + 2, j - 1:j + 2, :3]) == 0:
        corr[i][j] = [1, 1, 1, 1]

  return corr

def get_graph(img, name = 'graph', thres = 0.033):
  """
  Creates a graph from the specified bitmap image with pixels as nodes,
  where adjacent pixels are linked if they are more similar than the treshold.
  Function returns an undirected graph represented by class Graph.
  """
  (h, w) = img.shape[:2]
  
  G = Graph(name)
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

def get_segments(G, CCs, shape, thres = 0.0005):
  """
  Creates a bitmap image from the specified undirected graph and its connected components.
  Function returns a segmented image with pixels from a component being assigned the same color.
  """
  (h, w) = img.shape[:2]
  
  seg = np.ones(shape)
  for CC in CCs:
    clr = [random(), random(), random()] if len(CC) > thres * G.get_n() else [1, 1, 1]
    for i in CC:
      seg[i // w][i % w][:3] = clr

  return seg

# creates coloring images from inverted segmented real images

start = time()

for name in os.listdir('figs'):
  if name.endswith('.png'):
    name = name.split('.')[0]

    # reads image from a given file and saves it

    img = read_image(name, 'figs')
    save_image(img, name + '_img')

    # creates grayscale image from color image and saves it

    gs = get_grayscale(img)
    save_image(gs, name + '_gs')

    # creates an undirected graph from color image and saves it

    G = get_graph(img, name)
    Graph.write(G)
    print(G)

    # creates segmented image of graph connected components and saves it

    seg = get_segments(G, Graph.components(G), img.shape)
    save_image(seg, name + '_seg')

    # creates inverted image from segmented image and saves it

    inv = get_inverted(seg)
    save_image(inv, name + '_inv')
    
    # corrects black patches of inverted image and saves it

    corr = get_corrected(inv)
    save_image(corr, name + '_corr')

    # creates coloring image of real color image and saves it

    (h, w) = img.shape[:2]
    color = np.concatenate([img, np.ones([h, w // 20, 4]), corr], axis = 1)
    save_image(color, name, 'outs')

print("{0:>12s} | {1:.1f} sec\n".format('Time', time() - start))
