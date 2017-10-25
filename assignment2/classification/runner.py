import os
import subprocess

percentages = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

running = list()
for p in percentages:
  curr_env = os.environ.copy()
  curr_env["TRAIN_PERCENTAGE"] = str(p)
  p1 = subprocess.Popen(["python", "dataClassifier.py", "-c", "perceptron", "-i", "10", "-t", "5000", "-s", "1000"], env=curr_env)
  p2 = subprocess.Popen(["python", "dataClassifier.py", "-c", "mlp", "-i", "500", "-t", "5000", "-s", "1000"], env=curr_env)
  p3 = subprocess.Popen(["python", "dataClassifier.py", "-c", "svm", "-i", "1", "-t", "5000", "-s", "1000"], env=curr_env)

  p1.wait()
  p2.wait()
  p3.wait()
