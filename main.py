import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from matplotlib.ticker import ScalarFormatter

fAbt = 44100 #Abtastrate
f = 1000 #Signalfrequenz
a = 1 #Amplitude
d = 3 #Duration
x = np.linspace(0, d, fAbt*d)
#Kalibrierungston:
cal_amp = 10 ** (-20 / 20) #-20 dBFS als Richtwert
x_cal = np.linspace(0, 60, int(fAbt * 30))
cal_sound = cal_amp * np.sin(2 * np.pi * 1000 * x_cal)
FREQUENCIES = [125, 250, 500, 1000, 2000, 4000, 8000] #Frequenzen, die gemessen werden sollen

verdeckung = input("Mit Verdeckung? (ja/nein):").strip().lower() #Aktivierung/Deaktivierung von Verdeckung
while verdeckung not in ["ja", "nein"]:
    verdeckung = input("Bitte mit ja oder nein antworten: ").strip().lower()
data_freq = [] #gemessene Frequenz
data_volume = [] #gemessene Lautstärke
data_volume_1khz = []
print (f"Messung des Audiogramms {'mit' if verdeckung == 'ja' else 'ohne'} Verdecker:")

print("Lautstärkekalibrierung:")
sd.play(cal_sound, fAbt)
input("Enter zum Bestätigen.")
sd.stop()
print("Lautstärke kalibriert.\n")

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
    letzter_ton = None
    print (f"Frequenz = {freq}:")
    while eingabe != "nein":
        a_dbfs = float(input("Lautstärke in dBFS eingeben (-90 bis 0, positive Werte werden in negative umgewandelt): "))
        if a_dbfs > 0:
            a_dbfs = -a_dbfs
        a = 10 ** (a_dbfs / 20) #Umrechnung von dBFS lineare Amplitude
        print (f"Lautstärke (dBFS): {a_dbfs}")
        sin_play(freq, a)
        eingabe = input ("War der Ton hörbar? (ja/nein):").strip().lower()
        while eingabe not in ["ja", "", "yes", "nein", "no", "ne"]:
            eingabe = input("Bitte mit ja oder nein antworten: ").strip().lower()
        #Speichern der noch hörbaren Lautstärke
        if eingabe in ["ja", "", "yes"]:
            letzter_ton = a_dbfs
        #Überprüfung ob überhaupt ein hörbarer Ton gemessen wurde
        elif eingabe == "nein" and letzter_ton is None:
            print("Der erste Ton war nicht hörbar! Bitte einen lauteren Ton wählen")
            eingabe = ""

    #Speicherung der Daten:
    data_freq.append(freq)
    data_volume.append(letzter_ton)

for vol in data_volume:
    data_volume_1khz.append(vol - data_volume[3])


#Audiogramm:
plt.plot(data_freq, data_volume_1khz, marker='o', linestyle='-', color='b')
plt.xscale("log")
plt.xticks(data_freq, labels=data_freq)
plt.gca().xaxis.set_major_formatter(ScalarFormatter())
plt.minorticks_off()
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.xlabel("Frequenz (Hz)")
plt.ylabel("Relativer Pegel zu 1 kHz (dB)")
plt.title(f"Audiogramm ({'mit' if verdeckung == 'ja' else 'ohne'} Verdecker)")

plt.show()