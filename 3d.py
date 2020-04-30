from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np
import csv
import glob
import argparse
import datetime
import velocity

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--logaritmic", help="plot logaritmic amplitude",
                    action="store_true")
parser.add_argument("ifile", default = "", nargs = "?", type = str)
parser.add_argument("qfile", default = "", nargs = "?", type = str)
args = parser.parse_args()

sample_size = 200
ipath = args.ifile or sorted(glob.glob("I_CW*.csv"))[-1] or "I_CW.csv"
qpath = args.qfile or sorted(glob.glob("Q_CW*.csv"))[-1] or "Q_CW.csv"

print("Opening files:\n\t- {}\n\t- {}".format(ipath, qpath))

fftsize = velocity.fftsize
vmax = velocity.v0
crop = 0.25 * fftsize

f = np.linspace(-vmax, vmax, fftsize, endpoint = False) 
adata = []
tdata = []
vx = []
vy = []

# def jtransform(ivalues, qvalues):
#     ikonst = (np.mean(ivalues))
#     qkonst = (np.mean(qvalues))
#     ivalues = np.hamming(len(ivalues)) * np.add(ivalues, - ikonst)
#     qvalues = np.hamming(len(qvalues)) * np.add(qvalues, - qkonst)
#     # Remove the remaining DC after applying hamming window
#     ikonst = (np.mean(ivalues))
#     qkonst = (np.mean(qvalues))
#     ivalues = np.add(ivalues, - ikonst)
#     qvalues = np.add(qvalues, - qkonst)
#     qvalues = np.multiply(1j, qvalues)
# 
#     return np.abs(np.fft.fftshift(np.fft.fft(np.add(ivalues, qvalues), fftsize)))

with open(ipath) as ifil, open(qpath) as qfil:
    ireader = csv.reader(ifil)
    qreader = csv.reader(qfil)
    i = 0
    for ipoint, qpoint in zip(ireader, qreader):
        i += 1
        ivalues = [int(value) for value in ipoint[:sample_size]]
        qvalues = [int(value) for value in qpoint[:sample_size]]
   
        adata.append(velocity.transform(ivalues, qvalues))
        tdata.append(matplotlib.dates.date2num(datetime.datetime.fromisoformat(ipoint[-1])))
        vy.append(velocity.ftovel(adata[-1]))
        vx.append([tdata[-1]] * len(vy[-1]))

vx = [y for x in vx for y in x]
vy = [y for x in vy for y in x] 

print(i, len(tdata))
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(211)
ax2 = plt.subplot(212, sharex=ax, sharey=ax)
#ax.set_ylim(-18, 18)
#ax.set_xlim(matplotlib.dates.date2num('10:56:21'),matplotlib.dates.datestr2num('10:56:47'))
ax.set_ylim(-35, 35)
tfmt = matplotlib.dates.DateFormatter('%H:%M:%S:%f')
ax.set_xlabel(r'Tid [HH:MM:SS]')
ax.set_ylabel(r'Hastighet [m/s]')

ax.xaxis.set_major_formatter(tfmt)
ax2.xaxis.set_major_formatter(tfmt)

if args.logaritmic:
    noisefloor = (-80)
    x, y = np.meshgrid(tdata, f)
    print(len(vx), len(vy))
    z = np.maximum(20 * np.log10(np.abs(adata)) - 20 * np.log10(sample_size * 4096),
               noisefloor)
    print(len(x), len(y), len(z)) 
    cont = ax.contourf(x,y,z.T, cmap=plt.cm.inferno, levels=50, vmin=noisefloor, vmax=-50)
    ax2.scatter(vx, vy)
else:
    noisefloor = 0
    x, y = np.meshgrid(tdata, f)
    z = np.maximum(noisefloor, np.abs(adata))
    print(len(x), len(y), len(z))
    cont = ax.contourf(x,y,z.T, cmap=plt.cm.inferno, levels=50, vmin=noisefloor,vmax=1500)
    ax2.scatter(vx, vy)
 
#cbar = plt.colorbar(cont)
#cbar.ax.set_ylabel(r'Målt signalstyrke (normalisert) [dB]')
#plt.tight_layout()
#plt.savefig("tempor.png", dpi=600)
plt.show()


