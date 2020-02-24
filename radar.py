#!/usr/bin/python3

import numpy as np
import uRAD
import argparse
import datetime
import send

parser = argparse.ArgumentParser()
parser.add_argument("points", type=int, default = 0, nargs="?",
                    help = "number of datapoints to take")
parser.add_argument("-s", "--send", action="store_true")
args = parser.parse_args()

# uRAD.detection takes an array for each measurement it provides.
# The format is:
# uRAD.detection(distance, velocity, SNR, I, Q, movement)
# even though the manual says otherwise...
# See the documentation for the correct lengths of these arrays

# Radar input parameters
mode = 1   # 1 = doppler mode
f0   = 100 # starting at 24.1 GHz
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
time = datetime.datetime.now().isoformat()
out_i = "I_CW_{}.csv".format(time)
out_q = "Q_CW_{}.csv".format(time)

# Number of datapoints to log, 0 will run forever
ndata = args.points

# Append one sample to csv file, 'safer' than overwriting
def datappend(sample, path):
    csv_string = ""
    for point in sample[:-1]:
        csv_string += str(point) + ","
    csv_string += str(sample[-1:][0]) + "\n"
    with open(path, 'a') as file:
        file.write(csv_string)

#Create a file, so we can append to it later
def datawrite(path):
    with open(path, 'w') as file:
        #do nothing
        file.write("")
        
##############################################################################

uRAD.loadConfiguration(mode, f0, BW, Ns, Ntar, Rmax, MTI, Mth)

uRAD.turnON()

datawrite(outdir + out_i)
datawrite(outdir + out_q)

i = 0
while (i < ndata or not ndata):
    uRAD.detection(0, velocity, snr, iarr, qarr, movement)
    if movement[0]==True:
        print("velocity: {: 6.2f}, snr: {: 6.2f}".format(velocity[0], snr[0]))
        if args.send:
            send.send(2,np.mean(velocity),20,35)
    else:
        print(i)
    datappend(iarr, outdir + out_i)
    datappend(qarr, outdir + out_q)
    i += 1

uRAD.turnOFF()
