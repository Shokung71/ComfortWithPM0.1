import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt


# อ่านไฟล์ CSV
df = pd.read_csv(rf"D:\1-BukAILab\EDA Collection\Shokung_all\VDO1-1 UnderTheSea\2024-12-14_19-30-39-281346_PG.csv")

# แปลง LocalTimestamp เป็น datetime และเวลาแบบ human-readable
df['human_readable_time'] = pd.to_datetime(df['LocalTimestamp'], unit='s').dt.strftime('%H:%M:%S')  # เพิ่มคอลัมน์ human_readable_time
df['datetime'] = pd.to_datetime(df['LocalTimestamp'], unit='s')  # เพิ่มคอลัมน์ datetime

# ทำความสะอาดสัญญาณ PPG
PPG = nk.ppg_clean(df['PG'], sampling_rate=25)  # ใช้ neurokit2 ทำความสะอาดสัญญาณ PPG

# เพิ่มคอลัมน์สัญญาณ PPG ที่ทำความสะอาดแล้วลงใน DataFrame
df['PPG_clean'] = PPG  # เพิ่มคอลัมน์ PPG_clean

# กำหนดช่วงเวลาสำหรับการแบ่งข้อมูล (2 นาที)
time_interval = pd.Timedelta(minutes=2)  # กำหนดช่วงเวลาทุก 2 นาที
start_time = df['datetime'].min()  # กำหนดเวลาจุดเริ่มต้น
end_time = start_time + time_interval  # คำนวณเวลาจุดสิ้นสุด

# เก็บผลลัพธ์ HRV
hrv_results = []  # สร้างลิสต์สำหรับเก็บผลลัพธ์

while start_time < df['datetime'].max():  # วนลูปจนกว่าจะครบทุกช่วงเวลา
    # เลือกข้อมูลในช่วงเวลานี้
    segment = df[(df['datetime'] >= start_time) & (df['datetime'] < end_time)]  # เลือกข้อมูลที่อยู่ในช่วงเวลา start_time ถึง end_time

    if not segment.empty:  # ตรวจสอบว่าช่วงเวลานี้มีข้อมูล
        # สกัด peaks ของ PPG
        peaks, info = nk.ppg_peaks(segment['PPG_clean'], sampling_rate=25)  # ค้นหา peaks ของ PPG ในช่วงเวลานี้

        # คำนวณ HRV
        hrv = nk.hrv(peaks, sampling_rate=25)  # คำนวณค่า HRV จาก peaks

        # คำนวณ HRV_Frequency (Welch Method)
        hrv_welch = nk.hrv_frequency(peaks, sampling_rate=25, show=False, psd_method="welch")  # คำนวณ Welch PSD

        # เก็บผลลัพธ์ในรูปแบบ dictionary
        hrv_results.append({
            "start_time": start_time,  # เวลาเริ่มต้นของช่วงนี้
            "end_time": end_time,  # เวลาสิ้นสุดของช่วงนี้
            "HRV_LF": hrv_welch["HRV_LF"][0] if "HRV_LF" in hrv_welch else None,  # ค่า HRV_LF
            "HRV_HF": hrv_welch["HRV_HF"][0] if "HRV_HF" in hrv_welch else None,  # ค่า HRV_HF
        })

    # ขยับไปยังช่วงเวลาถัดไป
    start_time = end_time  # อัปเดตเวลาเริ่มต้นใหม่
    end_time = start_time + time_interval  # อัปเดตเวลาสิ้นสุดใหม่

# สร้าง DataFrame จากผลลัพธ์
hrv_results_df = pd.DataFrame(hrv_results)  # สร้าง DataFrame จากผลลัพธ์ที่เก็บไว้ใน hrv_results

# แสดงผลลัพธ์
print(hrv_results_df.to_string())  # พิมพ์ DataFrame ทั้งหมด

# plt.plot(rv_results_df["EDA_Phasic"], label="VDO1 (Phasic)", color="blue")

# Plot ค่า HRV_HF ในแต่ละช่วงเวลา
plt.figure(figsize=(12, 6))
plt.plot(hrv_results_df['start_time'], hrv_results_df['HRV_LF'], marker='o', linestyle='-', color='red', label='HRV_LF')
plt.title('HRV_LF Over Time', fontsize=14)
plt.xlabel('Start Time of Interval', fontsize=12)
plt.ylabel('HRV_LF (Welch Method)', fontsize=12)
plt.xticks(rotation=45)  # หมุนแกน x ให้เวลาอ่านง่ายขึ้น
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

