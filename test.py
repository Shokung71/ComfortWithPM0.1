import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt

# ---- วิดีโอแรก ----
print("EDA data about 15 minutes from watching a normal/natural video.\nsrc: https://youtu.be/AgpWX18dby4?si=28Rujud2GTNEdlVs")
vdo1 = pd.read_csv(rf"D:\1-BukAILab\EmotiBit\Shokung_all\rawData\new1\2024-12-15_13-14-01-421995_EA.csv")

data_clean1 = nk.eda_clean(vdo1["EA"])
data1 = nk.eda_phasic(data_clean1, sampling_rate=15, method="cvxeda")
print(data1)
print()

# ---- วิดีโอที่สอง ----
print("EDA data about 15 minutes from watching a stressed video.\nsrc: https://youtu.be/OZH7TBoKyks?si=M1Pgh1lld4p-q_Cc")
vdo2 = pd.read_csv(rf"D:\1-BukAILab\EmotiBit\Shokung_all\rawData\VDO2-OOP\2024-12-14_20-04-37-140956_EA.csv")

data_clean2 = nk.eda_clean(vdo2["EA"])
data2 = nk.eda_phasic(data_clean2, sampling_rate=15, method="cvxeda")
print(data2)

# ---- การพล็อต ----
plt.figure(figsize=(12, 6))

# พล็อต VDO1
plt.plot(data1["EDA_Phasic"], label="VDO1 (Phasic - Relaxing)", color="blue", linestyle="-")
plt.plot(data1["EDA_Tonic"], label="VDO1 (Tonic - Relaxing)", color="green", linestyle="-")

# พล็อต VDO2
plt.plot(data2["EDA_Phasic"], label="VDO2 (Phasic - Stressing)", color="red", linestyle="-")
plt.plot(data2["EDA_Tonic"], label="VDO2 (Tonic - Stressing)", color="orange", linestyle="-")

# ตั้งค่ากราฟ
plt.title("Comparison of EDA Responses from Two Videos")
plt.xlabel("Time (s)")
plt.ylabel("EDA Signal")
plt.legend()
plt.grid(True)

# แสดงกราฟ
plt.show()
