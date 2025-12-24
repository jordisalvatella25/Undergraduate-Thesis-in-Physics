from google.colab import files
uploaded = files.upload()

import numpy as np
import matplotlib.pyplot as plt

def read_file(filename):
  mcs=[]
  energy=[]
  with open(filename, "r") as f:
    for line in f:
      if line.startswith("#"):
        continue
      else:
        parts=line.strip().split()
        Step, E = None, None
        Step = int(parts[0])
        E = float(parts[1])
        mcs.append(Step)
        energy.append(E)
  return mcs, energy

mcs_adhesion, energy_adhesion = read_file("adhesion_energy.txt")
mcs_volume, energy_volume = read_file("volume_energy.txt")
mcs_total, energy_total = read_file("total_energy.txt")
energy_total_secondpart = energy_total[-500:]
mean_total_energy = np.mean(energy_total_secondpart)

plt.figure(figsize=(13,6))
plt.plot(mcs_total, energy_total, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'green', label = 'Total Energy')
plt.axhline(y=mean_total_energy, color = 'red', linestyle = '-', linewidth = 1.5, label = f'Mean Energy = {mean_total_energy:.0f}')
plt.xlabel('MCS')
plt.ylabel('Total Energy')
plt.legend()
plt.grid(True)

plt.savefig("Total_Energy_vs_MCS.png", dpi=300)

plt.show()

files.download("Total_Energy_vs_MCS.png")

plt.figure(figsize=(13,6))

plt.plot(mcs_total, energy_total, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'green', label = 'Total Energy')
plt.plot(mcs_adhesion, energy_adhesion, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'red', label = 'Adhesion Energy')
plt.plot(mcs_volume, energy_volume, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'blue', label = 'Volume Energy')

plt.xlabel('MCS')
plt.ylabel('Energy')
plt.legend()
plt.grid(True)

plt.savefig("Energies_vs_MCS.png", dpi=300)

plt.show()

files.download("Energies_vs_MCS.png")

import os

def delete(filename):
  if os.path.exists(filename):
    os.remove(filename)
    print (f'{filename} correctly removed')
  else:
    print(f'{filename} not found')
  print('------------------------------')

delete("adhesion_energy.txt")
delete("volume_energy.txt")
delete("total_energy.txt")