#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMU exercise
# Copyright (c) 2015-2018 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk


# import libraries
from math import pi, sqrt, atan2
import matplotlib.pyplot as plt
import matplotlib.lines as ln
import numpy as np
from scipy.signal import lfilter
import scipy.integrate as integrate

##### Insert initialize code below ###################

## Uncomment the file to read ##
fileName = 'imu_razor_data_static.txt'
# fileName = 'imu_razor_data_pitch_55deg.txt'
# fileName = 'imu_razor_data_roll_65deg.txt'
# fileName = 'imu_razor_data_yaw_90deg.txt'

## IMU type
# imuType = 'vectornav_vn100'
imuType = 'sparkfun_razor'

## Variables for plotting ##
showPlot = True
plotData_pitch = []
plotData_roll = []
plotData_angle = []
plotData_angle_biased = []
timeData = []

## Initialize your variables here ##
myValue_pitch = 0.0

######################################################

# open the imu data file
f = open(fileName, "r")

# initialize variables
count = 0


# a bias of 0.04660033317566759 was introduced in 58.36031794548035 time units
def bias(x):
    return 0.04660033317566759 / 58.36031794548035 * x


# looping through file
for line in f:
    count += 1

    # split the line into CSV formatted data
    line = line.replace('*', ',')  # make the checkum another csv value
    csv = line.split(',')

    # keep track of the timestamps
    ts_recv = float(csv[0])
    if count == 1:
        ts_now = ts_recv  # only the first time
    ts_prev = ts_now
    ts_now = ts_recv

    if imuType == 'sparkfun_razor':
        # import data from a SparkFun Razor IMU (SDU firmware)
        acc_x = int(csv[2]) / 1000.0 * 4 * 9.82
        acc_y = int(csv[3]) / 1000.0 * 4 * 9.82
        acc_z = int(csv[4]) / 1000.0 * 4 * 9.82
        gyro_x = int(csv[5]) * 1 / 14.375 * pi / 180.0
        gyro_y = int(csv[6]) * 1 / 14.375 * pi / 180.0
        gyro_z = int(csv[7]) * 1 / 14.375 * pi / 180.0

    elif imuType == 'vectornav_vn100':
        # import data from a VectorNav VN-100 configured to output $VNQMR
        acc_x = float(csv[9])
        acc_y = float(csv[10])
        acc_z = float(csv[11])
        gyro_x = float(csv[12])
        gyro_y = float(csv[13])
        gyro_z = float(csv[14])

    ##### Insert loop code below #########################

    # Variables available
    # ----------------------------------------------------
    # count		Current number of updates
    # ts_prev	Time stamp at the previous update
    # ts_now	Time stamp at this update
    # acc_x		Acceleration measured along the x axis
    # acc_y		Acceleration measured along the y axis
    # acc_z		Acceleration measured along the z axis
    # gyro_x	Angular velocity measured about the x axis
    # gyro_y	Angular velocity measured about the y axis
    # gyro_z	Angular velocity measured about the z axis

    ## Insert your code here ##

    pitch = atan2(acc_y, sqrt(pow(acc_x, 2) + pow(acc_z, 2)))

    roll = atan2(-acc_x, acc_z)

    unbiased_angle = gyro_z * (ts_now - ts_prev) - bias((ts_now - ts_prev))
    angle = gyro_z * (ts_now - ts_prev)

    if len(plotData_angle) > 0:
        angle += plotData_angle_biased[-1]
        unbiased_angle += plotData_angle[-1]

    # in order to show a plot use this function to append your value to a list:
    plotData_pitch.append(pitch * 180.0 / pi)
    plotData_roll.append(roll * 180.0 / pi)
    plotData_angle.append(unbiased_angle)
    plotData_angle_biased.append(angle)
    timeData.append(ts_now)

######################################################

# closing the file	
f.close()

print('a bias of ' + str(np.max(plotData_angle_biased)) + ' was introduced in ' + str(
    np.max(timeData) - np.min(timeData)) + ' time units')

n = 200  # the larger n is, the smoother curve will be
b = [1.0 / n] * n
a = 1

# show the plot
# if showPlot:
#     plt.plot(plotData_pitch)
#     yy_pitch = lfilter(b, a, plotData_pitch)
#     plt.plot(yy_pitch, linewidth=1, linestyle="-", c="r")  # smooth by filter
#     plt.xlabel('Time')
#     plt.ylabel('Pitch [deg]')
#     plt.savefig('imu_exercise_plot_static_pitch_filtered.png')
#     plt.show()
#
# if showPlot:
#     plt.plot(plotData_roll)
#     yy_roll = lfilter(b, a, plotData_roll)
#     plt.plot(yy_roll, linewidth=1, linestyle="-", c="r")  # smooth by filter
#     plt.xlabel('Time')
#     plt.ylabel('Roll [deg]')
#     plt.savefig('imu_exercise_plot_static_roll_filtered.png')
#     plt.show()

if showPlot:
    plt.plot(plotData_angle_biased, c='b')
    plt.plot(plotData_angle, c='r')
    plt.legend(handles=[
        ln.Line2D([], [], color='blue', label='static data'),
        ln.Line2D([], [], color='red', label='unbiased data')
    ])
    plt.xlabel('Time')
    plt.ylabel('Relative Angular Distance')
    plt.savefig('gyro_z_static_bias.png')
    plt.show()
