#!/usr/bin/python3

import numpy as np
import uRAD

# input parameters
mode = 1  # sawtooth mode
f0 = 15   # starting at 24.015 GHz
BW = 240  # using all the BW available = 240 MHz
Ns = 200  # 200 samples
Ntar = 1  # only one target of interest
Rmax = 25 # searching in a range of 25 m/s
MTI = 0   # MTI mode disable (irrelevant for this application)
Mth = 4   # most sensitive threshold

print("Hei, sveis. {}".format(np.pi))

uRAD.loadConfiguration(mode, f0, BW, Ns, Ntar, Rmax, MTI, Mth)

uRAD.turnON()

velocity = [0] * Ntar
snr = [0] * Ntar
movement = [0]

while True:
    uRAD.detection(0, velocity, snr, 0, 0, movement)
    if movement[0]==True:
        print("velocity: {: 6.2f}, snr: {: 6.2f}".format(velocity[0], snr[0]))

