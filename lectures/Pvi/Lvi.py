import datetime

import numpy as np
import matplotlib.pyplot as plt

from sklearn import *

def accuracy(classes, predicts):
  """
  Compute accuracy of predicted classes relative to given true classes.
  """
  count = 0
  for i in range(len(classes)):
    if classes[i] == predicts[i]:
      count += 1
  return count / len(classes)

def MAPE(values, predicts):
  """
  Compute mean absolute percentage error between predicted and true values.
  """
  error = 0
  for i in range(len(values)):
    if values[i] != 0:
      error += abs(predicts[i] / values[i] - 1)
  return error / len(values)

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

# reads handwritten digits data from sklearn library repository

data = datasets.load_digits()

# plots first 96 handwritten digits and stores image to PDF file

fig = plt.figure()

for i in range(192):
  plt.subplot(8, 24, i + 1)

  plt.imshow(data.images[i], cmap = 'binary')
  plt.title(data.target[i], fontsize = 8)
  plt.axis('off')

plt.close()

fig.savefig('digits.pdf', bbox_inches = 'tight')

# initializes standard classification models in sklearn library

classifiers = {"kNN": neighbors.KNeighborsClassifier(), "Tree": tree.DecisionTreeClassifier(max_depth = 10), "Forest": ensemble.RandomForestClassifier(max_depth = 20, n_estimators = 50), "SVM": svm.SVC(gamma = 0.001), "MLP": neural_network.MLPClassifier()}

# defines instance values and true classes of handwritten digits

instances = data.data
classes = data.target

# computes accuracy of classifiers using K-fold cross validation

K = 5

accuracies = {}
for name, classifier in classifiers.items():
  accuracies[name] = 0

  for k in range(K):
    train_instances = [instance for i, instance in enumerate(instances) if i % K != k]
    train_classes = [clas for i, clas in enumerate(classes) if i % K != k]

    classifier.fit(train_instances, train_classes)

    test_instances = [instance for i, instance in enumerate(instances) if i % K == k]
    test_classes = [clas for i, clas in enumerate(classes) if i % K == k]

    test_predicts = classifier.predict(test_instances)

    accuracies[name] += accuracy(test_classes, test_predicts) / K

# prints out accuracy of classifiers for handwritten digits data

print("\n  Classifier | Accuracy")
for classifier in classifiers:
  print("{0:>12s} |  {1:5.2f}%".format("'" + classifier + "'", 100 * accuracies[classifier]))
print()

# reads electricity consumption of Ljubljana data from ARFF file

data = None
with open('electricity.arff', 'r') as file:
  for line in file:
    if line.startswith('@data'):
      data = []
    elif data is not None and '?' not in line:
      data.append([float(value) if i > 0 else datetime.datetime.strptime(value, '"%m/%d/%y %H:%M"').timestamp() for i, value in enumerate(line.split(',')) if i != 7])

# plots first weeks of electricity consumption and stores image to PDF file

dates = [datetime.datetime.fromtimestamp(instance[0]) for instance in data[:14 * 24]]
elecs = [instance[-1] for instance in data[:14 * 24]]

fig = plt.figure()

plt.fill_between(dates, elecs, color = [0, 0, 0], alpha = 0.33)

plt.xlim(dates[0], dates[-1])
plt.xticks([datetime.datetime.fromtimestamp(((4 - i) * dates[0].timestamp() + i * dates[-1].timestamp()) // 4) for i in range(5)])
plt.ylim(0, 1.2 * max(elecs))

plt.title("Ljubljana electricity consumption", fontweight = 'bold')
plt.xlabel("Date and time")
plt.ylabel("Electricity")

plt.close()

fig.savefig('electricity.pdf', bbox_inches = 'tight')

# defines data instances and true values of electricity consumption

instances = [instance[:-1] for instance in data]
instances = normalize(instances)

values = [instance[-1] for instance in data]

# initializes standard regression models in sklearn library

regressors = {"LR": linear_model.LinearRegression(), "SGD": linear_model.SGDRegressor(), "kNN": neighbors.KNeighborsRegressor(), "Tree": tree.DecisionTreeRegressor(), "SVM": svm.SVR(gamma = 'scale')}

# computes MAPE of regressors using K-fold temporal validation

FOLD = 7 * 24

MAPEs = {}
for name, regressor in regressors.items():
  MAPEs[name] = 0

  for k in range(1, K + 1):
    train_instances = instances[:-K * FOLD]
    train_values = values[:-K * FOLD]

    regressor.fit(train_instances, train_values)
    
    test_instances = instances[-K * FOLD:-(K - 1) * FOLD]
    test_values = values[-K * FOLD:-(K - 1) * FOLD]

    test_predicts = regressor.predict(test_instances)

    MAPEs[name] += MAPE(test_values, test_predicts) / K

# prints out MAPE of regressors for Ljubljana electricity consumption

print("   Regressor |  MAPE")
for regressor in regressors:
  print("{0:>12s} | {1:5.2f}%".format("'" + regressor + "'", 100 * MAPEs[regressor]))
print()
