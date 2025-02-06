import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt

# data = pd.read_csv(r"D:\1-BukAILab\01-MAX30102\compareEMOTIBIT\R3\2025-05-20_19-10-56-539584_PI.csv")

print("ข้อมูล PPG IR จากเซนเซอร์?\n1.\tEmotiBit\n2.\tMAX30102")
choice = input("Choose your option: ")

if choice == "1":
    path = input("PPG file path: ").strip('"')
    data = pd.read_csv(path)
    signals, info = nk.ppg_process(data['PI'], sampling_rate=25)

    nk.ppg_plot(signals, info)
    plt.show()

elif choice == "2":
    path = input("PPG file path: ").strip('"')
    data = pd.read_csv(path)
    signals, info = nk.ppg_process(data['IR'], sampling_rate=100)

    nk.ppg_plot(signals, info)
    plt.show()