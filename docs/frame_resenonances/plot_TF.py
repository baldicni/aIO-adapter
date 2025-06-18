import matplotlib.pyplot as plt
import numpy as np

filename = ['displacement_X_risposta_X.txt', 'displacement_X_risposta_Y.txt', 'displacement_X_risposta_Z.txt', 'displacement_Z_risposta_X.txt', 'displacement_Z_risposta_Y.txt', 'displacement_Z_risposta_Z.txt']

def produce_plot(filename):
    data = np.loadtxt(filename, unpack=False, skiprows=1)
    freq = data[1:, 1]  # (Frequenza)
    amp = data[1:, 2]   # (Ampiezza)
    phase = data[1:, 3] # (Fase)

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.loglog(freq, amp)  
    plt.xlabel('Frequenza [Hz]')
    plt.ylabel('Ampiezza [mm]')
    plt.title('Diagramma di Bode - Ampiezza')
    plt.grid(True, which="both", ls="-")

    plt.subplot(2, 1, 2)
    plt.semilogx(freq, np.unwrap(np.deg2rad(phase)) * 180 / np.pi)
    plt.xlabel('Frequenza [Hz]')
    plt.ylabel('Fase [°]')
    plt.title('Diagramma di Bode - Fase')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename.replace('.txt', '.png'))
    #plt.show()

for file in filename:
    produce_plot(file)
    print(f"Plot saved for {file}")