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
  mcs = np.array(mcs)
  energy = np.array(energy)
  return mcs, energy

mcs_2, energy_2 = read_file("total_energy_2.txt")
mcs_4, energy_4 = read_file("total_energy_4.txt")
mcs_6, energy_6 = read_file("total_energy_6.txt")
mcs_8, energy_8 = read_file("total_energy_8.txt")
mcs_10, energy_10 = read_file("total_energy_10.txt")
mcs_20, energy_20 = read_file("total_energy_20.txt")
mcs_40, energy_40 = read_file("total_energy_40.txt")

plt.figure(figsize=(13,6))

plt.plot(mcs_40, energy_40, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'gold', label = 'T=40')
plt.plot(mcs_20, energy_20, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'cyan', label = 'T=20')
plt.plot(mcs_10, energy_10, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'fuchsia', label = 'T=10')

plt.plot(mcs_8, energy_8, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'lime', label = 'T=8')
plt.plot(mcs_6, energy_6, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'red', label = 'T=6')
plt.plot(mcs_4, energy_4, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'mediumblue', label = 'T=4')
plt.plot(mcs_2, energy_2, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'darkorange', label = 'T=2')

plt.xlabel('MCS')
plt.ylabel('Total Energy')
leg = plt.legend(fontsize=14,framealpha=0.25)
for line in leg.get_lines():
    line.set_linewidth(2)
plt.grid(True)

plt.savefig("Total_Energy_variousT_vs_MCS.png", dpi=300)

plt.show()

files.download("Total_Energy_variousT_vs_MCS.png")

import os

def delete(filename):
  if os.path.exists(filename):
    os.remove(filename)
    print (f'{filename} correctly removed')
  else:
    print(f'{filename} not found')
  print('------------------------------')

delete("total_energy_2.txt")
delete("total_energy_4.txt")
delete("total_energy_6.txt")
delete("total_energy_8.txt")
delete("total_energy_10.txt")
delete("total_energy_20.txt")
delete("total_energy_40.txt")