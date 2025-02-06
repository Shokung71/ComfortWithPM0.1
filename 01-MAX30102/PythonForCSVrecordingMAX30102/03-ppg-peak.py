import neurokit2 as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# print(ppg_raw, info)
# ppg[400:600] = ppg[400:600] + np.random.normal(0, 1.25, 200)
# peaks = nk.ppg_peaks(ppg, sampling_rate=18, method="elgendi", show=True)
# nk.ppg_plot(peaks, info)


print("ข้อมูล PPG IR จากเซนเซอร์?\n1.\tEmotiBit\n2.\tMAX30102")
choice = input("Choose your option: ")
if choice == "1":
    path = input("PPG file path: ").strip('"')
    data = pd.read_csv(path)

    peaks, info = nk.ppg_peaks(data["PI"][:300], sampling_rate=25, method="bishop", show=True)
    plt.show()

elif choice == "2":
    path = input("PPG file path: ").strip('"')
    data = pd.read_csv(path)

    peaks, info = nk.ppg_peaks(data["IR"][:300], sampling_rate=25, method="bishop", show=True)
    plt.show()

    # ให้ลองใช้ high pass เพื่อให้ข้อมูลมีความแน่นิ่งและเสถียรขึ้น เมื่อเปรียบเทียบการบันทึกการวัดสัญญาณจาก 2 เซนเซอร์