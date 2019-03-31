#!/usr/bin/python
# coding=utf8

from math import *

import numpy as np
import matplotlib.pyplot as plt

def regression(x, y):
    (n, mx, my) = (len(x), np.mean(x), np.mean(y))
    k = (np.sum(x * y) - n * my * mx) / (np.sum(x * x) - n * mx * mx)
    return (my - k * mx, k)

labels = np.array([])
views = np.array([])
victims = np.array([])

with open('terrorism.tab', 'r') as file:
  for i, line in enumerate(file):
    if i > 0:
      values = line.split('\t')
      views = np.append(views, log(float(values[6])))
      victims = np.append(victims, float(values[4]) + float(values[5]))

regs = regression(views, victims)

fig = plt.figure()
gca = plt.gca()

xs = [exp(v) for v in views]

for i, x in enumerate(xs):
  plt.plot([x, x], [regs[0] + regs[1] * log(x), victims[i]], color = [0.9647, 0.4863, 0.1216] if regs[0] + regs[1] * log(x) < victims[i] else [0.0667, 0.4118, 0.4510], zorder = 0)

plt.plot(xs, regs[0] + regs[1] * views, color = 'k', linewidth = 3, zorder = 1)

plt.scatter(xs, victims, marker = '*', s = 75, c = [0, 0, 0], zorder = 2)

plt.title('Terrorism attacks', fontweight = 'bold')
plt.xlabel('Attack Wikipedia views')
plt.ylabel('Attack deads and injuries')

gca.set_xscale('log')

plt.show()

fig.savefig('terrorism.png', bbox_inches = 'tight')
