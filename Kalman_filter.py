#Exercise 1: 1D Kalman filter
#Given the lists of motions and measurements, the standard deviation of the
#motion and measurement signal, and the initial estimation of the robot's
#position (mu, sig) after the motions.

import math

motions = [1., 1., 2., 1., 1.]
measurements = [5., 6., 8., 9., 10.]
motion_sig = 2.
measurement_sig = 4.
mu = 0.
sig = 100.

#After motion
def predict(mu, sig, v, p):
    mu_new = mu + v
    sig_new = math.sqrt(sig * sig + p * p)
    return [mu_new, sig_new]


#After measurement
def update(mu, sig, v, p):
    mu_new = (p * p * mu + sig * sig * v) / (p * p + sig * sig)
    sig_new = math.sqrt(1 / (1 / (p * p) + 1 / (sig * sig)))
    return [mu_new, sig_new]

for i in range(len(measurements)):
    [mu, sig] = predict(mu, sig, motions[i], motion_sig)
    [mu, sig] = update(mu, sig, measurements[i], measurement_sig)
    
print ([mu, sig])

#Exercise 2: Multidimensional Kalman filter
#We launch a homemade rocket that accelerates 1 m/s2 vertically. 
#The weather is windy, so this is not a steady value.
#We have an onboard altimeter to measure the altitude.
#The sensor has some inaccuracy too.

from matrix import *;
import random;

dt = 0.1
p = 0. # initial position, m
v = 0. # initial velocity, m/s
a = 1. # acceleration, m/s^2
sigma_p_init = 1. # initial uncertainty of p, meters (one standard deviation)
sigma_v_init = 1. # initial uncertainty of v, meters (one standard deviation)
sigma_a = 0.2 # acceleration noise, m/s^2 (one standard deviation)
sigma_p_meas = 10. # measurement uncertainty of p, meters (one standard deviation)

#We use a Kalman filter to estimate the altitude of the rocket during the rise in this noisy environment.
#We use the attached matrix class to set up the matrices as follows:

x = matrix([[p], [v]]) # initial state
A = matrix([[1., dt], [0., 1.]]) # pk = pk-1 + dt*vk-1, vk = vk-1
B = matrix([[dt*dt/2.], [dt]]) # pk = ... + a/2*dt^2, vk = ... + a*dt
u = a # control signal
sigma_p = B.value[0][0] * sigma_a # uncertainty of p
sigma_v = B.value[1][0] * sigma_a # uncertainty of v
var_a = sigma_a * sigma_a
var_p = sigma_p * sigma_p
var_v = sigma_v * sigma_v
P = matrix([[sigma_p_init*sigma_p_init, 0.], [0., sigma_v_init*sigma_v_init]]) # initial uncertainty of p and v, cannot be 0s
Q = matrix([[sigma_p*sigma_p, sigma_p*sigma_v], [sigma_p*sigma_v, sigma_v*sigma_v]]) # process noise covariance
H = matrix([[1., 0]]) # pmeasuredk = pk
R = matrix([[sigma_p_meas*sigma_p_meas]]) # measurement noise covariance
I = matrix([[1., 0.], [0., 1.]]) # identity matrix

#The predict and update functions according to the Kalman filter equations:

def predict(x, P):
    x = A * x + B * u
    P = A * P * A.transpose() + Q
    return x, P

def update(x, P, z):
    Z = matrix([[z]])
    K = P * H.transpose() * (H * P * H.transpose() + R).inverse()
    x = x + K * (Z - H * x)
    P = (I - K * H) * P
    return x, P

#To simulate the launch the next loop has been created. 
#Your task is to draw a diagram that shows the measurement error and the estimation error during the launch.
#The measurement error is the difference between the measured and real position.
#The estimation error is the difference between the estimated position (p from matrix x) and the real position.

import matplotlib.pyplot as plt;
import pandas as pd;

measurement_errors = []
estimation_errors = []

for i in range(100):
    # the sensor is simulated this way:
    p_measured = random.gauss(p, sigma_p_meas)
    
    # Kalman filter: 
    x, P = predict(x, P)
    x, P = update(x, P, p_measured)
    # get the values here to create the diagram
    
    # simulation of the motion:
    a_real = random.gauss(a, sigma_a) # the real, uneven acceleration
    p += dt * v + a_real / 2. * dt * dt # the real position
    v += a_real * dt # the real velocity
    
    measurement_errors.append(p_measured - p)
    estimation_errors.append(x[0][0] - p)

    
df=pd.DataFrame({'x': range(0, 100), 'measurement_errors': measurement_errors, 'estimation_errors': estimation_errors})
plt.plot( 'x', 'measurement_errors', data=df, marker='', color='blue', linewidth=2)
plt.plot( 'x', 'estimation_errors', data=df, marker='', color='orange', linewidth=2)
plt.legend()


















