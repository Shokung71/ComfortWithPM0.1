
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
from neurokit2 import hrv_frequency
from datetime import datetime


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


df = pd.read_csv(rf"/EDA Collection/Shokung_all/VDO1-1 UnderTheSea/2024-12-14_19-30-39-281346_PG.csv")


# แปลง LocalTimestamp (Unix Time) เป็นเวลาในชีวิตมนุษย์
# df['human_readable_time'] = pd.to_datetime(df['LocalTimestamp'], unit='s').dt.strftime('%H:%M:%S')
#
# # แสดง DataFrame ที่แก้ไขแล้ว
# print(df[['LocalTimestamp', 'human_readable_time']])
# #
# แปลง LocalTimestamp เป็นเวลาในรูปแบบที่มนุษย์อ่านได้
df['human_readable_time'] = pd.to_datetime(df['LocalTimestamp'], unit='s').dt.strftime('%H:%M:%S')

# แปลง LocalTimestamp เป็น datetime เพื่อการคำนวณ
df['datetime'] = pd.to_datetime(df['LocalTimestamp'], unit='s')



PPG = nk.ppg_clean(df['PG'], sampling_rate=25)

print(PPG)
peaks, info = nk.ppg_peaks(PPG, sampling_rate=25)
print(peaks)

hrv = nk.hrv(peaks, sampling_rate=25)
print(hrv.to_string())

hrv_welch = nk.hrv_frequency(peaks, sampling_rate=100, show=True, psd_method="welch")
print(hrv_welch.to_string())

# กำหนดช่วงเวลาในการประมวลผล (2 นาที)
time_interval = pd.Timedelta(minutes=2)

# เริ่มต้นการวนลูปทุก ๆ 2 นาที
start_time = df['datetime'].min()
end_time = start_time + time_interval

results = []  # ลิสต์เก็บผลลัพธ์แต่ละช่วง

while start_time < df['datetime'].max():
    # เลือกข้อมูลในช่วงเวลานี้
    segment = df[(df['datetime'] >= start_time) & (df['datetime'] < end_time)]

    # ตรวจสอบว่าช่วงนี้มีข้อมูลหรือไม่
    if not segment.empty:
        # **ตัวอย่างการประมวลผล:** คำนวณค่าเฉลี่ยของคอลัมน์ signal (หรือคอลัมน์อื่น ๆ ที่สนใจ)
        mean_value = segment['signal'].mean()  # สมมติว่ามีคอลัมน์ 'signal'
        results.append({'start_time': start_time, 'end_time': end_time, 'mean_signal': mean_value})

    # ปรับเวลาไปยังช่วงถัดไป
    start_time = end_time
    end_time = start_time + time_interval

# แปลงผลลัพธ์เป็น DataFrame และพิมพ์ผลลัพธ์
results_df = pd.DataFrame(results)
print(results_df)
