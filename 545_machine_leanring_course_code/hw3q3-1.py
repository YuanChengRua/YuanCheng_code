# -*- coding: utf-8 -*-
"""HW3Q3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pd3WQdNQevMr6NErijTVU51S3fn6OuJ6
"""

import numpy as np
import matplotlib.pyplot as plt
np.random.seed(0)
x = np.load("pulsar_features.npy")
y = np.load("pulsar_labels.npy")

negInd = y == -1
posInd = y == 1
plt.scatter(x[0, negInd[0, :]], x[1, negInd[0, :]], color='b', s=0.3)
plt.scatter(x[0, posInd[0, :]], x[1, posInd[0, :]], color='r', s=0.3)
plt.figure(1)
plt.show()

initial_theta = np.zeros((x.shape[0], 1))

# Function that generate the J values
def obj_val(xtrain, ytrain, theta_hat, n, lam):
  sum_vals = 0
  for i in range(n):
    temp = 1 - ytrain[0, i] * np.dot(theta_hat.T, xtrain[:, i])
    if temp > 0:
      sum_vals = sum_vals + temp + (lam/2) * np.dot(theta_hat[1:,0].T, theta_hat[1:,0])
    else:
      sum_vals = sum_vals +  (lam/2) * np.dot(theta_hat[1:,0].T, theta_hat[1:,0])
  sum_vals = sum_vals / n

  return sum_vals

# The subgradient method's implementation
def GDregulizedHinge(lam, xtrain, ytrain, maxiter):
  xtrain_org = xtrain

  d, n = xtrain.shape  
  initial_theta = np.zeros((d + 1, 1))
  # initial_bias = 0
  xtrain = np.vstack([np.ones((xtrain.shape[1], 1)).reshape(1, -1), xtrain])
  obj_vals = []
  for iter in range(1,maxiter + 1):
    total_gradient = np.zeros((d + 1, 1))  # gradient of other parameters
    # total_bias = 0      # gradient of bias
    for i in range(n):
      part1 = np.dot(initial_theta.T, xtrain[:,i].reshape(-1,1))
      part2 = ytrain[:,i] * part1

      if part2 < 1:
        temp_gradient = ytrain[0,i] * xtrain[:,i]
           
        total_gradient[:,0] = total_gradient[:,0] + temp_gradient

    total_gradient = (total_gradient - n * lam * initial_theta) / n # substract n lam * initial_theta
    initial_theta = (100 / iter) * total_gradient + initial_theta
    obj_vals.append(obj_val(xtrain, ytrain, initial_theta, n, lam))

  
  return initial_theta, obj_vals


theta_hat, obj_vals = GDregulizedHinge(0.001, x, y, 10)

# The minimium value of the obejective function is 0.4351427

min_obj_val = min(obj_vals)
print(min_obj_val)

lamda = list(range(1,11))
plt.plot(lamda, obj_vals)

# The hyperplane parameters are: bias = 11.5815867, w1 = -17.30541152, w2 = -8.87993462
bias = theta_hat[0]
weights = theta_hat[1:]

print(bias)
print(weights)

# find training error: 0.09151921903599756
x_tilt = np.vstack([np.ones((x.shape[1], 1)).reshape(1, -1), x])
prediction = theta_hat.T.dot(x_tilt)
counter = 0
for idx in range(prediction.shape[1]):
  if prediction[0,idx] * y[0,idx] < 0:
    counter = counter + 1 

print(counter / x_tilt.shape[1])

# The margins and the hyperplane are shown below

x1 = np.linspace(0, 1, 10)
x2_hyper = -(bias + weights[0,0]*x1)/weights[1,0]
x2_m1 = (1 - (bias + weights[0,0]*x1)) / weights[1,0]
x2_m2 = (-1 - (bias + weights[0,0]*x1)) / weights[1,0]
plt.scatter(x[0, negInd[0, :]], x[1, negInd[0, :]], color='b', s=0.3)
plt.scatter(x[0, posInd[0, :]], x[1, posInd[0, :]], color='r', s=0.3)
plt.plot(x1, x2_hyper, '-b', label='hyperplane')
plt.plot(x1, x2_m1, "--", label = 'margin 1')
plt.plot(x1, x2_m2, "--", label = 'margin 2')
plt.figure(2)
plt.show()

# The margin is 0.051411978711393615
mar = 1/np.sqrt(weights[0,0]**2 + weights[1, 0]**2)

# The implementation of SGD
def SGDhinge(lam, xtrain, ytrain, maxiter):
  xtrain = xtrain
  d, n = xtrain.shape  
  initial_theta = np.zeros((d + 1, 1))
  # initial_bias = 0
  xtrain = np.vstack([np.ones((xtrain.shape[1], 1)).reshape(1, -1), xtrain])
  obj_vals = []
  for iter in range(1,maxiter + 1): 
    new_n = np.random.permutation(n)

    for i in new_n:
      part1 = np.dot(initial_theta.T, xtrain[:,i].reshape(-1,1))
      part2 = ytrain[:,i] * part1

      if part2 < 1:
        temp_gradient = ytrain[0,i] * xtrain[:,i]
        temp_gradient = temp_gradient.reshape((d + 1, 1))
        temp_gradient = (temp_gradient - lam * initial_theta)/n
        initial_theta = (100 / iter) * temp_gradient + initial_theta
      else:
        temp_gradient = (lam * initial_theta) / n
        initial_theta = -(100 / iter) * temp_gradient.reshape((d+1, 1)) + initial_theta


    obj_vals.append(obj_val(xtrain, ytrain, initial_theta, n, lam))

  return initial_theta, obj_vals


theta_hat_SGD, obj_vals_SGD = SGDhinge(0.001, x, y, 10)

# The hyper parameters are: bias = 3.88602442, w1 = -5.65532402, w2 = -4.32825642

bias_hat_SGD = theta_hat_SGD[0]
theta_hat_SGD_1 = theta_hat_SGD[1:]
print(bias_hat_SGD)
print(theta_hat_SGD_1)

# The minimum value of the objective is 0.25952763

print(min(obj_vals_SGD))

plt.plot(lamda, obj_vals_SGD)

# The hyperplane and its margins are shown below

x1_sgd = np.linspace(0, 1, 10)
x2_hyper_sgd = -(bias_hat_SGD + theta_hat_SGD_1[0,0] * x1_sgd)/theta_hat_SGD_1[1,0]
x2_m1_sgd = (1 - (bias_hat_SGD + theta_hat_SGD_1[0,0] * x1_sgd)) / theta_hat_SGD_1[1,0]
x2_m2_sdg = (-1 - (bias_hat_SGD + theta_hat_SGD_1[0,0] * x1_sgd)) / theta_hat_SGD_1[1,0]
plt.scatter(x[0, negInd[0, :]], x[1, negInd[0, :]], color='b', s=0.3)
plt.scatter(x[0, posInd[0, :]], x[1, posInd[0, :]], color='r', s=0.3)
plt.plot(x1_sgd, x2_hyper_sgd, '-b', label='hyperplane')
plt.plot(x1_sgd, x2_m1_sgd, "--", label = 'margin 1')
plt.plot(x1_sgd, x2_m2_sdg, "--", label = 'margin 2')
plt.figure()
plt.show()

# The margin of SGD method is 0.14053404323778426
mar_SGD = 1/np.sqrt(theta_hat_SGD_1[0,0]**2 + theta_hat_SGD_1[1, 0]**2)