import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--logaritmic", help="plot logaritmic amplitude",
                    action="store_true")
args = parser.parse_args()

sample_size = 200
ipath = "I_CW.csv"
qpath = "Q_CW.csv"

idata = []
qdata = []
crop = 0

with open(ipath) as ifil, open(qpath) as qfil:
    ireader = csv.reader(ifil)
    qreader = csv.reader(qfil)
    for ipoint, qpoint in zip(ireader, qreader):
        ivalues = [int(value) for value in ipoint[:sample_size]]
        qvalues = [int(value) for value in qpoint[:sample_size]]
        ivalues = np.hamming(len(ivalues)) * ivalues
        qvalues = np.hamming(len(qvalues)) * qvalues
        ikonst = (np.mean(ivalues))
        qkonst = (np.mean(qvalues))
        ivalues = np.add(ivalues, - ikonst)
        qvalues = np.add(qvalues, - qkonst)
        qvalues = np.multiply(1j, qvalues)
        idata.append(np.fft.fftshift(np.fft.fft(np.add(ivalues, qvalues)))[crop:-(crop+1)])

if args.logaritmic:
    plt.imshow(np.maximum(-1, np.log10(np.abs(idata))), cmap=plt.cm.inferno, alpha=1)
else:
    plt.imshow(np.minimum(1000, np.abs(idata)), cmap=plt.cm.inferno, alpha=1)

plt.colorbar()
plt.show()
