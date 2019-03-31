#!/usr/bin/python
# coding=utf8

import matplotlib.pyplot as plt
from sklearn import *

def accuracy(classes, predictions):
  """
  Compute accuracy of predicted class values compared to true class values.
  """
  accuracy = 0
  for i in range(len(classes)):
    if classes[i] == predictions[i]:
      accuracy += 1.0 / len(classes)
  return accuracy

# reads handwritten digits data from scikit-learn datasets repository

data = datasets.load_digits()

# plots first 72 handwritten digits as images and stores plot to PNG file

fig = plt.figure(figsize = (16, 12))

for i in range(72):
  plt.subplot(6, 12, i + 1)
  plt.imshow(data.images[i], cmap = 'Greens')
  plt.title(data.target[i], fontsize = 24, fontweight = 'bold')
  plt.axis('off')

fig.savefig('digits.png', bbox_inches = 'tight')
plt.close()

# initializes standard classification models and defines their print out labels

labels = ['K-nearest neighbors', 'Decision tree classification', 'Random forest classification', 'Support vector machines', 'Multilayer perceptron']
classifiers = [neighbors.KNeighborsClassifier(), tree.DecisionTreeClassifier(max_depth = 10), ensemble.RandomForestClassifier(max_depth = 20, n_estimators = 50), svm.SVC(gamma = 0.001), neural_network.MLPClassifier()]

# defines instance values and true classes of handwritten digits data

instances = data.images.reshape((len(data.images), -1))
classes = data.target

# evaluates accuracy of predictions of classifiers using 10-fold cross validation

accuracies = []
for i, classifier in enumerate(classifiers):
  accuracies.append(0.0)
  for j in range(10):
    train_instances = [instance for k, instance in enumerate(instances) if k % 10 != j]
    train_classes = [clas for k, clas in enumerate(classes) if k % 10 != j]
    classifier.fit(train_instances, train_classes)
    
    test_instances = [instance for k, instance in enumerate(instances) if k % 10 == j]
    test_classes = [clas for k, clas in enumerate(classes) if k % 10 == j]
    accuracies[i] += accuracy(test_classes, classifier.predict(test_instances)) / 10
  
# prints out average classification accuracy of defined classifiers
  
print("                    Classifier | Accuracy")
for i in range(len(classifiers)):
  print("{0:>30s} |  {1:5.2f}%".format("'" + labels[i] + "'", 100.0 * accuracies[i]))
