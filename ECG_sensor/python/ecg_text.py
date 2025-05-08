import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 📌 1. Đọc dữ liệu ECG từ file CSV
file_path = "E:\PCG-PPG-ECG_Code\ecg_data.csv"  # Đổi đường dẫn file nếu cần
df = pd.read_csv(file_path)

# 📌 2. Chuyển đổi dữ liệu ADC sang điện áp (giả sử ADC 12-bit, 3.3V)
ADC_MAX = 4095  # ADC 12-bit
V_REF = 3.3  # Điện áp tham chiếu
fs = 100000  # Sampling rate (Hz) - thay bằng giá trị bạn đã dùng

# 📌 3. Chuyển ADC về đơn vị Volt
ecg_voltage = df * (V_REF / ADC_MAX)

# 📌 4. Tạo trục thời gian
time = np.linspace(0, len(ecg_voltage) / fs, len(ecg_voltage))

# 📌 5. Vẽ tín hiệu ECG
plt.figure(figsize=(12, 5))
plt.plot(time, ecg_voltage, label="ECG Signal", color="blue")
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (V)")
plt.title("ECG Signal from AD8232")
plt.legend()
plt.grid()
plt.show()
