#!/usr/bin/python
# coding=utf8

from random import *
from datetime import *

import matplotlib.pyplot as plt
from sklearn import *
import scipy as spy
import numpy as np

def MAE(regressions, predictions):
  """
  Compute mean absolute error between true and predicted regression values.
  """
  errors = [abs(predictions[i] - regressions[i]) for i in range(len(regressions))]
  return sum(errors) / len(errors)

def MAPE(regressions, predictions):
  """
  Compute mean absolute percentage error between true and predicted regression values.
  """
  errors = [0.0 if regressions[i] == 0.0 else abs((predictions[i] - regressions[i]) / regressions[i]) for i in range(len(regressions))]
  return sum(errors) / len(errors)

def pearson(regressions, predictions):
  """
  Compute Pearson product moment correlation between true and predicted regression values.
  """
  return np.corrcoef(regressions, predictions)[0][1]

def spearman(regressions, predictions):
  """
  Compute Spearman rank correlation between true and predicted regression values.
  """
  return spy.stats.spearmanr(regressions, predictions)[0]

def normalize(instances):
  """
  Compute simple normalized values of the data values for the specified instances.
  Function returns data holding unit values between the minimum and maximum values.
  """
  extremes = []
  for j in range(len(instances[0])):
    values = [instances[i][j] for i in range(len(instances))]
    extremes.append([min(values), max(values)])
  data = [[0.0 for _ in range(len(extremes))] for _ in range(len(instances))]
  for i in range(len(data)):
    for j in range(len(data[i])):
      data[i][j] = (instances[i][j] - extremes[j][0]) / (extremes[j][1] - extremes[j][0])
  return data

# reads instance values of electricity consumption of Ljubljana from ARFF file

attributes = []
instances = None

with open('electricity.arff', 'r') as file:
  for line in file:
    line = line.strip()
    if line.startswith('@data'):
      instances = []
    elif line.startswith('@attribute'):
      attributes.append(line.split(' ')[1])
    elif instances is not None and '?' not in line:
      instances.append([float(value) if i > 0 else datetime.strptime(value, '"%m/%d/%y %H:%M"') for i, value in enumerate(line.split(','))])

# reformats timestamps of electricity consumption of Ljubljana

timestamps = [instance[0] for instance in instances]
for instance in instances:
  instance[0] = instance[0].timestamp()

# computes regression values of electricity consumption of Ljubljana

regressions = [[instance[-1]] for instance in instances]
for instance in instances:
  del instance[-1]

# computes simple normalized values of electricity consumption of Ljubljana

instances = normalize(instances)
regressions = np.ravel(normalize(regressions))

# initializes standard regression models and defines their print out labels

labels = ['Linear regression', 'K-nearest neighbors', 'Decision tree regression', 'Support vector machines', 'Multilayer perceptron']
regressors = [linear_model.LinearRegression(), neighbors.KNeighborsRegressor(), tree.DecisionTreeRegressor(max_depth = 20), svm.SVR(gamma = 'scale'), neural_network.MLPRegressor()]

# fits regression models to electricity consumption of Ljubljana and computes predictions

predictions = []
for regressor in regressors:
  regressor.fit(instances, regressions)
  predictions.append(regressor.predict(instances))

# prints out standard evaluation metrics of computed predictions of defined regressors

print("                     Regressor |    MAE     MAPE   Pearson  Spearman")
for i in range(len(regressors)):
  print("{0:>30s} |  {1:.5f}  {2:5.1f}%  {3:.5f}  {4:.5f}".format("'" + labels[i] + "'", MAE(regressions, predictions[i]), 100.0 * MAPE(regressions, predictions[i]), pearson(regressions, predictions[i]), spearman(regressions, predictions[i])))
print

# defines range of instances to plot and colors for different regression models

INSTANCES = slice(30 * 24, 44 * 24)

COLORS = [[0.13389146718702238, 0.29547805539345195, 0.5781426976058945], [0.07134831603372127, 0.4680494958692737, 0.2889992791677507], [0.1717625430485148, 0.9141905849673179, 6.327219474799861e-05], [0.7470131506359771, 0.12629159284822133, 0.3014562506242887], [0.26833139775716286, 0.14919522937399787, 0.6431708332470145]]

# plots predicted electricity consumption of Ljubljana for specified range of instances

fig = plt.figure(figsize = (20, 10))

for i, regressor in enumerate(regressors):
  plt.plot(timestamps[INSTANCES], predictions[i][INSTANCES], color = COLORS[i], alpha = 0.75, linewidth = 3, linestyle = '-', label = labels[i], zorder = 10 + i)

# plots electricity consumption, temperature and emissions of Ljubljana for specified range

plt.fill_between(timestamps[INSTANCES], regressions[INSTANCES], color = [0, 0, 0], alpha = 0.5, linewidth = 3, label = 'True electricity', zorder = 0)
plt.fill_between(timestamps[INSTANCES], [instance[6] for instance in instances[INSTANCES]], color = [0.9373, 0.6118, 0.3608], alpha = 0.5, linewidth = 3, label = 'Temperature', zorder = 1)
plt.fill_between(timestamps[INSTANCES], [instance[7] for instance in instances[INSTANCES]], color = [0.7882, 0.9020, 0.5294], alpha = 0.5, linewidth = 3, label = 'Emissions', zorder = 2)

# defines title, legend, and axes labels and ticks for plotted electricity consumption of Ljubljana

plt.title('Electricity consumption of Ljubljana', fontweight = 'bold', fontsize = 20)
plt.ylabel('Normalized instance values', fontweight = 'bold', fontsize = 18)
plt.xlabel('Date and time', fontweight = 'bold', fontsize = 18)
plt.legend(frameon = True, shadow = True, fontsize = 15)

plt.tick_params(labelsize = 15)
plt.ylim(0.0, 1.33)

# stores true and predicted electricity consumption of Ljubljana to PNG file

fig.savefig('electricity.png', bbox_inches = 'tight')
plt.close()
