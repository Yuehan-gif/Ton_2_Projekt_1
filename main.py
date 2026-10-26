import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

fAbt = 44100 #Abtastrate
f = 1000 #Signalfrequenz
a = 1 #Amplitude
d = 3 #Duration
x = np.linspace(0, d, fAbt*d)
FREQUENCIES = [125, 250, 500, 1000, 2000, 4000, 8000]

eingabe = ""
data_freq = [125, 250, 500, 1000, 2000, 4000, 8000]
data_volume = [1, 0.5,0.2,0.4,1,1,1]


def sin_play(frequency, amplitude):
    y = amplitude * np.sin(2 * np.pi * frequency * x)
    sd.play(y, fAbt)
    sd.wait()

for freq in FREQUENCIES:
    eingabe = ""
    while eingabe != "no":
        a = float(input("Enter volume (0-100): ")) / 100
        print (a)
        sin_play(freq, a)
        eingabe = input ("Did you hear the sine? (yes/no):").lower()
    data_freq.append(freq)
    data_volume.append(a)


plt.stem(data_freq, data_volume)
plt.xscale("log")

# plt.xticks(frequenzen, labels=frequenzen)
# Beschriftungen
plt.xlabel("frequency [Hz]")
plt.ylabel("Volume")
plt.title("Audiogramm")
plt.show()