#!/usr/bin/python3

import argparse
import cam
import datetime
import numpy as np
import send
import threading
import time
import uRAD

parser = argparse.ArgumentParser()
parser.add_argument("points", type = int, default = 0, nargs = "?",
                    help = "number of datapoints to take")
parser.add_argument("-s", "--send", action = "store_true",
                    help = "send data to server")
parser.add_argument("-d", "--duration", nargs = 1, type = int, help = 
                    "capture DURATION s of video on target detection")
parser.add_argument("-t", "--turbine", type = int, default = 2,
                    help = "id number of your wind-turbine")
parser.add_argument("-n", "--no-log", action = "store_false", help =
                    "do not write logfiles")
args = parser.parse_args()

duration = 0
if args.duration:
    global camthread
    camthread = threading.Thread()
    duration = int(args.duration[0])

# uRAD.detection takes an array for each measurement it provides.
# The format is:
# uRAD.detection(distance, velocity, SNR, I, Q, movement)
# even though the manual says otherwise...
# See the documentation for the correct lengths of these arrays

# Radar input parameters
BW   = 240 # using all the BW available = 240 MHz (irrelevant)
MTI  = 0   # MTI mode disable (irrelevant for this application)
Mth  = 1   # sensitivity threshold
Ns   = 200 # 200 samples
Ntar = 1   # only one target of interest
Rmax = 25  # searching in a range of 25 m/s
f0   = 100 # starting at 24.1 GHz
mode = 1   # 1 = doppler mode

# Data output arrays
distance        = [0] * Ntar
velocity        = [0] * Ntar
snr             = [0] * Ntar
iarr            = [0] * Ns
qarr            = [0] * Ns
movement        = [0]

# Output directory
outdir = "/home/pi/fugl/radar/output/"
starttime = datetime.datetime.now().isoformat()
out_i = "I/I_CW_{}.csv".format(starttime)
out_q = "Q/Q_CW_{}.csv".format(starttime)

# Number of datapoints to log, 0 will run forever
ndata = args.points

# Calculate endtime, starttime and birdminutes from 2D-array
def birdmins(arr):
    # arr = [datetime, activity {0..5}, avgspeed]
    # add maximum 10 birdseconds, in case of hangs
    if len(arr):
        maxtime   = 10
        activity  = 0
        birdmins  = 0.0
        endtime   = arr[-1][0]
        starttime = arr[0][0]
        sumspeed  = 0.0
        for i in range(0, len(arr) - 1):
            if arr[i][1]:
                # Add time since last measurement multiplied by number of birds
                # Use the least amount of birds, even if this is 0
                nbirds = min(activity, arr[i][1])
                dt = arr[i + 1][0] - arr[i][0]
                t = min(maxtime, round(dt.seconds + dt.microseconds * 1e-6, 2))
    
                print("Calculated Δt: ", t)
    
                birdmins += nbirds * t / 60
                sumspeed += arr[i][2]
                activity = arr[i][1]
            else:
                activity = 0
        return endtime, starttime, birdmins, sumspeed / len(arr)

# Buffer datapoints before sending
def buffadd(arr, velocity):
    arr.append([datetime.datetime.now(), len(velocity), 
               np.average(np.abs(velocity))])

# Append one sample to csv file, 'safer' than overwriting
def datappend(sample, path):
    csv_string = ""
    for point in sample:
        csv_string += str(point) + ","
    csv_string += datetime.datetime.now().isoformat() + "\n"
    with open(path, 'a') as file:
        file.write(csv_string)

# Create a file, so we can append to it later
def datawrite(path):
    with open(path, 'w') as file:
        #do nothing
        file.write("")

# Check if video capture thread is alive, or start a new
def videocapture(duration, mode = 0):
    global camthread
    # Do nothing if camera is already recording
    if not camthread.is_alive():
        # print("is ded")
        now = datetime.datetime.now().isoformat()
        path = outdir + "vid/{}.h264".format(now)
        camthread = threading.Thread(target = cam.video,
                                    args = (path, duration, mode))
        camthread.start()
        
###############################################################################

if __name__ == "__main__":
    # Number of samples to average before sending
    nsend = 100 

    # Start radar
    uRAD.loadConfiguration(mode, f0, BW, Ns, Ntar, Rmax, MTI, Mth)    
    uRAD.turnON()
    
    # Create files for logging
    if (not args.no_log):
        datawrite(outdir + out_i)
        datawrite(outdir + out_q)

    # Create buffer for sending
    if args.send:
        global activity
        activity = []
    
    # Main datacollection loop
    # Capture ndata datapoints   
    i = 0
    while (i < ndata or not ndata):
        uRAD.detection(0, velocity, snr, iarr, qarr, movement)
        if movement[0]==True:
            print("{}: velocity: {: 3.2f}, snr: {: 3.2f}"
                  .format(i, velocity[0], snr[0]))
            if args.duration:
                videocapture(duration, 1)
            if args.send:
                # Collect data
                buffadd(activity, velocity)
        else:
            print(i)

        # Send data if enabled        
        if args.send and not (i + 1) % nsend and len(activity):
            # send(turbine_id, end, start, birdmins, speed, temp, humid)
            end, start, bms, speed = birdmins(activity)
            
            try:
                send.call_with_timeout(
                    send.send,
                    (args.turbine, end, start, bms, speed, 20, 35),
                    3)
                print("{} Sending".format(activity))
            except:
                #oisann
                print("Could not send data this time.")
            else:
                activity = []

        # Save raw data from radar
        if (not args.no_log):
            datappend(iarr, outdir + out_i)
            datappend(qarr, outdir + out_q)

        # Delay so we do not fry the CPU
        time.sleep(0.01)
        i += 1
    
    # Turn off radar
    uRAD.turnOFF()
    
    # Wait for data transmission
    if args.send and len(activity):
        # send(turbine_id, end, start, birdmins, speed, temp, humid)
        end, start, bms, speed = birdmins(activity)        
        try:
            send.call_with_timeout(
                send.send,
                (args.turbine, end, start, bms, speed, 20, 35),
                30)
            print("{} Sending".format(activity))
        except:
            #oisann
            print("Could not send data this time.")

    # Wait for camera to finish last recording
    if duration:
        if camthread.is_alive():
            camthread.join()
