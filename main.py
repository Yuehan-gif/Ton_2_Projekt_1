import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from matplotlib.ticker import ScalarFormatter

fAbt = 44100 #Abtastrate
f = 1000 #Signalfrequenz
a = 1 #Amplitude
d = 3 #Duration
x = np.linspace(0, d, fAbt*d)
FREQUENCIES = [125, 250, 500, 1000, 2000, 4000, 8000] #Frequenzen, die gemessen werden sollen

verdeckung = input("Mit Verdeckung? (ja/nein):").lower() #Aktivierung/Deaktivierung von Verdeckung
data_freq = [] #gemessene Frequenz
data_volume = [] #gemessene Lautstärke

#Funktion zum Abspielen des Signals mit oder ohne Verdeckung
def sin_play(frequency, amplitude):
    if verdeckung == "ja":
        noise = 0.1 * np.random.uniform(-1.0, 1.0, fAbt * d)
        sine = amplitude * np.sin(2 * np.pi * frequency * x)
        signal = sine + noise
    else:
        signal = amplitude * np.sin(2 * np.pi * frequency * x)
    sd.play(signal, fAbt)
    sd.wait()

#Messung für die einzelnen Frequenzen
for freq in FREQUENCIES:
    eingabe = ""
    while eingabe != "nein":
        a = float(input("Lautstärke eingeben (0-100): ")) / 100
        print (a)
        sin_play(freq, a)
        a_dbfs = 20 * np.log10(max(a, 1e-6)) #Umwandlung der Lautstärke in dBFS
        eingabe = input ("War der Ton hörbar? (ja/nein):").lower()
    #Speicherung der Daten:
    data_freq.append(freq)
    data_volume.append(a)

#Audiogramm:
plt.plot(data_freq, data_volume, marker='o', linestyle='-', color='b')
plt.xscale("log")
plt.xticks(data_freq, labels=data_freq)
plt.gca().xaxis.set_major_formatter(ScalarFormatter())
plt.minorticks_off()
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.xlabel("Frequenz (Hz)")
plt.ylabel("Lautstärke (dBFS)")
plt.title("Audiogramm")

plt.show()