#!/usr/bin/python3

import numpy as np
import uRAD

print("Hei, sveis. {}".format(np.pi))

uRAD.loadConfiguration(1, 25, 0, 200, 5, 15, 0, 4)
uRAD.turnON()

velocity = [0]
snr = [0]

while True:
    uRAD.detection(0, velocity, snr, 0, 0, 0)
    print("velocity: {}, snr: {}".format(velocity[0], snr[0]))

