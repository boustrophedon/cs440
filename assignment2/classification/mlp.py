# mlp.py
# -------------

import numpy
from scipy.special import expit

from dataClassifier import TRAIN_PERCENTAGE

DATA_WIDTH=28
DATA_HEIGHT=28

LAYER1_WIDTH = 30
LAYER2_WIDTH = 10

LEARN_RATE = 0.1


class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = max_iterations

    # matrix that maps the inputs to a vector of outputs for each node
    # each of the LAYER1_WIDTH = H neurons has the number of weights as the size of the input,
    # that is, there is a link from the input to each output, each with a weight
    # which is DATA_WIDTH*DATA_HEIGHT = In
    # So our matrix multiplication is (H x In)(In x 1) = (H x 1)
    # The columns of the matrix are the links from a given input to every output,
    # and the rows are the links from every input to a given output
    # Since M . v is Row x column, this makes sense because we end up with a vector which has
    # each entry the dot product of the row in the matrix, i.e. the links from each input to a specific output
    # dot the input vector.
    self.layer1 = 0.01*numpy.random.randn(LAYER1_WIDTH, DATA_WIDTH*DATA_HEIGHT)
    self.layer1_bias = numpy.zeros(LAYER1_WIDTH)
    # for the output layer we have another set of weights, from a given input
    # (which is now the output of the activation function) to every output, which is our output layer
    # which is size 10 because there are ten classes.
    # So the matrix is (O x H)(H x 1) = (O x 1), where O = len(legalLabels) = 10

    # TODO: in the batch case, all the 1s turn into Ts where T is the number of test data
    # we don't really need to do that here but it is done in actual practice

    self.layer2 = 0.01*numpy.random.randn(len(self.legalLabels), LAYER1_WIDTH)
    self.layer2_bias = numpy.zeros(len(self.legalLabels))
    
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    in_vectorized = list()
    for datum in trainingData:
        x_in = numpy.empty(DATA_WIDTH*DATA_HEIGHT, dtype=int)
        for (x,y), v in datum.items():
            x_in[y*DATA_HEIGHT + x] = v
        in_vectorized.append(x_in)
        
    for iteration in range(self.max_iterations):
      print("Starting iteration ", iteration, "...")
      for i, x in enumerate(in_vectorized):
        if i > TRAIN_PERCENTAGE*len(in_vectorized):
          break

        y = numpy.zeros(len(self.legalLabels))
        y[trainingLabels[i]] = 1

        hidden = expit(numpy.dot(self.layer1, x) + self.layer1_bias)
        
        guess = expit(numpy.dot(self.layer2, hidden) + self.layer2_bias)

        error = (guess-y)

        dguess = (guess*(1-guess))*error

        # layer2 is (O x H), dguess is (O x 1), hidden is (H, 1), so we want dguess * hidden.T = (O x H)
        dlayer2 = numpy.outer(dguess, hidden.T)
        dbias2 = dguess
        
        # hidden is (H x 1), layer2 weights are (O x H), so we want layer2.T * (O x 1) => layer2.T * dguess
        dhidden = numpy.dot(self.layer2.T, dguess)
        # derivative of tanh again
        dhidden = dhidden*(hidden*(1-hidden))
        
        # layer1 = (H x I), dhidden is (H x 1) and input is (I x 1) so we do dhidden * x.T = (H x I)
        dlayer1 = numpy.outer(dhidden, x.T)
        dbias1 = dhidden

        self.layer2 -= LEARN_RATE*dlayer2
        self.layer2_bias -= LEARN_RATE*dbias2
        self.layer1 -= LEARN_RATE*dlayer1
        self.layer1_bias -= LEARN_RATE*dbias1

  def classify(self, data ):
    guesses = []
    for datum in data:
      x_in = numpy.empty(DATA_WIDTH*DATA_HEIGHT, dtype=int)
      for (x,y), v in datum.items():
          x_in[y*DATA_HEIGHT + x] = v

      hidden = numpy.tanh(numpy.dot(self.layer1, x_in) + self.layer1_bias)
      guess = numpy.tanh(numpy.dot(self.layer2, hidden) + self.layer2_bias)
      guesses.append(numpy.argmax(guess))
       
    return guesses
