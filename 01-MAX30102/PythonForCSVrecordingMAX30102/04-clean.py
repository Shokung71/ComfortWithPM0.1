import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
from neurokit2 import ppg_clean
from sklearn.preprocessing import MinMaxScaler

ppg_signal = pd.read_csv("")
PI  = ppg_signal['PI']

ppg_cleand = nk.ppg_clean(PI, sampling_rate=100)
# peaks, info = nk.ppg_peaks(ppg_cleand, sampling_rate=100, method="bishop", show=True)

peaks = nk.ppg_findpeaks(ppg_cleand, sampling_rate=100, show=True)
# scaler = MinMaxScaler()
# PR_scaled = scaler.fit_transform(PI.values.reshape(-1, 1))
# df_scaled = pd.DataFrame(PR_scaled, columns=["PI_scaled"])
# signals, info = nk.ppg_process(df_scaled['PI_Scaled'], sampling_rate=100)
# num_peaks = len(peaks['PPG_Peaks'])
# print("จำนวน PPG peaks EmotiBit = ", num_peaks)
# nk.ppg_plot(signals, info)

plt.tight_layout()
plt.show()

# signals, info = nk.ppg_process(ppg_signal["PR"], sampling_rate=100)

# import neurokit2 as nk
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
#
# path = input("PPG file path: ").strip('"')
# data = pd.read_csv(path)
#
# PPG = nk.ppg_clean(data['PI'], sampling_rate=25)
#
# print(PPG)
# peaks, info = nk.ppg_peaks(PPG, sampling_rate=25)
# print(peaks)
#
# hrv = nk.hrv(peaks, sampling_rate=25)
# print(hrv.to_string())