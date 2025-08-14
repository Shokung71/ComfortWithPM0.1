# นำเข้าจากไฟล์ฟังก์ชั่นที่ไม่อยู่ในไฟล์นี้
import filepath
import deviceProcess
import plotHRV

# นำเข้า Library
import os
import time
import pandas as pd

if __name__ == '__main__':
    pathfile, filename, typefile, pathSave = filepath.getFilepath()
    # print("\npathfile", pathfile)
    # print("filename", filename)
    # print("pathSave", pathSave)
    sampling_rate = int(input("\nEnter the sampling_rate: "))

    # subject_name = input("\nEnter the subject name: ")
    subject_name = filename
    print("Sampling_rate: ", sampling_rate, "\tSubject_name: ", subject_name)

    # try:
    if typefile == '.acq':
        pathfile, filename = deviceProcess.acq_add_timestamp_to_csv(pathfile, pathSave, filename, sampling_rate)
        # print(pathfile, filename)
        device_name = "Biopac"
        color = 'blue'
        signal_column = "PPG"
        saving_filename = "Biopac-PPG-" + filename

    elif typefile == '.csv':
        device_name = "EmotiBit"
        color = 'green'
        signal_column = "PG"    # เพื่อน IMI ใช้ Emo แบบ Green
        saving_filename = "EmotiBit-PPG-Green-" + filename
    else:
        print(f"\nไม่ใช่ประเภทไฟล์ที่เหมาะสมสำหรับการประมวลผลข้อมูลในโปรแกรมนี้ (.csv หรือ .acq เท่านั้น)\nคุณได้ใช้ไฟล์ประเภท {typefile}")
        exit()

    df = pd.read_csv(rf"{pathfile}")
    csv_time = len(df) // (sampling_rate * 60)
    print(f"\nThis csv file has a recording length of ~{csv_time} miniutes. Recorded from {device_name}.")

    print("\nPreparing", end="", flush=True)  # flush=True เพื่อให้พิมพ์ทันที
    for i in range(5):  # หน่วง 5 วินาที พร้อมพิมพ์จุด
        print(".", end="", flush=True)
        time.sleep(1)  # หน่วงทีละ 1 วินาที
    # โค้ดที่ต้องรันหลังรอ 5 วินาที

    # HF
    print("\n\nNext Processing in HF")
    hrvHFData = deviceProcess.ProcessingHrvFreq(device_name, ppg_df=df, window_size=60, sampling_rate=sampling_rate)

    HFoutput_filename = f"hrv_HF_{saving_filename}.csv"
    outputHF_csv_pathfile = os.path.join(saving_filename, HFoutput_filename)
    hrvHFData.to_csv(outputHF_csv_pathfile, index=False)

    # LF
    print("\nNext Processing in LF")
    df = pd.read_csv(rf"{pathfile}")
    hrvLFData = deviceProcess.ProcessingHrvFreq(device_name, ppg_df=df, window_size=120, sampling_rate=sampling_rate)

    LFoutput_filename = f"hrv_LF_{saving_filename}.csv"
    outputLF_csv_pathfile = os.path.join(saving_filename, LFoutput_filename)
    hrvLFData.to_csv(outputLF_csv_pathfile, index=False)

    # LF/HF
    print("\nNext Processing in Ratio LF/HF")
    df = pd.read_csv(rf"{pathfile}")
    hrvLFHFData = deviceProcess.ProcessingHrvFreq(device_name, ppg_df=df, window_size=300, sampling_rate=sampling_rate)

    LFHFoutput_filename = f"hrv_LFHF_{saving_filename}.csv"
    outputLFHF_csv_pathfile = os.path.join(saving_filename, LFHFoutput_filename)
    hrvLFHFData.to_csv(outputLFHF_csv_pathfile, index=False)

    # Ploting graph
    plotHRV.plot_hrv(hrvHFData, hrvLFData, hrvLFHFData, filename, pathSave)

    # EDA
    if device_name == 'EmotiBit':
        pathfile_ea = pathfile.replace("_PG.csv", "_EA.csv")
        eda_df = pd.read_csv(rf"{pathfile_ea}")
    else:
        eda_df = pd.read_csv(rf"{pathfile}")

    edaData, baselineData = deviceProcess(device_name, eda_df, sampling_rate)




    # NOTE: เหลือ ประมวลผล พล็อตกราฟ เซฟกราฟ EDA, ECG, Skin_temp??

    # except:
    #     print(f"????\nคุณได้ใช้ไฟล์ประเภทXXX {typefile}")
    #
