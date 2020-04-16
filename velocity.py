from scipy import signal
import numpy as np

def velocity(I_data, Q_data):
    """
    Calculates velocities of a single sample.

    Passed in parameters are I_data and Q_data
    arrays, samplesize is 200.

    Return parameter:
    :: velocities :: list :: contains velocities registered in sample
    """

    c = 299792458
    f0 = 24.05e9
    Fs = 25000 # sampling frequency
    v0 = (c * Fs/2) / (2 * f0)
    velocities = []

    I_data = I_data - np.mean(I_data)
    Q_data = Q_data - np.mean(Q_data)
    complex_sig = I_data + (1j * Q_data)
    fft_sig = abs(np.fft.fftshift(np.fft.fft(complex_sig, 2048)))
    fd_list = signal.find_peaks(fft_sig, distance = 400, prominence = 4000)[0]
    v_convert = np.linspace(-v0, v0, 2048)
    for sample in fd_list:
        velocity = v_convert[sample]
        if velocity > 20:
            continue
        else: velocities.append(velocity)

    return velocities


if __name__  == '__main__':
    """ Testcase data """
    # import matplotlib.pyplot as plt
    # import csv
    # no_velocity_I = []
    # no_velocity_Q = []
    # some_velocity_I = []
    # some_velocity_Q = []
    # more_I = []
    # more_Q = []
    #
    #
    # with open("rawdata_files/uten_I.csv", "r" ) as file:
    #     I_without = csv.reader(file)
    #     for row in I_without:
    #         row.pop() # remove time stamp
    #         row = [int(x) for x in row]
    #         no_velocity_I.append(row)
    #
    # with open("rawdata_files/uten_Q.csv", "r" ) as file:
    #     Q_without = csv.reader(file)
    #     for row in Q_without:
    #         row.pop() # remove time stamp
    #         row = [int(x) for x in row]
    #         no_velocity_Q.append(row)
    #
    # with open("rawdata_files/litt_I.csv", "r" ) as file:
    #     I_some = csv.reader(file)
    #     for row in I_some:
    #         row.pop() # remove time stamp
    #         row = [int(x) for x in row]
    #         some_velocity_I.append(row)
    #
    # with open("rawdata_files/litt_Q.csv", "r" ) as file:
    #     Q_some = csv.reader(file)
    #     for row in Q_some:
    #         row.pop() # remove time stamp
    #         row = [int(x) for x in row]
    #         some_velocity_Q.append(row)
    #
    # with open("rawdata_files/mer_I.csv", "r" ) as file:
    #     I_more = csv.reader(file)
    #     for row in I_more:
    #         row.pop() # remove time stamp
    #         row = [int(x) for x in row]
    #         more_I.append(row)
    #
    # with open("rawdata_files/mer_I.csv", "r" ) as file:
    #     Q_more = csv.reader(file)
    #     for row in Q_more:
    #         row.pop() # remove time stamp
    #         row = [int(x) for x in row]
    #         more_Q.append(row)
    #
    # # for meas in range(0, 100):
    # #     velocities, v_convert, fft_sig = velocity(no_velocity_I[meas], no_velocity_Q[meas])
    # #     plt.plot(v_convert, fft_sig, color = "red")
    # #     velocities, v_convert, fft_sig = velocity(some_velocity_I[meas], some_velocity_Q[meas])
    # #     plt.plot(v_convert, fft_sig, color = "blue")
    # #     velocities, v_convert, fft_sig = velocity(more_I[meas], more_Q[meas])
    # #     plt.plot(v_convert, fft_sig, color = "green")
    # #
    # # plt.show()
    # #
    # # for meas in range(0, len(more_I)):
    # #     print(velocity(more_I[meas],more_Q[meas]))
