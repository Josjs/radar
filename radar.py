#!/usr/bin/python3

import numpy as np
import uRAD

# uRAD.detection takes an array for each measurement it provides.
# The format is:
# uRAD.detection(distance, velocity, SNR, I, Q, movement)
# even though the manual says otherwise...
# See the documentation for the correct lengths of these arrays

# Radar input parameters
mode = 1   # 1 = doppler mode
f0   = 15  # starting at 24.015 GHz
BW   = 240 # using all the BW available = 240 MHz
Ns   = 200 # 200 samples
Ntar = 1   # only one target of interest
Rmax = 25  # searching in a range of 25 m/s
MTI  = 0   # MTI mode disable (irrelevant for this application)
Mth  = 1   # sensitivity threshold

# Data output arrays
distance        = [0] * Ntar
velocity        = [0] * Ntar
snr             = [0] * Ntar
movement        = [0]
iarr            = [0] * Ns
qarr            = [0] * Ns

# Output directory
outdir = "./output/"
out_i = "I_CW.csv"
out_q = "Q_CW.csv"

# Number of datapoints to log, 0 will run forever
ndata = 100

# Append one sample to csv file, 'safer' than overwriting
def datappend(sample, path):
    csv_string = ""
    for point in sample[:-1]:
        csv_string += str(point) + ","
    csv_string += str(sample[-1:][0]) + "\n"
    with open(path, 'a') as file:
        file.write(csv_string)
        
##############################################################################

uRAD.loadConfiguration(mode, f0, BW, Ns, Ntar, Rmax, MTI, Mth)

uRAD.turnON()

i = 0
while (i < ndata or not ndata):
    uRAD.detection(0, velocity, snr, iarr, qarr, movement)
    if movement[0]==True:
        print("velocity: {: 6.2f}, snr: {: 6.2f}".format(velocity[0], snr[0]))
        datappend(iarr, outdir + out_i)
        datappend(qarr, outdir + out_q)
        i += 1

