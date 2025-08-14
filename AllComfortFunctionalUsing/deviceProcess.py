import filepath

import os
from datetime import datetime, timedelta
import pandas as pd
import bioread
import neurokit2 as nk
import warnings
from pyEDA.main import *
import numpy as np

def acq_add_timestamp_to_csv(pathfile, pathSave, filename, sampling_rate):
    data = bioread.read_file(rf"{pathfile}")
    print("\n", data, "\n")

    df = pd.DataFrame({ch.name: ch.data for ch in data.channels})

    # ตัวอย่างข้อมูลจาก Biopac
    raw_time = input("Enter start datetime (e.g. Aug 13 2025 15:42:40.479): ")
    # แปลงเป็น datetime object
    start_time = datetime.strptime(raw_time, "%b %d %Y %H:%M:%S.%f")
    print("Start time:", start_time)

    time_delta = timedelta(milliseconds=1000 / sampling_rate)

    timestamps = [start_time + i * time_delta for i in range(len(df))]
    df.insert(0, 'Timestamp', timestamps)

    # บันทึกเป็น .csv
    save_csv_name = f"{filename}_addedTime.csv"
    output_csv_pathfile = os.path.join(pathSave, save_csv_name)

    df.to_csv(output_csv_pathfile, index=False)

    print(f"\nSaved CSV: {output_csv_pathfile}")

    filename = os.path.splitext(os.path.basename(output_csv_pathfile))[0]

    print("Finished converting from .acq to .csv !!")

    return output_csv_pathfile, filename


def ProcessingHrvFreq(device_name, ppg_df, window_size, sampling_rate):
    # อย่าแตะต้อง ppg_df ต้นฉบับ
    local_df = ppg_df.copy()
    extracted_df = None  # ป้องกัน UnboundLocalError

    csv_time = len(local_df) // (sampling_rate * 60)
    print(f"This csv file has a recording length of ~{csv_time} miniutes. Recorded from {device_name}.")

    # จำนวนขนาดเวลา(วินาที) ที่ขยับ shift เพื่อคำนวณค่า hrv freq ต่าง ๆ
    window_samples = window_size * sampling_rate
    # if window_size == 300:
    #     ppg_df["NewLFHF"] = []

    try:
        if device_name == "EmotiBit" :
            if device_name == "EmotiBit":
                ppg_df["Timestamp"] = pd.to_datetime(ppg_df["LocalTimestamp"], unit="s").dt.tz_localize(
                    'UTC').dt.tz_convert("Asia/Bangkok")
                ppg_df.drop(columns=["LocalTimestamp"], inplace=True)

                ppg_cleaned = nk.ppg_clean(ppg_df["PG"], sampling_rate=sampling_rate)

                ppg_normalized = nk.rescale(ppg_cleaned, to=[-1, 1])

                hrv_results = []
                for start in range(0, len(ppg_normalized) - window_samples, sampling_rate):
                    end = start + window_samples
                    window = ppg_cleaned[start:end]
                    start_time = ppg_df['Timestamp'].iloc[start]
                    if start % 30 == 0:
                        print(f"Start Time: {start_time} - End Time: {ppg_df['Timestamp'].iloc[end]}")

                    # Filter out specific warning by message substring
                    warnings.filterwarnings("ignore", message=".*DFA_alpha2.*")
                    warnings.filterwarnings("ignore", message=".*mse = np.trapz(mse)*")

                    ppg_processed, info = nk.ppg_process(window, sampling_rate=sampling_rate)
                    signals, info = nk.ppg_peaks(ppg_processed["PPG_Clean"], sampling_rate=sampling_rate)

                    hrv_metrics = nk.hrv(signals, sampling_rate=sampling_rate)
                    hrv_metrics['Timestamp'] = start_time
                    hrv_results.append(hrv_metrics)
                    # if window_size == 300:
                    #     LFHFvalue = float(ppg_df['HRV_LF'] / ppg_df['HRV_HF'])
                    #     ppg_df["NewLFHF"].append(LFHFvalue)
                hrv_df = pd.concat(hrv_results, ignore_index=True)
                hrv_df['Timestamp'] = pd.to_datetime(hrv_df['Timestamp'])
                hrv_df = hrv_df.set_index('Timestamp')

                # extracted_df = hrv_df.resample('1s').max()
                if window_size == 60:
                    extracted_df = hrv_df.resample('1s').max()
                elif window_size == 120:
                    extracted_df = hrv_df.resample('2s').max()
                elif window_size == 300:
                    extracted_df = hrv_df.resample('5s').max()

                extracted_df.reset_index(inplace=True)
                extracted_df['HR'] = 60 / (extracted_df['HRV_MeanNN'] / 1000)


        elif device_name == "Biopac":
            window_samples = window_size * sampling_rate
            ppg_df["Timestamp"] = pd.to_datetime(ppg_df["Timestamp"], dayfirst=True)

            ppg_filtered = nk.signal_filter(ppg_df["PPG"],
                                            sampling_rate=sampling_rate,
                                            lowcut=0.5, highcut=5,
                                            method="bessel", order=5)

            ppg_clean = nk.ppg_clean(ppg_filtered, sampling_rate=sampling_rate)
            ppg_normalized = nk.rescale(ppg_clean, to=[-1, 1])

            hrv_results = []

            for start in range(0, len(ppg_normalized) - window_samples, sampling_rate):
                end = start + window_samples
                window = ppg_normalized[start:end]
                start_time = ppg_df['Timestamp'].iloc[start]
                if start % 30 == 0:
                    print(f"Start Time: {start_time} - End Time: {ppg_df['Timestamp'].iloc[end]}")

                # ปิด warning บางประเภทที่ไม่สำคัญ
                warnings.filterwarnings("ignore", message=".*DFA_alpha2.*")
                warnings.filterwarnings("ignore", message=".*mse = np.trapz(mse)*")
                warnings.filterwarnings("ignore", message=".*invalid value encountered in scalar divide.*")

                # try:
                ppg_processed, info = nk.ppg_process(window, sampling_rate=sampling_rate)
                signals, info = nk.ppg_peaks(ppg_processed["PPG_Clean"], sampling_rate=sampling_rate)
                hrv_metrics = nk.hrv(signals, sampling_rate=sampling_rate)
                # except Exception as e:
                #     print(f"HRV calc failed at {start_time}: {e}")
                #     # สร้างแถวว่างที่มี Timestamp อย่างเดียว
                #     hrv_metrics = pd.DataFrame(columns=nk.hrv(signals.iloc[:0], sampling_rate=sampling_rate).columns)
                #     hrv_metrics.loc[0] = [np.nan] * len(hrv_metrics.columns)

                hrv_metrics['Timestamp'] = start_time
                hrv_results.append(hrv_metrics)
                # if window_size == 300:
                #     LFHFvalue = float(ppg_df['HRV_LF'] / ppg_df['HRV_HF'])
                #     ppg_df["NewLFHF"].append(LFHFvalue)

            hrv_df = pd.concat(hrv_results, ignore_index=True)
            hrv_df['Timestamp'] = pd.to_datetime(hrv_df['Timestamp'])
            hrv_df = hrv_df.set_index('Timestamp')

            if window_size == 60:
                extracted_df = hrv_df.resample('1s').max()
            elif window_size == 120:
                extracted_df = hrv_df.resample('2s').max()
            elif window_size == 300:
                extracted_df = hrv_df.resample('5s').max()

            extracted_df.reset_index(inplace=True)
            extracted_df['HR'] = 60 / (extracted_df['HRV_MeanNN'] / 1000)
        else:
            print("Device Not Supported")
            return None
    except Exception as e:
        if csv_time < 1:
            print("\nInsufficient time for HF calculation, data length must be at least 1 minutes.\n")
            print(str(e))
        elif csv_time < 2:
            print("\nInsufficient time for LF calculation, data length must be at least 2 minutes.\n")
            print(str(e))
        elif csv_time < 5:
            print("\nInsufficient time for LF/HF calculation, data length must be at least 5 minutes.\n")
            print(str(e))
        else:
            print(f"Can't result to convert Timestamp! Error: {str(e)}")
    return extracted_df

