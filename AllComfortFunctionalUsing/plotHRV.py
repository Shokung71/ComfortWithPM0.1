import matplotlib.pyplot as plt
import os
import platform
import subprocess

def open_with_default_app(file_path):
    system_name = platform.system()
    if system_name == "Windows":
        os.startfile(file_path)
    elif system_name == "Darwin":  # macOS
        subprocess.run(["open", file_path])
    else:  # Linux, Unix
        subprocess.run(["xdg-open", file_path])

def plot_hrv(hrvHFData, hrvLFData, hrvLFHFData, filename, pathSave):
    plt.figure(figsize=(12, 6))

    plt.plot(hrvHFData["Timestamp"], hrvHFData["HRV_HF"], label="HF (ms²)", color="blue")
    plt.plot(hrvLFData["Timestamp"], hrvLFData["HRV_LF"], label="LF (ms²)", color="green")
    plt.plot(hrvLFHFData["Timestamp"], hrvLFHFData["HRV_LFHF"], label="LF/HF Ratio", color="red")

    plt.xlabel("Time")
    plt.ylabel("Value (HF & LF: ms², LF/HF: ratio)")
    plt.title(f"HRV Frequency Domain Metrics: {filename}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # สร้าง path ไฟล์ภาพ
    image_filename = f"hrv_plot_{filename}.png"
    image_path = os.path.join(pathSave, image_filename)

    # บันทึกไฟล์ภาพ
    plt.savefig(image_path)
    plt.close()  # ปิด figure เพื่อไม่ให้กินหน่วยความจำ

    print(f"Saved plot to: {image_path}")

    # เปิดไฟล์ภาพทันที
    open_with_default_app(image_path)