# -*- coding: utf-8 -*-
"""SOC_Assignment_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mvpmtKECioTL1h58BqbrQekv68OjeN5Y

# Import lib
"""

import pickle as pkl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""# Loading Datasets"""

df = pd.read_pickle("/content/drive/MyDrive/train_data.pkl")
type(df)                            # a dictionary 
X = np.array(df['X'])
X = X.T
Y = np.array(df["y"])
X = np.divide(X, 255) #normalized

# to split data into test & train dataset
X_train = X[ : , :50000]
X_test = X[ : , 50000: ]
Y_train = Y[ : 50000, : ].reshape(1,50000)
Y_test = Y[50000 : , : ].reshape(1,10000)

Y_test

# displaying random 16 numbers
import random
rand = random.sample(range(0,60000), 16)
print(rand)
for i in rand:
  image = X[ : ,i, None]
  image = image.reshape((28,28))*255
  plt.gray()
  plt.imshow(image, interpolation = "nearest")
  plt.show()
  print(Y[i])

"""# Building up parts of our classifier"""

# Activation functions
def ReLU(Z):
  return np.maximum(0,Z)
def softmax(Z):
  return np.exp(Z)/np.sum(np.exp(Z), axis=0)

# initializing the weights
def init_params():
  W0 = np.random.randn(10, 784)
  b0 = np.random.randn(10,1)
  W1 = np.random.randn(10,10)
  b1 = np.random.randn(10,1)
  return W0, b0, W1, b1

# Forward propogation
def forward_propg(X, W0, b0, W1, b1):
  Z1 = W0.dot(X) + b0
  A1 = ReLU(Z1)
  Z2 = W1.dot(A1) + b1
  A2 = softmax(Z2)
  return Z1, A1, Z2, A2

def one_hot(Y):
  one_hot_Y = np.zeros((Y.size, Y.max()+1))
  one_hot_Y[np.arange(Y.size), Y] = 1
  one_hot_Y = one_hot_Y.T
  return one_hot_Y

def deriv_ReLU(Z):
    return Z>0

# Backwad propogation
def backward_propg(X, Y, W1, Z1, A1, Z2, A2):
  m = Y.size
  one_hot_Y = one_hot(Y)
  dZ2 = A2 - one_hot_Y
  dW1 = 1/m * dZ2.dot(A1.T)
  db1 = 1/m * np.sum(dZ2)
  dZ1 = W1.T.dot(dZ2) * deriv_ReLU(Z1)
  dW0 = 1/m * dZ1.dot(X.T)
  db0 = 1/m * np.sum(dZ1)
  return dW0, db0, dW1, db1 

def update_param(W0, b0, W1, b1, dW0, db0, dW1, db1, alpha):
  W0 = W0 - alpha*dW0
  b0 = b0 - alpha*db0
  W1 = W1 - alpha*dW1
  b1 = b1 - alpha*db1
  return W0, b0, W1, b1

def get_prediction(A2):
  return np.argmax(A2, 0)

def get_accuracy(pred, Y):
  #print(pred, Y)
  return np.sum(pred == Y)/Y.size

# gradient descent (standard batch gradient decent)
def grad_desc(X, Y, epox, alpha):
  W0, b0, W1, b1 = init_params()
  for i in range(epox):
    Z1, A1, Z2, A2 = forward_propg(X, W0, b0, W1, b1)
    dW0, db0, dW1, db1 = backward_propg(X, Y, W1, Z1, A1, Z2, A2)
    W0, b0, W1, b1 = update_param(W0, b0, W1, b1, dW0, db0, dW1, db1, alpha)
    
    if i%50 == 0:
      print("Iteration: ", i)
      print("Accuracy: ", get_accuracy(get_prediction(A2), Y))
  return W0, b0, W1, b1

"""# Training"""

#training the model
W0, b0, W1, b1 = grad_desc(X_train, Y_train, 10000, 0.1)

# achived a accuracy of 86.5%

"""# Making predictions on test dataset"""

def make_pred(W0, b0, W1, b1, X, Y):
  Z1, A1, Z2, A2 = forward_propg(X, W0, b0, W1, b1)
  print("Accuracy: ", get_accuracy(get_prediction(A2), Y))

make_pred(W0, b0, W1, b1, X_test, Y_test)

# achives an accuracy of 85.4%

"""# Save as pickle"""

import pickle
import random
from google.colab import files

roll_num = "20D170020"
hidden_dim = 10
model_dict = {
    'z': 10, # hidden dimension of your model
    'layer_0_wt': W0, # layer 0 weight (784, z)
    'layer_0_bias': b0, # layer 0 bias (z, 1)
    'layer_1_wt': W1, # layer 1 weight (z, 10)
    'layer_1_bias': b1 # layer 1 bias (10, 1)
}

assert model_dict['layer_0_wt'].shape == (10,784)
assert model_dict['layer_0_bias'].shape == (10, 1)
assert model_dict['layer_1_wt'].shape == (10, 10)
assert model_dict['layer_1_bias'].shape == (10, 1)

with open(f'model_20D170020.pkl', 'wb') as f:
    pickle.dump(model_dict, f)
    files.download(f'model_20D170020.pkl')