
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
from neurokit2 import hrv_frequency


# path = input("EDA file path: ").strip('"')
# data = pd.read_csv(path)

# data = nk.data(rf"D:\1-BukAILab\EDA Collection\25Dec\4 depress\2024-12-25_16-21-47-852462_PG.csv")
# print(data)


#
# peaks, info = nk.ecg_peaks(data["ECG"], sampling_rate=100)
# hrv = nk.hrv_time(ppg, sampling_rate=100, show=True)
#
# print(hrv.to_string())

#
# ppg = nk.ppg_simulate(duration=10, sampling_rate=1000, heart_rate=70)
# signals, info = nk.ppg_process(ppg, sampling_rate=1000)
# nk.ppg_plot(signals, info)

# ppg = nk.ppg_simulate(data, sampling_rate=25)
# print(peak)
#
# hrv = nk.hrv_time(ppg, sampling_rate=100, show=True)
# peaks, info = nk.ppg_peaks(ppg, sampling_rate=100, method="elgendi", show=True)


df = pd.read_csv(rf"/EDA Collection/20Dec/1/2024-12-20_16-18-38-578633_PG.csv")
print(df)

PPG = nk.ppg_clean(df['PG'], sampling_rate=100)

print(PPG)
peaks, info = nk.ppg_peaks(PPG, sampling_rate=100)
print(peaks)

hrv = nk.hrv(peaks, sampling_rate=100)
print(hrv.to_string())