def ProcessEDA(device_name, eda_df, sampling_rate):
    if device_name == "EmotiBit":
        timestamps = pd.to_datetime(eda_df['LocalTimestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert(
            'Asia/Bangkok')
        eda_df = eda_df.copy()
        eda_df['Timestamp'] = timestamps

        start_time = timestamps.iloc[0]
        one_minute_later = start_time + pd.Timedelta(minutes=1)
        eda_df_1min = eda_df[eda_df['Timestamp'] <= one_minute_later]

        m, wd, eda_clean = process_statistical(eda_df['EA'], use_scipy=True, sample_rate=15, new_sample_rate=15)

        phasic_gsr_combined = np.concatenate(wd['phasic_gsr'])
        tonic_gsr_combined = np.concatenate(wd['tonic_gsr'])
        eda_clean_combined = np.concatenate(eda_clean)

        n_1min_points = 60 * 15
        baseline_1min = tonic_gsr_combined[:n_1min_points]
        baseline_scl = baseline_1min.mean()

        tonic_corrected = tonic_gsr_combined - baseline_scl

        extracted_df = pd.DataFrame({
            'EDA_Phasic_E': phasic_gsr_combined,
            'EDA_Tonic_E': tonic_corrected,
            'EDA_E': eda_clean_combined,
        })

        extracted_df['Timestamp'] = timestamps
        extracted_df = extracted_df.set_index('Timestamp')

        extracted_df = extracted_df.resample("1s").max()
        extracted_df.reset_index(inplace=True)

    elif device_name == "Biopac":
        start_time = pd.to_datetime(eda_df['Timestamp'].iloc[0])
        one_minute_later = start_time + pd.Timedelta(minutes=1)
        eda_df_1min = eda_df[pd.to_datetime(eda_df['Timestamp']) <= one_minute_later]

        Biopac = nk.signal_resample(eda_df['EDA'], desired_sampling_rate=100, sampling_rate=100)
        new_timestamps = pd.date_range(start=start_time, periods=len(Biopac), freq='1ms')

        m, wd, eda_clean = process_statistical(eda_df['EDA'], use_scipy=True, sample_rate=100, new_sample_rate=100)
        phasic_gsr_combined = np.concatenate(wd['phasic_gsr'])
        tonic_gsr_combined = np.concatenate(wd['tonic_gsr'])
        eda_clean_combined = np.concatenate(eda_clean)

        baseline_1min = tonic_gsr_combined[:len(eda_df_1min)]
        baseline_scl = baseline_1min.mean()

        tonic_corrected = tonic_gsr_combined - baseline_scl

        extracted_df = pd.DataFrame({
            'EDA_Phasic_B': phasic_gsr_combined,
            'EDA_Tonic_B': tonic_corrected,
            'EDA_B': eda_clean_combined
        })
        extracted_df['Timestamp'] = new_timestamps
        extracted_df = extracted_df.set_index('Timestamp')

        extracted_df = extracted_df.resample("1s").max()
        extracted_df.reset_index(inplace=True)

    return extracted_df, baseline_scl
