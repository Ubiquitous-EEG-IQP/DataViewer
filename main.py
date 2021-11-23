from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json


def getEOH(path):
    tmp = open(path)
    eoh = 0
    for line in tmp.readlines():
        eoh += 1
        if line.find("# EndOfHeader") >= 0:
            return eoh
    return 0


def readFile(path):
    print(f"Loading data from {path}")
    eoh = getEOH(path)
    data = pd.read_csv(path, skiprows=eoh, header=None, sep="\t", usecols=[2, 3, 4], names=["EEG", "fNIRS1", "fNIRS2"])

    try:
        file1 = open(path, 'r')
        jsonText = file1.readlines()[1][2:]
        headerJson = json.loads(jsonText)
        fs = headerJson["00:07:80:79:6F:DB"]["sampling rate"]
        file1.close()
    except json.decoder.JSONDecodeError:
        print("\theader missing defaulting to sampling frequency of 1000hz")
        fs = 1000
    print(f"\tSampling rate {fs}hz")
    print(data.head())

    return data, fs


def displayData(df):
    # yasa.plot_spectrogram(df["EEG"].to_numpy(), win_sec=1, sf=1000, cmap='Spectral_r')
    # plt.xlabel("Time[S]")
    sr = 1000  # Sampling rate
    resolution = 16  # Resolution (number of available bits)
    signal_red_uA = (0.15 * np.array(df["fNIRS1"])) / 2 ** resolution
    signal_infrared_uA = (0.15 * np.array(df["fNIRS1"])) / 2 ** resolution

    plt.figure(0)
    # Plot EEG
    plt.subplot(2, 2, 1)
    plt.plot(df["EEG"])

    plt.subplot(2, 2, 3)
    plt.specgram(df["EEG"])

    # Plot fNIRS1
    plt.subplot(2, 2, 2)
    plt.plot(signal_red_uA)

    # Plot fNIRS2
    plt.subplot(2, 2, 4)
    plt.plot(signal_infrared_uA)
    plt.show()


if __name__ == '__main__':

    while True:
        Tk().withdraw()
        path = askopenfilename()
        if path == '':
            break
        df, fs = readFile(path)
        displayData(df)
