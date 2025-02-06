import pandas as pd
import neurokit2 as nk

import matplotlib.pyplot as plt

print("EDA data about 15 minutes from watching a normal/natural video.\nsrc: https://youtu.be/AgpWX18dby4?si=28Rujud2GTNEdlVs")
vdo1 = pd.read_csv(rf"D:\1-BukAILab\EmotiBit\Shokung_all\rawData\VDO1-1 UnderTheSea\2024-12-14_19-30-39-281346_EA.csv")

data_clean = nk.eda_clean(vdo1["EA"])
data1 = nk.eda_phasic(data_clean, sampling_rate=15, method="cvxeda")
print(data1)
print()

plt.figure(figsize=(10, 5))
plt.plot(data1["EDA_Phasic"], label="VDO1 (Phasic)", color="blue")
plt.plot(data1["EDA_Tonic"], label="VDO1 (Tonic)", color="green")
plt.title("EDA Response from VDO1 (Relaxing Video)")
plt.xlabel("Time (s)")
plt.ylabel("EDA Signal")
plt.legend()
plt.show()

# ----

print("EDA data about 15 minutes from watching a stressed video.\nsrc: https://youtu.be/OZH7TBoKyks?si=M1Pgh1lld4p-q_Cc")
vdo2 = pd.read_csv(rf"D:\1-BukAILab\EmotiBit\Shokung_all\rawData\VDO2-OOP\2024-12-14_20-04-37-140956_EA.csv")

data_clean = nk.eda_clean(vdo2["EA"])
data2 = nk.eda_phasic(data_clean, sampling_rate=15, method="cvxeda")
print(data2)

plt.figure(figsize=(10, 5))
plt.plot(data2["EDA_Phasic"], label="VDO2 (Phasic)", color="blue")
plt.plot(data2["EDA_Tonic"], label="VDO2 (Tonic)", color="green")
plt.title("EDA Response from VDO2 (Stressing Video)")
plt.xlabel("Time (s)")
plt.ylabel("EDA Signal")
plt.legend()
plt.show()