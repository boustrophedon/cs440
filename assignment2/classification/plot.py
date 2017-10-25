import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def read_data(fname):
  lines = list()
  with open(fname, "r") as f:
    lines = [line.strip() for line in f.readlines()]

  name = str()
  x = list()
  y = list()

  lines = [line.split(",") for line in lines]

  name = lines[0][0]

  x = [int(line[1]) for line in lines]
  y = [float(line[2]) for line in lines]

  return (x, y, name)

def draw_graph(title, x, y, label):
  plt.plot(x, y, label=label)
  plt.title(title)
  plt.legend(numpoints=1)
  plt.xlabel("Number of data points")
  plt.ylabel("Error percentage")

def main():
  p_training = "perceptron_training_data.txt"
  mlp_training = "mlp_training_data.txt"
  svm_training = "svm_training_data.txt"

  p_test = "perceptron_test_data.txt"
  mlp_test = "mlp_test_data.txt"
  svm_test = "svm_test_data.txt"

  ptr_data = read_data("out/"+p_training)
  mlptr_data = read_data("out/"+mlp_training)
  svmtr_data = read_data("out/"+svm_training)

  pte_data = read_data("out/"+p_test)
  mlpte_data = read_data("out/"+mlp_test)
  svmte_data = read_data("out/"+svm_test)

  plt.hold(True)
  draw_graph("Training on small data sets, training data error", *ptr_data)
  draw_graph("Training on small data sets, training data error", *mlptr_data)
  draw_graph("Training on small data sets, training data error", *svmtr_data)
  plt.savefig("out/training.eps", format="eps")
  plt.cla()

  draw_graph("Training on small data sets, test data error", *pte_data)
  draw_graph("Training on small data sets, test data error", *mlpte_data)
  draw_graph("Training on small data sets, test data error", *svmte_data)
  plt.savefig("out/test.eps", format="eps")

if __name__ == '__main__':
  main()
