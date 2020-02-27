import csv
import matplotlib.pyplot as plt
import numpy as np

"""
Processing data from uRad

This script aims to process doppler_shift
and calculate radial velocity of
incoming/outgoing objects.
"""

def velocity(i_file, q_file):
    """
    Calculate velocity

    This function fetches rawdata from
    file, calculates doppler_shift and velocity.

    Parameters:
    :c (int): speed of light
    :f0 (int): radar frequency
    :Fs (int): sampling frequency
    :v0 (func): velocity
    :i (list): infase component
    :q (list): quadrature component
    :fd (int): doppler_shift
    :return: v_list: list of sample velocities
    """
    c = 299792458
    f0 = 24.05e9 # 24.05 GHz
    Fs = 25000 # sampling frequency
    v0 = (Fs/2 * c) / (2 * f0)

    i_data = "rawdata_files/" + i_file
    q_data = "rawdata_files/" + q_file

    i = []
    q = []
    v_list = []

    with open(i_data) as file_1, open(q_data) as file_2:
        i_read = csv.reader(file_1)
        q_read = csv.reader(file_2)

        fig, ax = plt.subplots(1, 2) # initialize plots
        ax[0].set_title('Frequency Components')
        ax[0].set_xlabel('Frequency [Hz]')
        ax[0].set_ylabel('Amplitude')
        ax[1].set_title('Velocity')
        ax[1].set_xlabel('time (?)')
        ax[1].set_ylabel('m/s')

        for rows_i, rows_q in zip(i_read, q_read):

            i = ([int(value_i) for value_i in rows_i[:200]]) # infase
            q = ([int(value_q) for value_q in rows_q[:200]]) # quadrature

            i = i - np.mean(i) # remove dc-offset
            q = q - np.mean(q)

            complex_sig = i + (1j * q)
            fft_sig = np.fft.fftshift(np.fft.fft(complex_sig, 4096))

            f = np.linspace(-Fs/2, Fs/2, 4095)
            ax[0].plot(f, abs(fft_sig[1:]))

            fd_sample = np.argmax(fft_sig)
            v_convert = np.linspace(-v0, v0, 4095)
            v = v_convert[fd_sample]
            v_list.append(v) # list of sample velocities

        # TODO: Fix time-axes
        time = range(0, len(v_list))
        ax[1].scatter(time, v_list)
        plt.show()
        file_1.close()
        file_2.close()

    return v_list


if __name__ == "__main__":
    v_list = velocity("I_CW.csv", "Q_CW.csv")
    print(v_list)
