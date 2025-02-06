import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt

pathfile = input("Enter the path of file: ").strip('"')
# df = pd.read_csv(rf"{pathfile}")
df_trimmed = pd.read_csv(rf"{pathfile}")

# ตัดข้อมูลจำนวน trim_time ข้อมูล ทั้งหน้าทั้งหลัง

# trim_time = int(input("Enter the trim time (Trimming Head and Tail of the dataframe): "))
# # df_first_x = df.head(trim_time )
# # df_last_x = df.tail(trim_time )
# df_trimmed = df.iloc[trim_time:-trim_time].reset_index(drop=True)
# if len(df_trimmed) < -1:
#     print("ไม่เหลือข้อมูลเพียงพอหลังตัด ต้องใช้ trim_time ที่น้อยกว่านี้")
# else:
print("ข้อมูล PPG IR จากเซนเซอร์?\n1.\tEmotiBit\n2.\tMAX30102")
choice = input("Choose your option: ")

if choice == "1":
    PPG = nk.ppg_clean(df_trimmed["PI"], sampling_rate=100)

    df_trimmed['PPG_clean'] = PPG

    peakRaw, infoRaw = nk.ppg_peaks(df_trimmed["PI"], sampling_rate=100, method="bishop", show=True)
    plt.gcf().text(0.01, 0.96, 'AliNEmotiBit_Raw',
                   fontsize=12, color='white',
                   bbox=dict(facecolor='green'),
                   ha='left', va='top')


    peaksClean, infoClean = nk.ppg_peaks(df_trimmed["PPG_clean"], sampling_rate=100, method="bishop", show=True)
    plt.gcf().text(0.01, 0.96, 'AliNEmotiBit_Clean&Peak',
                   fontsize=12, color='white',
                   bbox=dict(facecolor='green'),
                   ha='left', va='top')
    # plt.show()


    # คำนวณ HRV จากสัญญาณ PPG ที่ตรวจจับ peak แล้ว

    # Compute HRV indices using method="welch กราฟ HRV Frequency"
    hrv_indices = nk.hrv(peaksClean, sampling_rate=100, show=True)
    plt.text(0.01, 0.99, 'AliNEmotiBit', transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top',
             horizontalalignment='left', color='white', bbox=dict(facecolor='green'))
    plt.show()

elif choice == "2":
    # df['IR'] = -df['IR']
    # df['IR'] = -df['IR'].abs()

    PPG = nk.ppg_clean(df_trimmed["IR"], sampling_rate=100)

    df_trimmed['PPG_clean'] = PPG

    peakRaw, infoRaw = nk.ppg_peaks(df_trimmed["IR"], sampling_rate=100, method="bishop", show=True)
    plt.gcf().text(0.01, 0.96, 'AliNMAX30102_Raw',
                   fontsize=12, color='white',
                   bbox=dict(facecolor='red'),
                   ha='left', va='top')

    peaksClean, infoClean = nk.ppg_peaks(df_trimmed["PPG_clean"], sampling_rate=100, method="bishop", show=True)
    plt.gcf().text(0.01, 0.96, 'AliNMAX30102_Clean&Peak',
                   fontsize=12, color='white',
                   bbox=dict(facecolor='red'),
                   ha='left', va='top')
    # plt.show()

    # คำนวณ HRV จากสัญญาณ PPG ที่ตรวจจับ peak แล้ว
    hrv_indices = nk.hrv(peaksClean, sampling_rate=100, show=True)
    plt.text(0.01, 0.99, 'AliNMAX30102', transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top',
             horizontalalignment='left', color='white', bbox=dict(facecolor='red'))
    plt.show()
else:
    print("Try run again.")

# import pandas as pd
# import neurokit2 as nk
# import matplotlib.pyplot as plt
#
# path = input("Enter the path of file: ").strip('"')
# # df = pd.read_csv(rf"{pathfile}")
# df = pd.read_csv(path)
#
#
# print("ข้อมูล PPG IR จากเซนเซอร์?\n1.\tEmotiBit\n2.\tMAX30102")
# choice = input("Choose your option: ")
#
# if choice == "1":
#     PPG = nk.ppg_clean(df["PI"], sampling_rate=100)
#
#     df['PPG_clean'] = PPG
#     peaks, info = nk.ppg_peaks(df["PI"], sampling_rate=100, method="bishop", show=True)
#     plt.show()
#
# elif choice == "2":
#     df['IR'] = -df['IR']    # invert -1 value in graph into the same trand without fliping graph
#
#     PPG = nk.ppg_clean(df["IR"], sampling_rate=100)
#
#     df['PPG_clean'] = PPG
#
#     peaks, info = nk.ppg_peaks(df["IR"], sampling_rate=100, method="bishop", show=True)
#     plt.show()