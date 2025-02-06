import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt

pathfile = input("Enter the path of file: ").strip('"')
df = pd.read_csv(rf"{pathfile}")

# ตัดข้อมูลจำนวน trim_time ข้อมูล ทั้งหน้าทั้งหลัง

trim_time = int(input("Enter the trim time: "))
# df_first_x = df.head(trim_time )
# df_last_x = df.tail(trim_time )
df_trimmed = df.iloc[trim_time:-trim_time]

print("ข้อมูล PPG IR จากเซนเซอร์?\n1.\tEmotiBit\n2.\tMAX30102")
choice = input("Choose your option: ")
if choice == "1":
    ppg_cleaned = nk.ppg_clean(df["PI"], sampling_rate=100)
    # ตรวจจับจุด peaks จาก PPG
    signals, info = nk.ppg_peaks(ppg_cleaned, sampling_rate=100)

    # คำนวณ HRV จากสัญญาณ PPG ที่ตรวจจับ peak แล้ว
    hrv_indices = nk.hrv(signals, sampling_rate=100, show=True)

    plt.text(0.01, 0.99, 'EmotiBit', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left', color='white',bbox=dict(facecolor='green'))
    plt.show()

elif choice == "2":
    ppg_cleaned = nk.ppg_clean(df["IR"], sampling_rate=100)
    # ตรวจจับจุด peaks จาก PPG
    signals, info = nk.ppg_peaks(ppg_cleaned, sampling_rate=100)

    # คำนวณ HRV จากสัญญาณ PPG ที่ตรวจจับ peak แล้ว
    hrv_indices = nk.hrv(signals, sampling_rate=100, show=True)

    plt.text(0.01, 0.99, 'MAX30102', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left',color='white',bbox=dict(facecolor='red'))
    plt.show()