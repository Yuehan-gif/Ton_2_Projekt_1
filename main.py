import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from matplotlib.ticker import ScalarFormatter

fAbt = 44100 #Abtastrate
f = 1000 #Signalfrequenz
a = 1 #Amplitude
d = 3 #Duration
x = np.linspace(0, d, fAbt*d)
FREQUENCIES = [125, 250, 500, 1000, 2000, 4000, 8000]

eingabe = ""
data_freq = []
data_volume = []


def sin_play(frequency, amplitude):
    y = amplitude * np.sin(2 * np.pi * frequency * x)
    sd.play(y, fAbt)
    sd.wait()


for freq in FREQUENCIES:
    eingabe = ""
    while eingabe != "nein":
        a = float(input("Lautstärke eingeben (0-100): ")) / 100
        print (a)
        sin_play(freq, a)
        eingabe = input ("War der Ton hörbar? (ja/nein):").lower()
    data_freq.append(freq)
    data_volume.append(a)

# Linienplot mit Datenpunkten statt Stem
plt.plot(data_freq, data_volume, marker='o', linestyle='-', color='b')
plt.xscale("log")
plt.xticks(data_freq, labels=data_freq)
plt.gca().xaxis.set_major_formatter(ScalarFormatter())
plt.minorticks_off()
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Lautstärke (Amplitude)")
plt.title("Audiogramm")

plt.show()