import pandas as pd
import matplotlib.pyplot as plt

# Đọc file CSV (dùng raw string hoặc dấu /)
df = pd.read_csv(r'E:\PCG-PPG-ECG_Code\ecg_data.csv')

# Trích xuất dữ liệu
time = df["Time (s)"]  # tên cột có khoảng trắng ở đầu!
amplitude = df["Amplitude"]  # tên cột có khoảng trắng

# Vẽ biểu đồ
plt.figure(figsize=(12, 4))
plt.plot(time, amplitude)
plt.title('ECG Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.show()
