# svm.py
# -------------

# svm implementation
from dataClassifier import TRAIN_PERCENTAGE

import util

import numpy
import sklearn

from sklearn import svm

PRINT = True

DATA_WIDTH=28
DATA_HEIGHT=28


class SVMClassifier:
  """
  svm classifier
  """
  def __init__( self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "svm"
    self.classifier = svm.LinearSVC()
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    in_vectorized = list()
    data_size = int(TRAIN_PERCENTAGE*len(trainingLabels))
    for i,datum in enumerate(trainingData):
      if i == data_size:
        break
      x_in = numpy.empty(DATA_WIDTH*DATA_HEIGHT, dtype=int)
      for (x,y), v in datum.items():
          x_in[y*DATA_HEIGHT + x] = v
      in_vectorized.append(x_in)
   
    labels = trainingLabels[:data_size]
    self.classifier.fit(in_vectorized, labels)
  def classify(self, data ):
    guesses = []
    for datum in data:
      x_in = numpy.empty(DATA_WIDTH*DATA_HEIGHT)
      for (x,y),v in datum.items():
          x_in[y*DATA_HEIGHT + x] = v
      guesses.append(self.classifier.predict([x_in]))
      
    return guesses

